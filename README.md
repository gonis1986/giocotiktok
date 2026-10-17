# ⚡ ANDROBS Quantum Pinball Reactor — TikTok LIVE Interactive Arena

> **Motore Arcade Interattivo 2D Full HD (1080x1920) a 60 FPS in Tempo Reale per TikTok LIVE.**  
> Progettato per massimizzare il coinvolgimento degli spettatori, scatenare scariche di dopamina/endorfina sui regali (Rose, Super Gifts) e **azzerare qualsiasi restrizione algoritmica di TikTok per "contenuti riprodotti"**.

---

## 🎯 1. La Strategia Anti-Ban: Zero File Video, 100% Canvas HD

### Il Problema dei Contenuti Riprodotti su TikTok LIVE
Nelle trasmissioni interattive su TikTok LIVE, l'algoritmo automatico di moderazione scansiona costantemente i flussi video alla ricerca di video preregistrati o loop multimediali (`<video>`, file MP4, stream statici).  
Quando l'algoritmo rileva un file video in loop continuo:
1. Contrassegna la live come **"Contenuto Riproducibile / Pre-registrato"**.
2. **Sospende immediatamente la ricezione dei regali** (gli spettatori vedono i regali bloccati).
3. Esclude la trasmissione dal feed "Per Te" (FYP) e abbassa il shadowban della live.

### La Soluzione Architetturale Definitiva
Questo repository implementa l'azzeramento totale del tag `<video>`:
- **Zero MP4 / Zero flussi video preregistrati**: Tutta la scena 1080x1920 è generata fotogramma per fotogramma (`requestAnimationFrame`) tramite **HTML5 Canvas 2D ad altissima definizione** (`window.devicePixelRatio`).
- **Nessun frame identico**: La fisica delle particelle, i moti browniani, i rimbalzi elastici e i bumper reagiscono in tempo reale alle azioni degli spettatori. Per i server di TikTok la live è a tutti gli effetti una **sessione di videogame live interattivo a 60 FPS**, sbloccando la spinta nei "Per Te" e la monetizzazione dei regali.
- **Audio procedurale via Web Audio API**: Invece di file musicali statici, un sintetizzatore audio genera armonici, scale pentatoniche sui bumper e accordi dinamici che accelerano quando sale la barra del Caos.

---

## 🕹️ 2. Il Concetto del Gioco: Quantum Pinball Reactor

Il gioco fonde le meccaniche di **Flipper Neon (Pinball) + Plinko + Re del Reattore**, governato da un **Termometro del Caos (0% – 100%)**:

```
+-------------------------------------------------------------+
| ⚡ ANDROBS Studio        👥 SFÉRE ATTIVE        🎯 @streamer |
+-------------------------------------------------------------+
| 🌐 WWW.ANDROBS.COM — WEBCAM 4K 60FPS — AI LIVE TRANSLATOR  |
+-------------------------------------------------------------+
| 🔥 LIVELLO CAOS REATTORE: [============== 45% =============]|
| ❤️ Like = Attacco  | 💬 Chat = Turbo x2  | 🌹 Rosa = METEORA |
+-------------------------------------------------------------+
|                                                             |
|           (Bumper 1)                  (Bumper 2)            |
|                                                             |
|                         👑                                  |
|                 [ TRONO REATTORE ]                          |
|                 (Scudo Rotante HP)                          |
|                                                             |
|           (Bumper 3)                  (Bumper 4)            |
|                                                             |
|                 \                    /                      |
|                  \  SLINGSHOT KICK  /                       |
|                   ------------------                        |
+-------------------------------------------------------------+
| 👑 CLASSIFICA REATTORE (TOP 5) | ⚡ FEED EVENTI REAL-TIME   |
| 🥇 @User1          25,400 pt   | 🌹 @User dona 1 Rosa!      |
| 🥈 @User2          18,200 pt   | 💬 @User lancia Turbo x2!  |
+-------------------------------------------------------------+
| 00:00:00.000 | 60.0 FPS | 6,120 kb/s | ● BRIDGE ONLINE      |
+-------------------------------------------------------------+
```

### Elementi di Gioco nell'Arena:
1. **Il Trono del Reattore (Centro):**
   - Nucleo energetico circolare circondato da uno scudo rotante a segmenti.
   - Mostra l'avatar gigante, la corona 👑, il `@nickname` e il punteggio del **RE ATTUALE DELLA LIVE**.
   - Lo scudo ha una barra HP: ogni pallina normale che urta il nucleo sottrae energia. Chi sferra il colpo finale **espugna il Trono** con un'esplosione di particelle.
2. **6 Bumper Flipper al Neon:**
   - Disposti a cerchio attorno al Reattore.
   - All'impatto con una sfera, si espandono con un flash al neon, rilanciano la sfera ad altissima velocità (`restituzione: 1.35x`), emettono anelli d'onda concentrici e suonano note della scala pentatonica via Web Audio API.
3. **Respingenti Slingshot Inferiori:**
   - Posizionati sul fondo per rilanciare le sfere verso l'alto per 8–12 secondi di pura azione prima che la sfera si consumi.
4. **Sfere Giocatori in HD:**
   - Ogni sfera carica la foto profilo reale dello spettatore, contorno al neon, scia cometaria (motion trail a 12 punti) e `@nickname` in grassetto sempre dritto e leggibile.

---

## 💥 3. Il Termometro del Caos & Scarica di Endorfina sui Regali

- **Decay Naturale del Caos (-2.5% / secondo):**  
  Quando non arrivano regali, il livello di Caos scende gradualmente, mantenendo l'arena su toni ciano/viola rilassanti e fisica armoniosa.
- **❤️ Like / 💬 Chat:**  
  Genera sfere d'attacco o sfere Turbo x2 e aggiunge `+4%` di Caos.
- **🌹 1 Rosa (Scarica di Dopamina / Endorfina +40% Caos):**
  1. **Camera Shake & Golden Flash:** Lo schermo trema energicamente per 1.2 secondi e i bordi dell'arena pulsano in oro incandescente.
  2. **Audio Dopamina:** Accordo Fanfare sintetizzato in Web Audio API + Bass Drop subsonico (85Hz -> 30Hz) + pioggia scrosciante di monete metalliche, seguito dalla voce TTS entusiasta che annuncia l'incoronazione.
  3. **Impatto Fisico:** Dal cielo piove una **METEORA DORATA GIGANTE (`r=58px`)** con la faccia del donatore che si schianta al centro generando un'onda d'urto ad alta velocità che scaraventa tutte le sfere contro i Bumper.
  4. **Incoronazione Istantanea:** Il donatore conquista all'istante il **Trono del Reattore** e rilascia **6 Sfere Dorate Bonus**!
- **🌪️ Supernova Overdrive (80% – 100% Caos):**
  - Scatta se arrivano più regali in sequenza o donazioni maggiori (> 5 monete).
  - L'arena si accende di rosso e oro elettrico.
  - Per 8 secondi si attiva un **Vortice Gravitazionale (Buco Nero)** al centro: le sfere orbitano a spirale ad altissima velocità, si generano scariche di fulmini al neon tra le palline, e i punti di tutti i Bumper salgono a **`x10 JACKPOT`** con una pioggia di 12 sfere esplosive!

### Celebrazioni Scalate sul Valore del Regalo (diamanti)
Il bridge legge il `diamond_count` reale di ogni regalo TikTok: più il regalo vale, più lo spettacolo è enorme — è il meccanismo che spinge a donare regali più grandi.

| Valore totale | Livello | Effetto |
|---|---|---|
| 1 – 19 💎 | 🌹 Rosa | Meteora dorata + conquista del Trono + 6 sfere dorate |
| 20 – 99 💎 | 💥 Mega Regalo | Meteora gigante + 9 sfere dorate + caos +70% |
| ≥ 100 💎 | 💎 Jackpot Supremo | Meteora enorme + 12 sfere dorate + caos 100% + Supernova immediata |

I regali "combo/streak" di TikTok vengono conteggiati una sola volta alla fine della serie (non ad ogni tick), quindi il punteggio e gli effetti corrispondono al valore reale donato.

### Barra Obiettivo Regali (`?goal=DIAMANTI`)
Aprendo l'overlay con `?goal=100` compare una seconda barra dorata **OBIETTIVO REGALI** che si riempie ad ogni donazione in base ai diamanti ricevuti. Al raggiungimento: jackpot collettivo (celebrazione + supernova) e la barra riparte da zero. È il classico "gift goal" che mantiene alta la spinta alle donazioni per tutta la live.

### Modalità Torneo (`?tourney=MINUTI`)
Aprendo l'overlay con `?tourney=30` parte un **torneo a tempo**: barra dorata con countdown, regole riscritte ("TAP TAP sui like = punti gratis, rose/regali = sorpasso"), annuncio vocale delle regole all'avvio. Allo 00:00 i punteggi si congelano e il primo della classifica viene proclamato vincitore.

**Estrazione del premio — Ruota della Fortuna**: senza parametri extra, dopo la cerimonia del vincitore gira una ruota gigante che estrae il premio dal montepremi (default pesato sui premi piccoli: `5€,10€,15€,5€,3 MESI ANDROBS,10€,20€,5€` — costo medio ~9€/live). Personalizzabile con `?prizes=5€,10€,...`; con `?prize=20€` si forza un premio fisso e la ruota non gira.

Dettagli importanti:
- La classifica parte **vuota**: gli utenti demo precaricati non contano.
- Solo gli utenti con **eventi reali** (like, chat, regali via bridge) fanno punti — i giocatori simulati che animano l'arena a riposo non possono vincere il premio.
- I like sono il modo gratuito di accumulare punti: il torneo è vincibile anche senza donare.
- **Anti-ripetizione premio**: chi ha già vinto non può vincere di nuovo — allo scadere il premio passa al primo in classifica "vergine" di premio. I vincitori sono registrati in `tiktok_data/tiktok_winners.json` (scritto automaticamente a ogni incoronazione; modificabile a mano) e marcati 🏆✕ in classifica. Richiede `ANDROBS_PANEL_KEY` sul server e `&key=LA_CHIAVE` nell'URL dell'overlay; localStorage fa da riserva. `?repeat=1` disattiva il blocco.
- **Anti-autoclicker**: i punti gratis (like/chat/join/follow/share) hanno un tetto di 150 pt/s per utente, e chi supera ~25 tap/s per 3 secondi viene marchiato ⚠️ in classifica con punti like congelati 30s — uno script non può più battere un umano.
- Esempio completo: `tiktok.html?user=NOME&tourney=30&key=LA_CHIAVE`

### Pagina Regolamento (`regole.html`)
Pagina pubblica del torneo da mostrare/linkare prima della live: spiega l'appuntamento settimanale (domenica ore 20:00), le regole del gioco, il montepremi estratto con la Ruota, e le condizioni di ritiro (DM su Instagram/TikTok + video d'uso di ANDROBS sui social con tag, poi invio al canale YouTube ufficiale). Include il countdown live alla prossima domenica.

### Follow, Condivisioni e Abbonamenti
Anche gli eventi di crescita generano sfere e righe nel feed: **follow** (+30 pt), **share** (sfera dorata +80 pt — le condivisioni spingono l'algoritmo FYP) e **subscribe** (sfera dorata +500 pt).

---

## 🎙️ 4. Sponsorizzazione ANDROBS & Speaker Vocale in 4 Lingue

Anche senza video preregistrato, il brand e il prodotto sono sempre al centro dell'attenzione:
- **Banner Neon Safe Zone:** Marquee continuo e header dedicati a `WWW.ANDROBS.COM` (Webcam 4K 60fps da Smartphone, Traduttore Vocale AI, Zero Lag).
- **Speaker Vocale Automatico ogni 40s (Web Speech API):**  
  Quando non c'è una celebrazione regalo in corso, una voce madrelingua sintetizzata annuncia le funzionalità di ANDROBS con una card di sottotitoli elegante:
  - 🇮🇹 `it-IT`: *"Trasforma il tuo telefono in una webcam 4K e traduci la tua voce in tempo reale con androbs punto com!"*
  - 🇬🇧 `en-US`: *"Turn your phone into a 4K webcam with real-time AI voice translation! Visit androbs dot com!"*
  - 🇪🇸 `es-ES`: *"¡Convierte tu móvil en una webcam 4K con traducción de voz por IA en tiempo real en androbs punto com!"*
  - 🇯🇵 `ja-JP`: *"スマホを4Kウェブカメラに変えて、AIでリアルタイム音声翻訳！今すぐ androbs ドットコムへ！"*

---

## 🏗️ 5. Architettura di Sistema a 3 Livelli

```
+------------------------------------+
| 1. Server Linux / Contabo VPS      |
|    - bridge.py (TikTokLive)        |  <--- WebSocket con TikTok LIVE
|    - Systemd Daemon 24/7           |
+------------------------------------+
                  |
                  | HTTPS POST (con X-Bridge-Token)
                  v
+------------------------------------+
| 2. Web Server (Hosting / Apache)   |
|    - tiktok_events.php             |  <--- Buffer Circolare JSON (ultimi 50 eventi)
|    - tiktok_target_user.json       |
+------------------------------------+
                  |
                  | HTTPS GET (Polling 800ms ?since=ID)
                  v
+------------------------------------+
| 3. Client OBS Studio / Browser     |
|    - tiktok.html (1080x1920)       |  <--- Motore Canvas 2D 60 FPS
|    - Web Audio API + Speech Synth  |       Zero Lag, Zero Video
+------------------------------------+
```

### Livello 1: Daemon Python sul Server Contabo (Linux VPS)
1. **Connessione WebSocket a TikTok**:
   - Usa la libreria `TikTokLive` per intercettare gli eventi ufficiali (`ConnectEvent`, `LikeEvent`, `CommentEvent`, `GiftEvent`, `JoinEvent`).
   - Estrae gli avatar originali ad alta risoluzione (`avatar_large` / `avatar_medium`) degli spettatori.
2. **Resilienza e Auto-Riconnessione**:
   - Il daemon gestisce disconnessioni, stanze offline e crash riprovando la riconnessione ogni 15 secondi.
3. **Monitoraggio Dinamico Stanza (Zero Restart)**:
   - Un thread in background interroga ogni 12 secondi il backend web: se lo streamer cambia il proprio `@username` dall'interfaccia grafica del browser, il daemon effettua l'hot-swap della stanza senza dover riavviare il servizio di sistema.

### Livello 2: Backend API e Buffer Circolare (`tiktok_events.php`)
- **Autenticazione**: Accetta chiamate POST solo se l'header `X-Bridge-Token` coincide con la chiave di sicurezza definita nel server.
- **Buffer Circolare Leggero**: Memorizza gli eventi in un file JSON (`tiktok_live_queue.json`), mantenendo rigorosamente solo gli ultimi 50 record. Nessun database pesante (MySQL/PostgreSQL) necessario: tempi di risposta < 5ms.
- **Zero CORS**: Essendo servito dallo stesso dominio del gioco, non ci sono blocchi o ritardi di sicurezza nel browser.

### Livello 3: Frontend Game Engine (`tiktok.html`)
- **1080x1920 Full HD Nativo**: Rapporto d'aspetto perfetto 9:16 conforme al formato TikTok LIVE.
- **Supporto Auto-Fit Responsivo**: Si adatta a qualsiasi monitor o finestra OBS tramite CSS `scale()`.
- **Safe Zone Inferiore (310px)**: L'area inferiore dello schermo è protetta per consentire agli spettatori di leggere la chat di TikTok senza coprire l'azione dei Bumper.
- **Simulatore Ibrido Autonomo**: Se non arrivano eventi reali per oltre 2.5 secondi, un generatore intelligente mantiene attive da 6 a 10 sfere, e simula picchi di test ogni 45 secondi se la live è in fase di warmup.

---

## 🚀 6. Guida di Configurazione e Deploy

### A. Configurazione sul Server Contabo (Linux VPS)
1. Connettiti via SSH al tuo server:
   ```bash
   ssh root@YOUR_SERVER_IP
   ```
2. Crea la cartella del servizio e l'ambiente virtuale Python:
   ```bash
   mkdir -p /opt/androbs-tiktok-bridge
   cd /opt/androbs-tiktok-bridge
   python3 -m venv venv
   source venv/bin/activate
   pip install TikTokLive requests
   ```
3. Copia i file `bridge.py` e configura il file `.env`:
   ```bash
   nano /opt/androbs-tiktok-bridge/.env
   ```
   *Esempio contenuto `.env`:*
   ```ini
   TIKTOK_USER=tuo_username_tiktok
   ANDROBS_BACKEND_URL=https://www.tuodominio.com/tiktok_events.php
   ANDROBS_BRIDGE_TOKEN=tua_chiave_segreta_molto_sicura_2026
   ```

   Sul web server (PHP) puoi impostare due variabili d'ambiente:
   - `ANDROBS_BRIDGE_TOKEN` — obbligatorio, deve coincidere con quello del bridge.
   - `ANDROBS_PANEL_KEY` — opzionale: se impostata, il cambio di streamer
     monitorato (`?target=`) richiede anche il parametro `&key=`, così
     nessun altro può dirottare la stanza seguita dal bridge durante la live.
     In tal caso apri l'overlay come `tiktok.html?user=IL_TUO_USERNAME&key=LA_CHIAVE`.
4. Installa il servizio di sistema Systemd:
   ```bash
   cp androbs-tiktok-bridge.service /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable androbs-tiktok-bridge
   systemctl start androbs-tiktok-bridge
   ```
5. Verifica i log in tempo reale:
   ```bash
   journalctl -u androbs-tiktok-bridge -f
   ```

### B. Deploy dei File Web via FTP
1. Imposta le credenziali FTP nel tuo terminale locale:
   ```bash
   export FTP_HOST="ftp.tuodominio.com"
   export FTP_USER="tuo_utente_ftp"
   export FTP_PASS="tua_password_ftp"
   ```
2. Esegui lo script di deploy (tenta prima FTPS cifrato, ricade su FTP solo se il server non lo supporta):
   ```bash
   python deploy_ftp.py
   ```
   Lo script caricherà automaticamente:
   - `tiktok.html` -> `/htdocs/tiktok.html` e `/htdocs/b/tiktok.html`
   - `tiktok_events.php` -> `/htdocs/tiktok_events.php` e `/htdocs/b/tiktok_events.php`

### C. Aggiunta su OBS Studio / TikTok LIVE Studio
1. In OBS Studio, aggiungi una fonte **Browser (Browser Source)**.
2. Imposta l'URL su: `https://www.tuodominio.com/tiktok.html?user=IL_TUO_USERNAME`
   - Aggiungi `&goal=100` per mostrare la barra Obiettivo Regali (in diamanti).
   - Aggiungi `&key=LA_CHIAVE` se hai impostato `ANDROBS_PANEL_KEY` sul server.
3. Imposta le dimensioni fisse:
   - **Larghezza (Width):** `1080`
   - **Altezza (Height):** `1920`
4. Spunta le caselle:
   - *Arresta il codice sorgente quando non è visibile* = NO (mantieni attivo in background).
   - *Controlla l'audio tramite OBS* = SI (se desideri regolare i volumi dal mixer di OBS).
5. Premi **OK**: il gioco inizierà a girare a 60 FPS senza richiedere alcun file video!

---

## 🔒 7. Sicurezza e Privacy (Zero Credenziali Esposte)

Questo repository pubblico è conforme a tutte le best practice di sicurezza:
- Nessun indirizzo IP reale, password FTP o token privato è presente nel codice sorgente.
- Tutte le chiavi di autenticazione e gli endpoint sono gestiti tramite variabili d'ambiente (`.env`) e `.gitignore`.
- La comunicazione tra Contabo e il backend web è protetta da header personalizzati `X-Bridge-Token`.

---

## 📄 Licenza
Progetto rilasciato per l'ecosistema [ANDROBS Studio](https://www.androbs.com). Tutti i diritti riservati.
