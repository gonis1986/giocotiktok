#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deploy_ftp.py - Script di deploy automatico via FTP
Carica i file del gioco TikTok sul tuo web server senza esporre credenziali nel codice.

Configurazione:
Imposta le variabili d'ambiente prima dell'esecuzione:
  export FTP_HOST="ftp.tuodominio.com"
  export FTP_USER="tuo_utente_ftp"
  export FTP_PASS="tua_password_ftp"
"""

import os
import ssl
import sys
from ftplib import FTP, FTP_TLS, error_perm

FTP_HOST = os.environ.get("FTP_HOST")
FTP_USER = os.environ.get("FTP_USER")
FTP_PASS = os.environ.get("FTP_PASS")

FILES_TO_DEPLOY = [
    ("tiktok.html", "/htdocs/tiktok.html"),
    ("tiktok.html", "/htdocs/b/tiktok.html"),
    ("tiktok_events.php", "/htdocs/tiktok_events.php"),
    ("tiktok_events.php", "/htdocs/b/tiktok_events.php"),
]

def main():
    if not FTP_HOST or not FTP_USER or not FTP_PASS:
        print("[!] ERRORE: Credenziali FTP non trovate nelle variabili d'ambiente.")
        print("[i] Esegui:")
        print("    export FTP_HOST='ftp.tuosito.com'")
        print("    export FTP_USER='utente'")
        print("    export FTP_PASS='password'")
        sys.exit(1)

    print(f"=== Connessione FTP a {FTP_HOST} ===")

    # Preferisce FTPS esplicito (FTP_TLS): le credenziali non viaggiano in
    # chiaro. Se il server non lo supporta ricade sul FTP classico.
    ftp = None
    try:
        ftps = FTP_TLS(FTP_HOST, timeout=60)
        ftps.login(FTP_USER, FTP_PASS)
        ftps.prot_p()
        ftps.set_pasv(True)
        ftp = ftps
        print(f"[*] Login FTPS (cifrato) riuscito su {FTP_HOST}.")
    except (error_perm, OSError, ssl.SSLError) as e:
        print(f"[!] FTPS non disponibile ({e}), uso FTP in chiaro.")
        ftp = FTP(FTP_HOST, timeout=60)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.set_pasv(True)
        print(f"[*] Login FTP riuscito su {FTP_HOST}.")

    local_root = os.path.dirname(os.path.abspath(__file__))

    for rel_path, remote_path in FILES_TO_DEPLOY:
        local_path = os.path.join(local_root, rel_path)
        if not os.path.exists(local_path):
            print(f"[!] File locale mancante: {local_path}")
            continue

        file_size = os.path.getsize(local_path)
        print(f"[*] Caricamento: {rel_path} -> {remote_path} ({file_size / 1024:.1f} KB)...", end="", flush=True)
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f, blocksize=65536)
        print(" OK!")

    ftp.quit()
    print("[OK] Upload FTP completato con successo!")

if __name__ == "__main__":
    main()
