#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bridge.py - Daemon TikTok LIVE Event Bridge (Python / TikTokLive)
Eseguito sul server Linux / Contabo per connettersi ai WebSocket di TikTok LIVE
ed inoltrare in tempo reale Likes, Commenti, Ingressi e Regali al backend web.

NOTE FOR OPEN-SOURCE / AI DEVELOPERS:
Non inserire credenziali o token hardcoded in questo file.
Configura le variabili d'ambiente nel file .env o nel servizio systemd.
"""

import os
import sys
import time
import logging
import threading
import requests
from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent,
    CommentEvent,
    LikeEvent,
    GiftEvent,
    JoinEvent,
    FollowEvent,
    ShareEvent,
    SubscribeEvent,
    DisconnectEvent
)
from TikTokLive.client.errors import (
    UserOfflineError,
    UserNotFoundError,
    TikTokLiveError
)

# Configurazione Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TikTokBridge")

BACKEND_URL = os.environ.get("ANDROBS_BACKEND_URL", "https://YOUR_DOMAIN.com/tiktok_events.php")
SECRET_TOKEN = os.environ.get("ANDROBS_BRIDGE_TOKEN", "YOUR_SECURE_BRIDGE_TOKEN_HERE")
DEFAULT_USER = os.environ.get("TIKTOK_USER", "androbs_official")

current_client = None
active_target_user = None
should_restart_for_new_user = False

# Sessione HTTP persistente: riusa la connessione TLS invece di riaprirla
# ad ogni evento (decine di handshake al secondo durante i like-storm)
http_session = requests.Session()

def extract_avatar(user) -> str:
    """Estrae l'URL dell'avatar ad alta risoluzione dell'utente TikTok."""
    if not user:
        return ""
    for field in ['avatar_large', 'avatar_medium', 'avatar_thumb']:
        img = getattr(user, field, None)
        if img and getattr(img, 'url_list', None):
            for url in img.url_list:
                if url and isinstance(url, str) and url.startswith('http'):
                    return url
    return ""

def send_event_to_androbs(payload: dict):
    """Invia l'evento in formato JSON al backend web tramite POST con token di sicurezza."""
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Bridge-Token": SECRET_TOKEN
        }
        resp = http_session.post(BACKEND_URL, json=payload, headers=headers, timeout=4)
        if resp.status_code != 200:
            logger.warning("Backend response %s: %s", resp.status_code, resp.text[:100])
    except Exception as e:
        logger.error("Error sending event to backend: %s", e)

def get_remote_target_user():
    """Interroga l'endpoint leggero ?action=get_target per sapere quale stanza monitorare.

    Ritorna None in caso di errore di rete o risposta non valida: chi chiama
    deve mantenere l'utente corrente invece di saltare per errore alla stanza
    di default.
    """
    try:
        resp = http_session.get(BACKEND_URL, params={"action": "get_target"}, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            remote_u = data.get("target_user")
            if remote_u and isinstance(remote_u, str):
                cleaned = remote_u.strip().lstrip('@')
                if cleaned:
                    return cleaned
    except Exception as e:
        logger.debug("Failed to fetch remote target user: %s", e)
    return None

def monitor_target_changes():
    """Thread di monitoraggio per cambio dinamico della stanza TikTok senza riavvio del demone."""
    global active_target_user, should_restart_for_new_user, current_client
    while True:
        try:
            time.sleep(12)
            remote_user = get_remote_target_user()
            # remote_user None = backend irraggiungibile: NON cambiare stanza
            if remote_user and active_target_user and remote_user.lower() != active_target_user.lower():
                logger.info("Target user changed on backend: '%s' -> '%s'! Switching live room...", active_target_user, remote_user)
                should_restart_for_new_user = True
                if current_client and current_client.connected:
                    current_client.disconnect()
        except Exception as e:
            logger.error("Monitor thread error: %s", e)

def run_bridge_session(target_username: str):
    """Esegue la sessione di ascolto per lo username indicato."""
    global current_client, active_target_user, should_restart_for_new_user
    active_target_user = target_username
    should_restart_for_new_user = False

    logger.info("Starting TikTokLive listener for target: @%s", target_username)
    client = TikTokLiveClient(unique_id=target_username)
    current_client = client

    @client.on(ConnectEvent)
    def on_connect(event: ConnectEvent):
        logger.info(">>> CONNECTED to TikTok LIVE room of @%s (Room ID: %s)", target_username, client.room_id)
        send_event_to_androbs({
            "type": "connect",
            "user": target_username,
            "nickname": f"TikTok LIVE @{target_username}",
            "text": "Stanza TikTok connessa con successo!"
        })

    @client.on(JoinEvent)
    def on_join(event: JoinEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        logger.info("[JOIN] @%s (%s)", uname, nick)
        send_event_to_androbs({
            "type": "join",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "text": "entra nella LIVE"
        })

    @client.on(LikeEvent)
    def on_like(event: LikeEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        count = getattr(event, 'count', 1) or 1
        logger.info("[LIKE] @%s x%d", uname, count)
        send_event_to_androbs({
            "type": "like",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "repeatCount": count,
            "text": f"ha messo {count} Like"
        })

    @client.on(CommentEvent)
    def on_comment(event: CommentEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        text = getattr(event, 'comment', '') or ''
        logger.info("[CHAT] @%s: %s", uname, text)
        send_event_to_androbs({
            "type": "comment",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "text": text
        })

    @client.on(GiftEvent)
    def on_gift(event: GiftEvent):
        # Regali "streakable" (combo): TikTok emette un GiftEvent per OGNI
        # tick della combo con repeat_count parziale. Contiamo il regalo solo
        # alla fine dello streak, altrimenti una combo 100x genererebbe 100
        # celebrazioni complete e un punteggio gonfiato oltre il reale.
        if getattr(event, 'streaking', False):
            return

        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        gift_obj = getattr(event, 'gift', None)
        gift_name = getattr(gift_obj, 'gift_name', 'Rosa') if gift_obj else 'Rosa'
        count = getattr(event, 'repeat_count', 1) or getattr(event, 'combo_count', 1) or 1

        # Valore in diamanti dell'intero regalo (prezzo unitario x quantità)
        unit_value = getattr(gift_obj, 'diamond_count', 0) or 0
        gift_value = unit_value * count

        logger.info("[GIFT] @%s invia %dx %s (valore: %d diamanti)", uname, count, gift_name, gift_value)
        send_event_to_androbs({
            "type": "gift",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "giftName": gift_name,
            "repeatCount": count,
            "giftValue": gift_value,
            "text": f"ha donato {count}x {gift_name}!"
        })

    @client.on(FollowEvent)
    def on_follow(event: FollowEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        logger.info("[FOLLOW] @%s (%s)", uname, nick)
        send_event_to_androbs({
            "type": "follow",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "text": "ha iniziato a seguirti!"
        })

    @client.on(ShareEvent)
    def on_share(event: ShareEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        logger.info("[SHARE] @%s (%s)", uname, nick)
        send_event_to_androbs({
            "type": "share",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "text": "ha condiviso la LIVE!"
        })

    @client.on(SubscribeEvent)
    def on_subscribe(event: SubscribeEvent):
        u = event.user
        uname = u.unique_id if u else "Guest"
        nick = u.nickname if u and u.nickname else uname
        avatar = extract_avatar(u)
        logger.info("[SUBSCRIBE] @%s (%s)", uname, nick)
        send_event_to_androbs({
            "type": "subscribe",
            "user": uname,
            "nickname": nick,
            "avatar": avatar,
            "text": "si è abbonato al canale!"
        })

    @client.on(DisconnectEvent)
    def on_disconnect(event: DisconnectEvent):
        logger.warning("Disconnected from TikTok LIVE room @%s", target_username)

    try:
        client.run()
    except (UserOfflineError, UserNotFoundError) as e:
        logger.info("Room @%s is currently OFFLINE or NOT FOUND (%s). Will retry in 15 seconds...", target_username, e)
    except TikTokLiveError as e:
        logger.warning("TikTokLive error for @%s: %s. Retrying in 15 seconds...", target_username, e)
    except Exception as e:
        logger.error("Unexpected error for @%s: %s. Retrying in 15 seconds...", target_username, e)

def main():
    logger.info("==================================================")
    logger.info(" ANDROBS TIKTOK LIVE EVENT BRIDGE DAEMON")
    logger.info(" Backend: %s", BACKEND_URL)
    logger.info("==================================================")

    # Thread per il controllo periodico di cambio utente dal browser
    monitor_thread = threading.Thread(target=monitor_target_changes, daemon=True)
    monitor_thread.start()

    while True:
        # None = backend irraggiungibile: riprova senza toccare la stanza attiva
        target = get_remote_target_user() or active_target_user or DEFAULT_USER
        run_bridge_session(target)
        time.sleep(15)

if __name__ == "__main__":
    main()
