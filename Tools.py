import os
import time
import requests
import re
import socket
import threading
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# ─── COULEURS ANSI (VIVANTES) ────────────────────────────────────────────────
CYAN    = "\033[38;5;51m"
PURPLE  = "\033[38;5;165m"
BLUE    = "\033[38;5;33m"
GREEN   = "\033[38;5;82m"
YELLOW  = "\033[38;5;226m"
RED     = "\033[38;5;196m"
WHITE   = "\033[38;5;15m"
GRAY    = "\033[38;5;244m"
RESET   = "\033[0m"

CLEAR = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# ─── CONFIGURATION ──────────────────────────────────────────────────────────
BASE_DIR            = Path(__file__).resolve().parent
PHONE_API_KEY_OMKAR = os.getenv("PHONE_API_KEY_OMKAR", "")
EMAIL_API_KEY       = os.getenv("EMAIL_API_KEY", "")
WHOIS_API_KEY       = os.getenv("WHOIS_API_KEY", "")
DISCORD_BOT_TOKEN   = os.getenv("DISCORD_BOT_TOKEN", "")
DB_PATH             = BASE_DIR / "DB"

# ─── ANIMATIONS & UI ─────────────────────────────────────────────────────────
def fade_text(text, color):
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.005)
    print()

def animate_banner():
    CLEAR()
    colors = [PURPLE, BLUE, CYAN, GREEN, YELLOW, RED]
    banner_lines = [
        "▄████▄▓██   ██▓ ▄▄▄          ██░ ██  █    ██  ▄▄▄▄   ",
        "▒██▀ ▀█ ▒██  ██▒▒████▄       ▓██░ ██▒ ██  ▓██▒▓█████▄ ",
        "▒▓█    ▄ ▒██ ██░▒██  ▀█▄     ▒██▀▀██░▓██  ▒██░▒██▒ ▄██",
        "▒▓▓▄ ▄██▒░ ▐██▓░░██▄▄▄▄██    ░▓█ ░██ ▓▓█  ░██░▒██░█▀  ",
        "▒ ▓███▀ ░░ ██▒▓░ ▓█   ▓██▒   ░▓█▒░██▓▒▒█████▓ ░▓█  ▀█▓",
        "░ ░▒ ▒  ░ ██▒▒▒  ▒▒   ▓▒█░    ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░▒▓███▀▒",
        "  ░  ▒  ▓██ ░▒░   ▒   ▒▒ ░    ▒ ░▒░ ░░▒░ ░ ░ ▒░▒   ░ ",
        "░       ▒ ▒ ░░    ░   ▒       ░  ░░ ░ ░░░ ░ ░  ░    ░ ",
        "░ ░     ░ ░           ░  ░    ░  ░  ░   ░      ░      ",
        "░       ░ ░                                         ░ ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       "
    ]
    
    # Animation de balayage de couleur
    for i in range(len(colors)):
        CLEAR()
        color = colors[i]
        for line in banner_lines:
            print(f"{color}{line}{RESET}")
        print(f"{GRAY}                     [ Cia Hub - OSINT LOOKUP TOOL ]{RESET}")
        time.sleep(0.1)

def loading_animation(duration=1.5, msg="Recherche en cours..."):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        c = chars[i % len(chars)]
        sys.stdout.write(f"\r{PURPLE}[{c}]{RESET} {CYAN}{msg}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")

def show_banner():
    banner_lines = [
        "▄████▄▓██   ██▓ ▄▄▄          ██░ ██  █    ██  ▄▄▄▄   ",
        "▒██▀ ▀█ ▒██  ██▒▒████▄       ▓██░ ██▒ ██  ▓██▒▓█████▄ ",
        "▒▓█    ▄ ▒██ ██░▒██  ▀█▄     ▒██▀▀██░▓██  ▒██░▒██▒ ▄██",
        "▒▓▓▄ ▄██▒░ ▐██▓░░██▄▄▄▄██    ░▓█ ░██ ▓▓█  ░██░▒██░█▀  ",
        "▒ ▓███▀ ░░ ██▒▓░ ▓█   ▓██▒   ░▓█▒░██▓▒▒█████▓ ░▓█  ▀█▓",
        "░ ░▒ ▒  ░ ██▒▒▒  ▒▒   ▓▒█░    ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░▒▓███▀▒",
        "  ░  ▒  ▓██ ░▒░   ▒   ▒▒ ░    ▒ ░▒░ ░░▒░ ░ ░ ▒░▒   ░ ",
        "░       ▒ ▒ ░░    ░   ▒       ░  ░░ ░ ░░░ ░ ░  ░    ░ ",
        "░ ░     ░ ░           ░  ░    ░  ░  ░   ░      ░      ",
        "░       ░ ░                                         ░ ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       "
    ]
    for line in banner_lines:
        print(f"{PURPLE}{line}{RESET}")
    print(f"{GRAY}                     [ Cia Hub - OSINT LOOKUP TOOL ]{RESET}")

# ─── NOUVELLES FONCTIONS OSINT MASSIVES ───────────────────────────────────────

def threat_intel(target: str) -> dict:
    # Simulation d'analyse de menace (Intel)
    loading_animation(2, f"Analyzing Threat Intel for {target}...")
    try:
        r = requests.get(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{target}/general", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                "IP": target,
                "Reputation": d.get("reputation", 0),
                "Pulses": len(d.get("pulse_info", {}).get("pulses", [])),
                "Country": d.get("country_name", "Unknown"),
                "Malicious": "✅ Oui" if d.get("reputation", 0) > 0 else "❌ Non"
            }
        return {"error": "API Threat Intel inaccessible"}
    except: return {"error": "Erreur lors de l'analyse Intel"}

def bin_lookup(bin_code: str) -> dict:
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_code}", timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "BIN": bin_code,
                "Type": d.get("type", "Inconnu"),
                "Marque": d.get("scheme", "Inconnue"),
                "Banque": d.get("bank", {}).get("name", "Inconnue"),
                "Pays": d.get("country", {}).get("name", "Inconnu"),
                "Niveau": d.get("brand", "Inconnu")
            }
        return {"error": "BIN non trouvé"}
    except: return {"error": "Erreur API BIN"}

def vat_validator(vat: str) -> dict:
    try:
        r = requests.get(f"https://api.vatcomply.com/vat?vat_number={vat}", timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "VAT": vat,
                "Valide": "✅ Oui" if d.get("valid") else "❌ Non",
                "Nom": d.get("name", "Inconnu"),
                "Adresse": d.get("address", "Inconnue")
            }
        return {"error": "Numéro TVA invalide"}
    except: return {"error": "Erreur API TVA"}

def steam_id_lookup(steam_id: str) -> dict:
    try:
        # SteamID64 ou Vanité URL
        r = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=YOUR_STEAM_API_KEY&steamids={steam_id}", timeout=8)
        # Simulation sans clé API réelle
        return {"SteamID": steam_id, "Status": "Vérifie manuellement (Clé API requise)"}
    except: return {"error": "Erreur Steam API"}

def clone_website(url: str) -> dict:
    """Refuse la copie de sites, qui peut servir à l'usurpation et au phishing."""
    return {"error": "Copie de sites désactivée dans cette version publique."}

    """Clone réellement un site web avec téléchargement des fichiers"""
    import urllib.parse
    import os
    import re
    from urllib.parse import urljoin, urlparse
    
    # Étape 1: Analyse de l'URL
    print(f"{CYAN}[1/6]{RESET} {YELLOW}Analyse de l'URL...{RESET}")
    time.sleep(0.5)
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    clone_folder = f"clone_{domain.replace('.', '_')}"
    
    try:
        os.makedirs(clone_folder, exist_ok=True)
        print(f"{GREEN}   URL valide: {url}{RESET}")
    except Exception as e:
        return {"error": f"Erreur création dossier: {e}"}
    
    # Étape 2: Téléchargement du HTML principal
    print(f"{CYAN}[2/6]{RESET} {YELLOW}Téléchargement HTML principal...{RESET}")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return {"error": f"Site inaccessible (HTTP {response.status_code})"}
        
        html_content = response.text
        print(f"{GREEN}   HTML téléchargé ({len(html_content)} caractères){RESET}")
        
        # Sauvegarder index.html
        with open(os.path.join(clone_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        return {"error": f"Erreur téléchargement HTML: {e}"}
    
    # Étape 3: Extraction et téléchargement des assets
    print(f"{CYAN}[3/6]{RESET} {YELLOW}Extraction et téléchargement des assets...{RESET}")
    
    assets_downloaded = 0
    total_size = 0
    
    # Créer les dossiers pour les assets
    os.makedirs(os.path.join(clone_folder, "css"), exist_ok=True)
    os.makedirs(os.path.join(clone_folder, "js"), exist_ok=True)
    os.makedirs(os.path.join(clone_folder, "images"), exist_ok=True)
    
    # Extraire les URLs des assets avec regex
    css_pattern = r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']'
    js_pattern = r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']'
    img_pattern = r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg)[^"\']*)["\']'
    
    # Télécharger les CSS
    css_matches = re.findall(css_pattern, html_content, re.IGNORECASE)
    for css_url in css_matches:
        try:
            full_css_url = urljoin(url, css_url)
            css_response = requests.get(full_css_url, headers=headers, timeout=10)
            if css_response.status_code == 200:
                css_filename = os.path.basename(css_url.split('?')[0])
                with open(os.path.join(clone_folder, "css", css_filename), "w", encoding="utf-8") as f:
                    f.write(css_response.text)
                assets_downloaded += 1
                total_size += len(css_response.content)
                print(f"{GREEN}   CSS: {css_filename}{RESET}")
        except:
            continue
    
    # Télécharger les JS
    js_matches = re.findall(js_pattern, html_content, re.IGNORECASE)
    for js_url in js_matches:
        try:
            full_js_url = urljoin(url, js_url)
            js_response = requests.get(full_js_url, headers=headers, timeout=10)
            if js_response.status_code == 200:
                js_filename = os.path.basename(js_url.split('?')[0])
                with open(os.path.join(clone_folder, "js", js_filename), "w", encoding="utf-8") as f:
                    f.write(js_response.text)
                assets_downloaded += 1
                total_size += len(js_response.content)
                print(f"{GREEN}   JS: {js_filename}{RESET}")
        except:
            continue
    
    # Télécharger les images (limité aux 10 premières pour éviter trop de temps)
    img_matches = re.findall(img_pattern, html_content, re.IGNORECASE)
    img_matches = img_matches[:10]  # Limiter à 10 images
    
    for img_url in img_matches:
        try:
            full_img_url = urljoin(url, img_url)
            img_response = requests.get(full_img_url, headers=headers, timeout=10)
            if img_response.status_code == 200:
                img_filename = os.path.basename(img_url.split('?')[0])
                with open(os.path.join(clone_folder, "images", img_filename), "wb") as f:
                    f.write(img_response.content)
                assets_downloaded += 1
                total_size += len(img_response.content)
                print(f"{GREEN}   IMG: {img_filename}{RESET}")
        except:
            continue
    
    print(f"{GREEN}   {assets_downloaded} assets téléchargés{RESET}")
    
    # Étape 4: Modification des URLs dans le HTML pour les liens locaux
    print(f"{CYAN}[4/6]{RESET} {YELLOW}Modification des URLs locales...{RESET}")
    time.sleep(0.5)
    
    # Remplacer les URLs par des chemins locaux
    modified_html = html_content
    
    # Remplacer les CSS
    for css_url in css_matches:
        css_filename = os.path.basename(css_url.split('?')[0])
        # Remplacer toutes les occurrences de l'URL
        modified_html = re.sub(re.escape(css_url), f"css/{css_filename}", modified_html, flags=re.IGNORECASE)
    
    # Remplacer les JS
    for js_url in js_matches:
        js_filename = os.path.basename(js_url.split('?')[0])
        modified_html = re.sub(re.escape(js_url), f"js/{js_filename}", modified_html, flags=re.IGNORECASE)
    
    # Remplacer les images
    for img_url in img_matches:
        img_filename = os.path.basename(img_url.split('?')[0])
        modified_html = re.sub(re.escape(img_url), f"images/{img_filename}", modified_html, flags=re.IGNORECASE)
    
    # Ajouter un header pour forcer le chargement local
    meta_tag = '<meta name="clone-info" content="Cia Hub - Local Version">\n'
    modified_html = modified_html.replace('<head>', '<head>\n' + meta_tag)
    
    # Désactiver certaines restrictions CORS pour le fonctionnement local
    cors_disable = '<script>\n// Disable CORS restrictions for local clone\nif (typeof fetch !== "undefined") {\n  const originalFetch = window.fetch;\n  window.fetch = function(url, options) {\n    if (url.startsWith("http")) {\n      return originalFetch(url.replace(/^https?:\\/\\//, window.location.origin + "/"), options);\n    }\n    return originalFetch(url, options);\n  };\n}\n</script>\n</head>'
    modified_html = modified_html.replace('</head>', cors_disable)
    
    # Sauvegarder le HTML modifié
    with open(os.path.join(clone_folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(modified_html)
    
    print(f"{GREEN}   URLs locales configurées{RESET}")
    
    # Étape 5: Création d'un fichier README et version simplifiée si nécessaire
    print(f"{CYAN}[5/6]{RESET} {YELLOW}Création des métadonnées...{RESET}")
    time.sleep(0.3)
    
    # Détecter si c'est un site dynamique (Discord, etc.)
    is_dynamic_site = any(keyword in html_content.lower() for keyword in ['discord', 'react', 'webpack', 'chunk', 'dynamic'])
    
    if is_dynamic_site:
        print(f"{YELLOW}   Site dynamique détecté - Création version simplifiée...{RESET}")
        
        # Créer une version simplifiée pour les sites dynamiques
        simple_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clone de {domain}</title>
    <link rel="stylesheet" href="css/discord-2022.shared.37d7c19df.min.css">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #36393f; color: #dcddde; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .info {{ background: #4f545c; padding: 20px; border-radius: 8px; margin: 10px 0; }}
        .assets {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
        .asset-item {{ background: #2f3136; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Site Clone: {domain}</h1>
            <p>Clone créé par Cia Hub</p>
        </div>
        <div class="info">
            <h2>Informations du Clone</h2>
            <p><strong>URL originale:</strong> <a href="{url}" target="_blank">{url}</a></p>
            <p><strong>Date de clonage:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Assets téléchargés:</strong> {assets_downloaded}</p>
            <p><strong>Taille totale:</strong> {total_size / 1024:.1f} KB</p>
            <p><strong>Type:</strong> Site dynamique (version simplifiée)</p>
        </div>
        <div class="info">
            <h2>Assets Disponibles</h2>
            <div class="assets">
                <div class="asset-item">
                    <h3>CSS ({len(css_matches)})</h3>
                    <p>Feuilles de style téléchargées</p>
                </div>
                <div class="asset-item">
                    <h3>JavaScript ({len(js_matches)})</h3>
                    <p>Scripts téléchargés</p>
                </div>
                <div class="asset-item">
                    <h3>Images ({len(img_matches)})</h3>
                    <p>Images téléchargées</p>
                </div>
            </div>
        </div>
        <div class="info">
            <h2>Note</h2>
            <p>Ce site utilise des technologies modernes (React, APIs dynamiques). 
            Le clone contient tous les assets téléchargés mais certaines fonctionnalités 
            peuvent nécessiter une connexion internet pour fonctionner pleinement.</p>
            <p>Pour voir le site original, visitez: <a href="{url}" target="_blank">{url}</a></p>
        </div>
    </div>
</body>
</html>"""
        
        # Sauvegarder la version simplifiée
        with open(os.path.join(clone_folder, "index_simple.html"), "w", encoding="utf-8") as f:
            f.write(simple_html)
        
        print(f"{GREEN}   Version simplifiée créée: index_simple.html{RESET}")
    
    readme_content = f"""# Site Clone: {domain}
URL originale: {url}
Date de clonage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Assets téléchargés: {assets_downloaded}
Taille totale: {total_size / 1024:.1f} KB
Type de site: {"Dynamique" if is_dynamic_site else "Statique"}

## Structure:
- index.html (version complète avec liens locaux)
- index_simple.html (version simplifiée pour sites dynamiques)
- css/ (feuilles de style)
- js/ (scripts JavaScript)
- images/ (images)

## Pour visualiser:
{"Ouvrez index_simple.html pour les sites dynamiques comme Discord" if is_dynamic_site else "Ouvrez index.html dans votre navigateur web."}

## Note:
{"Les sites modernes comme Discord chargent leur contenu via JavaScript. La version simplifiée affiche les informations du clone et les assets téléchargés." if is_dynamic_site else "Clone statique complet fonctionnel."}
"""
    
    with open(os.path.join(clone_folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Étape 6: Finalisation
    print(f"{CYAN}[6/6]{RESET} {YELLOW}Finalisation...{RESET}")
    time.sleep(0.5)
    
    print(f"{GREEN}   Clone terminé avec succès!{RESET}")
    print(f"{GREEN}   Dossier: {clone_folder}/{RESET}")
    print(f"{GREEN}   Ouvrez index.html pour visualiser{RESET}")
    
    return {
        "url_original": url,
        "domaine": domain,
        "dossier_clone": clone_folder,
        "assets_telecharges": assets_downloaded,
        "taille_totale": f"{total_size / 1024:.1f} KB",
        "statut": "Clonage réel terminé",
        "fichiers": {
            "html": "index.html",
            "css": f"{len(css_matches)} fichiers",
            "js": f"{len(js_matches)} fichiers", 
            "images": f"{len(img_matches)} fichiers"
        }
    }

# ─── FONCTIONS EXISTANTES AMÉLIORÉES ──────────────────────────────────────────

def tiktok_info(username: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            return {"Username": username, "URL": f"https://www.tiktok.com/@{username}", "Status": "Actif"}
        return {"error": "Compte introuvable ou protégé"}
    except: return {"error": "Erreur réseau"}

def minecraft_info(username: str) -> dict:
    try:
        r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}", timeout=8)
        if r.status_code == 200:
            d = r.json()
            uuid = d.get("id")
            r_hist = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names", timeout=8)
            names = [n['name'] for n in r_hist.json()] if r_hist.status_code == 200 else []
            return {"Username": d.get("name"), "UUID": uuid, "Historique": " -> ".join(names)}
        return {"error": "Joueur introuvable"}
    except: return {"error": "Erreur API Mojang"}

def instagram_info(username: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://www.instagram.com/{username}/?__a=1&__d=dis", headers=headers, timeout=10)
        if r.status_code == 200:
            return {"Username": username, "URL": f"https://www.instagram.com/{username}/", "Status": "Vérifie manuellement"}
        return {"error": "Compte introuvable ou privé"}
    except: return {"error": "Erreur réseau"}

def proxy_check(ip: str) -> dict:
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy,hosting,vpn", timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "IP": ip,
                "Proxy": "✅ Oui" if d.get("proxy") else "❌ Non",
                "VPN": "✅ Oui" if d.get("vpn") else "❌ Non",
                "Hosting": "✅ Oui" if d.get("hosting") else "❌ Non"
            }
        return {"error": f"HTTP {r.status_code}"}
    except: return {"error": "Erreur API Proxy Check"}

def discord_server_info(guild_id: str, token: str) -> dict:
    headers = get_discord_headers(token)
    if not headers: return {"error": "Token invalide"}
    try:
        r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}?with_counts=true", headers=headers, timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                "Nom": d.get("name"),
                "ID": d.get("id"),
                "Propriétaire": d.get("owner_id"),
                "Membres": d.get("approximate_member_count"),
                "En ligne": d.get("approximate_presence_count"),
                "Boosts": d.get("premium_subscription_count"),
                "Niveau": d.get("premium_tier")
            }
        return {"error": f"HTTP {r.status_code}"}
    except: return {"error": "Erreur API Discord"}

def nitro_gen(count: int):
    import random
    import string
    codes = []
    for _ in range(count):
        code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        codes.append(f"https://discord.gift/{code}")
    return codes

def show_title_animation():
    CLEAR()
    lines = [
        "Cia Hub System Booting...",
        "Loading Neural API Hub...",
        "Initializing Global DB Sync...",
        "Connection Secure. System Ready."
    ]
    for line in lines:
        print(f"{PURPLE}[*]{RESET} {CYAN}{line}{RESET}")
        time.sleep(0.25)
    time.sleep(0.4)

# ─── NOUVEAUX OUTILS OSINT ───────────────────────────────────────────────────

def port_scanner(target):
    loading_animation(2, f"Scanning ports on {target}...")
    common_ports = [21, 22, 23, 25, 53, 80, 88, 110, 111, 135, 139, 143, 443, 445, 548, 587, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443]
    results = {}
    lock = threading.Lock()

    def scan_port(p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            if s.connect_ex((target, p)) == 0:
                try: service = socket.getservbyport(p)
                except: service = "Inconnu"
                with lock: results[p] = f"OUVERT ({service})"
        except: pass
        finally: s.close()

    threads = []
    for port in common_ports:
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()
    
    for t in threads: t.join()
    
    return dict(sorted(results.items())) if results else {"status": "Aucun port commun ouvert"}

def username_tracker(username):
    sites = {
        "Instagram": f"https://www.instagram.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Twitter": f"https://www.twitter.com/{username}",
        "GitHub": f"https://www.github.com/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Linktree": f"https://linktr.ee/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Medium": f"https://medium.com/@{username}"
    }
    results = {}
    lock = threading.Lock()

    def check_site(name, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            r = requests.get(url, timeout=5, headers=headers)
            with lock:
                if r.status_code == 200:
                    # Certains sites retournent 200 même si l'utilisateur n'existe pas, on peut ajouter des checks spécifiques ici
                    if name == "TikTok" and "tiktok.com/@" not in r.url: results[name] = "❌ Non trouvé"
                    elif name == "Instagram" and "login" in r.url: results[name] = "⚠️ Possible (Login requis)"
                    else: results[name] = f"✅ Trouvé : {url}"
                else: results[name] = "❌ Non trouvé"
        except:
            with lock: results[name] = "⚠️ Erreur"

    threads = []
    for name, url in sites.items():
        t = threading.Thread(target=check_site, args=(name, url))
        threads.append(t)
        t.start()
    
    for t in threads: t.join()
    return results

def dns_lookup(domain):
    loading_animation(1, f"Analyse DNS pour {domain}...")
    types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    results = {}
    try:
        import dns.resolver
        for t in types:
            try:
                answers = dns.resolver.resolve(domain, t)
                results[t] = [str(rdata) for rdata in answers]
            except: continue
    except ImportError:
        # Fallback simple si dnspython n'est pas là
        try: results['A'] = [socket.gethostbyname(domain)]
        except: return {"error": "dnspython non installé et fallback échoué"}
    return results if results else {"error": "Aucun enregistrement trouvé"}

def get_discord_headers(token):
    token = token.strip()
    # On teste d'abord sans préfixe (User Token)
    headers_user = {"Authorization": token, "Content-Type": "application/json"}
    try:
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers_user, timeout=5)
        if r.status_code == 200: return headers_user
    except: pass
    
    # Sinon on teste avec préfixe (Bot Token)
    headers_bot = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    try:
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers_bot, timeout=5)
        if r.status_code == 200: return headers_bot
    except: pass
    
    return None

def discord_backup(guild_id, token):
    return {"error": "Export et duplication de serveurs désactivés dans cette version publique."}

    headers = get_discord_headers(token)
    if not headers: return {"error": "Token invalide (401)", "conseil": "Vérifie ton token."}
    
    loading_animation(2, f"Génération du backup pour {guild_id}...")
    try:
        r_guild = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers, timeout=10)
        if r_guild.status_code != 200: return {"error": f"Erreur Guild: {r_guild.status_code}"}
        guild_data = r_guild.json()

        r_channels = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers, timeout=10)
        channels = r_channels.json() if r_channels.status_code == 200 else []

        r_roles = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers, timeout=10)
        roles = r_roles.json() if r_roles.status_code == 200 else []

        backup = {
            "info": {
                "name": guild_data.get("name"),
                "id": guild_id,
                "backup_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            },
            "channels": [{"id": c["id"], "name": c["name"], "type": c["type"], "position": c.get("position"), "parent_id": c.get("parent_id")} for c in channels],
            "roles": [{"name": r["name"], "color": r["color"], "permissions": r["permissions"]} for r in roles]
        }

        filename = f"backup_{guild_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(backup, f, indent=4, ensure_ascii=False)
        
        return {"status": "✅ SUCCÈS", "serveur": guild_data.get("name"), "fichier": filename, "salons": len(channels), "rôles": len(roles)}
    except Exception as e: return {"error": str(e)}

def discord_load_backup(target_guild_id, token, backup_file):
    return {"error": "Export et duplication de serveurs désactivés dans cette version publique."}

    headers = get_discord_headers(token)
    if not headers: return {"error": "Token invalide (401)"}
    
    if not os.path.exists(backup_file): return {"error": f"Fichier {backup_file} introuvable."}
    
    try:
        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        loading_animation(3, f"Clonage en cours sur {target_guild_id}...")
        
        # 1. Création des Rôles
        roles_created = 0
        for role in data.get("roles", []):
            if role["name"] != "@everyone":
                requests.post(f"https://discord.com/api/v10/guilds/{target_guild_id}/roles", headers=headers, json={"name": role["name"], "color": role["color"], "permissions": role["permissions"]}, timeout=10)
                roles_created += 1
                time.sleep(0.4)

        # 2. Création des Catégories (type 4)
        category_map = {} # {old_id: new_id}
        for chan in data.get("channels", []):
            if chan["type"] == 4:
                r = requests.post(f"https://discord.com/api/v10/guilds/{target_guild_id}/channels", headers=headers, json={"name": chan["name"], "type": 4, "position": chan["position"]}, timeout=10)
                if r.status_code in [200, 201]:
                    category_map[chan["id"]] = r.json()["id"]
                time.sleep(0.4)

        # 3. Création des autres Salons
        channels_created = 0
        for chan in data.get("channels", []):
            if chan["type"] != 4:
                payload = {"name": chan["name"], "type": chan["type"], "position": chan["position"]}
                if chan.get("parent_id") in category_map:
                    payload["parent_id"] = category_map[chan["parent_id"]]
                
                r = requests.post(f"https://discord.com/api/v10/guilds/{target_guild_id}/channels", headers=headers, json=payload, timeout=10)
                if r.status_code in [200, 201]:
                    channels_created += 1
                time.sleep(0.4)

        return {"status": "✅ CLONAGE TERMINÉ", "serveur_cible": target_guild_id, "salons": channels_created, "catégories": len(category_map), "rôles": roles_created}
    except Exception as e: return {"error": str(e)}

# ─── DATABASE SEARCH ─────────────────────────────────────────────────────────
def db_search(query: str, use_regex: bool = False):
    if not os.path.exists(DB_PATH):
        return {"error": f"Dossier DB introuvable à {DB_PATH}"}
    results = []
    loading_animation(2, f"Scanning databases for '{query}'...")
    
    pattern = None
    if use_regex:
        try: pattern = re.compile(query, re.IGNORECASE)
        except Exception as e: return {"error": f"Regex invalide : {e}"}

    for root, dirs, files in os.walk(DB_PATH):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                category = os.path.basename(root)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            found = False
                            if use_regex:
                                if pattern.search(line): found = True
                            else:
                                if query.lower() in line.lower(): found = True
                            
                            if found:
                                results.append({"category": category, "file": file, "content": line, "line": line_num})
                                if len(results) >= 100: return results # Limite pour éviter les lags
                except: continue
    return results

# ─── LOOKUPS CLASSIQUES (PHONE, EMAIL, IP, ROBLOX, DISCORD, WHOIS) ───────────
def discord_creation_date(user_id: str) -> str:
    try:
        snowflake = int(user_id)
        timestamp_ms = (snowflake >> 22) + 1420070400000
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return dt.strftime("%d/%m/%Y %H:%M:%S UTC")
    except: return "Inconnu"

def email_lookup(email: str) -> dict:
    email = email.strip().lower()
    if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email): return {"error": "Format invalide"}
    if not EMAIL_API_KEY: return {"error": "EMAIL_API_KEY non configurée"}
    try:
        r = requests.get(f"https://client.myemailverifier.com/verifier/validate_single/{email}/{EMAIL_API_KEY}", timeout=12)
        if r.status_code == 200:
            d = r.json()
            s = d.get("Status", "UNKNOWN").upper()
            return {"email": email, "status": s, "score": d.get("score", "—"), "deliverable": "✅" if s in ["VALID", "OK"] else "❌", "disposable": "Oui" if str(d.get("Disposable_Domain")).lower()=="true" else "Non"}
        return {"error": f"HTTP {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def phone_lookup(local_input: str, calling_code: str) -> dict:
    cleaned = re.sub(r'[^0-9+]', '', local_input.strip()).lstrip('+')
    if cleaned.startswith('0'): cleaned = cleaned[1:]
    if not PHONE_API_KEY_OMKAR: return {"error": "PHONE_API_KEY_OMKAR non configurée"}
    try:
        r = requests.get("https://carrier-lookup-api.omkar.cloud/lookup", params={"phone": f"+{calling_code}{cleaned}"}, headers={"API-Key": PHONE_API_KEY_OMKAR}, timeout=10)
        return r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def ip_lookup(ip: str = None) -> dict:
    url = "https://ipapi.co/json/" if not ip else f"https://ipapi.co/{ip}/json/"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            # On enrichit avec des infos de base
            return {
                "IP": d.get("ip"),
                "Ville": d.get("city"),
                "Région": d.get("region"),
                "Pays": f"{d.get('country_name')} ({d.get('country_code')})",
                "Continent": d.get("continent_code"),
                "Postal": d.get("postal"),
                "Latitude": d.get("latitude"),
                "Longitude": d.get("longitude"),
                "ASN": d.get("asn"),
                "Organisation": d.get("org"),
                "Fuseau": d.get("timezone"),
                "Appel": f"+{d.get('country_calling_code')}",
                "Devise": d.get("currency")
            }
        return {"error": f"HTTP {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def roblox_info(user_id: str) -> dict:
    try:
        r = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=8)
        d = r.json()
        return {"username": d.get("name"), "display": d.get("displayName"), "creation": d.get("created")[:10], "banned": d.get("isBanned")}
    except Exception as e: return {"error": str(e)}

def mac_lookup(mac: str) -> dict:
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}", timeout=8)
        return {"mac": mac, "constructeur": r.text if r.status_code == 200 else "Inconnu"}
    except: return {"error": "Impossible de contacter l'API"}

def iban_validator(iban: str) -> dict:
    iban = iban.replace(" ", "").upper()
    try:
        r = requests.get(f"https://openiban.com/validate/{iban}?get_bank_data=true", timeout=8)
        if r.status_code == 200:
            d = r.json()
            bank = d.get("bankData", {})
            return {
                "iban": iban,
                "valide": "✅ Oui" if d.get("valid") else "❌ Non",
                "banque": bank.get("name", "Inconnue"),
                "ville": bank.get("city", "Inconnue"),
                "bic": bank.get("bic", "Inconnu")
            }
        return {"error": f"HTTP {r.status_code}"}
    except: return {"error": "Erreur lors de la validation"}

def subdomain_finder(domain: str) -> list:
    loading_animation(2, f"Recherche de sous-domaines pour {domain}...")
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=15)
        if r.status_code == 200:
            subs = set()
            for entry in r.json():
                name = entry['name_value']
                if "\n" in name:
                    for n in name.split("\n"): subs.add(n)
                else: subs.add(name)
            return sorted(list(subs))
        return {"error": f"HTTP {r.status_code}"}
    except: return {"error": "Erreur lors de la recherche"}

def discord_info(user_id: str) -> dict:
    if not DISCORD_BOT_TOKEN: return {"error": "DISCORD_BOT_TOKEN non configurée"}

    try:
        headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
        r = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers=headers, timeout=8)
        if r.status_code == 200:
            d = r.json()
            avatar_hash = d.get("avatar")
            banner_hash = d.get("banner")
            
            # Reconstruction des URLs
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=1024" if avatar_hash else "Aucun"
            banner_url = f"https://cdn.discordapp.com/banners/{user_id}/{banner_hash}.png?size=1024" if banner_hash else "Aucune"
            
            res = {
                "Username": d.get("username"),
                "Global Name": d.get("global_name", "Aucun"),
                "ID": d.get("id"),
                "Création": discord_creation_date(user_id),
                "Avatar": avatar_url,
                "Banner": banner_url,
                "Bot": "Oui" if d.get("bot") else "Non",
                "Flags": d.get("public_flags", 0)
            }
            
            # Recherche de Prevnames (via source externe simulée car pas d'API publique gratuite stable)
            try:
                r_prev = requests.get(f"https://discord.id/api/v1/user/{user_id}", timeout=5)
                if r_prev.status_code == 200:
                    prev_data = r_prev.json()
                    res["Prevnames (DB)"] = prev_data.get("previous_usernames", ["Aucun historique trouvé"])
            except:
                res["Prevnames (DB)"] = "Erreur de connexion à la DB de noms"
                
            return res
        elif r.status_code == 401:
            return {"error": "Token Bot Invalide (401)", "conseil": "Vérifie DISCORD_BOT_TOKEN dans le code."}
        return {"error": f"HTTP {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def whois_info(domain: str) -> dict:
    domain = domain.strip().lower()
    if domain.endswith('.fr'):
        try:
            r = requests.get(f"https://rdap.afnic.fr/domain/{domain}", timeout=10)
            if r.status_code == 200:
                d = r.json()
                res = {"domaine": domain, "source": "AFNIC"}
                for e in d.get("events", []):
                    if "registration" in e["eventAction"]: res["création"] = e["eventDate"][:10]
                return res
        except: pass
    if not WHOIS_API_KEY: return {"error": "WHOIS_API_KEY non configurée (RDAP .fr uniquement sans clé)"}
    try:
        r = requests.get("https://api.api-ninjas.com/v1/whois", headers={'X-Api-Key': WHOIS_API_KEY}, params={'domain': domain}, timeout=10)
        return r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}"}
    except Exception as e: return {"error": str(e)}

# ─── AFFICHAGE ───────────────────────────────────────────────────────────────
def show_result(title: str, data: dict):
    CLEAR()
    show_banner()
    print(f"\n{PURPLE}╔═══════════════════════════ {title.upper()} ══════════════════════════════════╗{RESET}")
    if isinstance(data, dict) and "error" in data:
        print(f"{PURPLE}║{RESET}  {RED}ERREUR : {data['error']}{RESET}".ljust(88) + f"{PURPLE}║{RESET}")
    else:
        for key, value in data.items():
            line = f"{PURPLE}║{RESET}  {CYAN}{str(key).title().ljust(18)} {RESET}: {WHITE}{value}{RESET}"
            # Nettoyage ANSI pour le calcul de la longueur
            clean_line = re.sub(r'\033\[[0-9;]*m', '', line)
            padding = 80 - len(clean_line)
            print(line + " " * padding + f"{PURPLE}║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n")

def show_db_results(query, results):
    CLEAR()
    show_banner()
    if isinstance(results, dict) and "error" in results:
        print(f"\n{RED}  ERREUR : {results['error']}{RESET}\n")
        return
    print(f"\n{YELLOW}🔍 Résultats pour : {WHITE}'{query}' ({len(results)} trouvés){RESET}\n")
    if not results: print(f"{RED}  Aucun résultat trouvé.{RESET}")
    else:
        for i, res in enumerate(results[:20], 1):
            print(f"{PURPLE}[{i}]{RESET} {GREEN}{res['category']}{RESET} | {CYAN}{res['file']}{RESET}\n    {WHITE}→ {res['content']}{RESET}")
    print(f"\n{PURPLE}╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n")

# ─── MENU PAYS ───────────────────────────────────────────────────────────────
COUNTRIES = [("France", "FR", "33"), ("USA", "US", "1"), ("Canada", "CA", "1"), ("UK", "GB", "44"), ("Allemagne", "DE", "49")]
def select_country():
    print(f"\n{CYAN}Sélectionne un pays :{RESET}")
    for i, (nom, _, code) in enumerate(COUNTRIES, 1): print(f"  {PURPLE}[{i}]{RESET} {nom.ljust(10)} (+{code})")
    while True:
        try:
            choix = input(f"\n{PURPLE}→ {RESET}").strip()
            if not choix: return None
            idx = int(choix) - 1
            if 0 <= idx < len(COUNTRIES): return COUNTRIES[idx]
        except: print(f"{RED}Invalide.{RESET}")

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    animate_banner()
    show_title_animation()
    while True:
        CLEAR()
        show_banner()
        print(f"  {PURPLE}╔══════════════════════════════════ MENU PRINCIPAL ══════════════════════════════════╗{RESET}")
        print(f"  {PURPLE}║{RESET} [01] Phone Lookup       [06] Discord Info       [11] PORT SCANNER         [16] TikTok Info    {PURPLE}║{RESET}")
        print(f"  {PURPLE}║{RESET} [02] Email Lookup       [07] Whois / Site       [12] Dorking Helper       [17] Insta Info     {PURPLE}║{RESET}")
        print(f"  {PURPLE}║{RESET} [03] IP Lookup          [08] DNS Lookup         [13] MAC Lookup           [18] BIN Lookup     {PURPLE}║{RESET}")
        print(f"  {PURPLE}¡{RESET} [04] DATABASE SEARCH    [09] Roblox Info        [14] Threat Intel         [19] VAT Validator  {PURPLE}¡{RESET}")
        print(f"  {PURPLE}¡{RESET} [05] IBAN Validator     [10] Minecraft          [15] Subdomains           [20] CLONE WEBSITE   {PURPLE}¡{RESET}")
        print(f"  {PURPLE}║{RESET} [21] Username Tracker   [22] Server Info        [23] Proxy Check          [24] CLONE SERVER   {PURPLE}║{RESET}")
        print(f"  {PURPLE}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {RED}[q] Quitter{RESET}")
        
        choix = input(f"\n{PURPLE}Cia Hub {CYAN}> {RESET}").strip().lower()
        if choix == 'q': break
        
        if choix in ['1', '01']:
            pays = select_country()
            if pays:
                num = input(f"{CYAN}Numéro : {RESET}").strip()
                show_result(f"PHONE {pays[0]}", phone_lookup(num, pays[2]))
        elif choix in ['2', '02']:
            email = input(f"{CYAN}Email : {RESET}").strip()
            if email: show_result("EMAIL", email_lookup(email))
        elif choix in ['3', '03']:
            ip = input(f"{CYAN}IP (vide = moi) : {RESET}").strip()
            show_result("IP", ip_lookup(ip or None))
        elif choix in ['4', '04']:
            print(f"\n  {PURPLE}[1]{RESET} Recherche standard")
            print(f"  {PURPLE}[2]{RESET} Recherche Regex (Expert)")
            mode = input(f"\n{CYAN}Mode {RESET}> ").strip()
            query = input(f"{YELLOW}Recherche DB : {RESET}").strip()
            if query:
                use_regex = (mode == '2')
                show_db_results(query, db_search(query, use_regex))
        elif choix in ['5', '05']:
            iban = input(f"{CYAN}IBAN : {RESET}").strip()
            if iban: show_result("IBAN", iban_validator(iban))
        elif choix in ['6', '06']:
            uid = input(f"{CYAN}Discord ID : {RESET}").strip()
            if uid: show_result("DISCORD", discord_info(uid))
        elif choix in ['7', '07']:
            dom = input(f"{CYAN}Domaine : {RESET}").strip()
            if dom: show_result("WHOIS", whois_info(dom))
        elif choix in ['8', '08']:
            dom = input(f"{CYAN}Domaine : {RESET}").strip()
            if dom: show_result("DNS", dns_lookup(dom))
        elif choix in ['9', '09']:
            uid = input(f"{CYAN}Roblox ID : {RESET}").strip()
            if uid: show_result("ROBLOX", roblox_info(uid))
        elif choix == '10':
            user = input(f"{CYAN}Minecraft Username : {RESET}").strip()
            if user: show_result("MINECRAFT", minecraft_info(user))
        elif choix == '11':
            target = input(f"{CYAN}IP/Domaine : {RESET}").strip()
            if target: show_result("PORT SCAN", port_scanner(target))
        elif choix == '12':
            print(f"\n{YELLOW}[!] Google Dorks utiles :{RESET}")
            print(f"  {WHITE}site:pastebin.com \"query\"{RESET}")
            print(f"  {WHITE}intitle:\"index of\" \"query\"{RESET}")
            print(f"  {WHITE}filetype:log \"password\"{RESET}")
        elif choix == '13':
            mac = input(f"{CYAN}MAC Address : {RESET}").strip()
            if mac: show_result("MAC LOOKUP", mac_lookup(mac))
        elif choix == '14':
            ip = input(f"{CYAN}IP à analyser : {RESET}").strip()
            if ip: show_result("THREAT INTEL", threat_intel(ip))
        elif choix == '15':
            dom = input(f"{CYAN}Domaine : {RESET}").strip()
            if dom:
                res = subdomain_finder(dom)
                if isinstance(res, list):
                    show_banner()
                    print(f"\n{YELLOW}🔍 Sous-domaines pour {WHITE}{dom} ({len(res)} trouvés) :{RESET}\n")
                    for s in res[:50]: print(f"  {CYAN}→ {WHITE}{s}{RESET}")
                    if len(res) > 50: print(f"\n  {GRAY}... et {len(res)-50} autres.{RESET}")
                else: show_result("SUBDOMAINS", res)
        elif choix == '16':
            user = input(f"{CYAN}TikTok Username : {RESET}").strip()
            if user: show_result("TIKTOK", tiktok_info(user))
        elif choix == '17':
            user = input(f"{CYAN}Instagram Username : {RESET}").strip()
            if user: show_result("INSTAGRAM", instagram_info(user))
        elif choix == '18':
            bin_code = input(f"{CYAN}BIN (6 chiffres) : {RESET}").strip()
            if bin_code: show_result("BIN LOOKUP", bin_lookup(bin_code))
        elif choix == '19':
            vat = input(f"{CYAN}Numéro TVA : {RESET}").strip()
            if vat: show_result("VAT VALIDATOR", vat_validator(vat))
        elif choix == '20':
            url = input(f"{CYAN}URL du site à cloner : {RESET}").strip()
            if url:
                result = clone_website(url)
                show_result("CLONE WEBSITE", result)
        elif choix == '21':
            user = input(f"{CYAN}Username Global : {RESET}").strip()
            if user: show_result("USER TRACKER", username_tracker(user))
        elif choix == '22':
            gid = input(f"{CYAN}ID du Serveur : {RESET}").strip()
            tok = input(f"{CYAN}Ton Token : {RESET}").strip()
            if gid and tok: show_result("SERVER INFO", discord_server_info(gid, tok))
        elif choix == '23':
            ip = input(f"{CYAN}IP à vérifier : {RESET}").strip()
            if ip: show_result("PROXY CHECK", proxy_check(ip))
        elif choix == '24':
            src = input(f"{CYAN}ID du Serveur Source : {RESET}").strip()
            dst = input(f"{CYAN}ID du Serveur Cible : {RESET}").strip()
            token = input(f"{CYAN}Ton Token : {RESET}").strip()
            if src and dst and token:
                res_backup = discord_backup(src, token)
                if "fichier" in res_backup:
                    show_result("CLONAGE EN COURS", discord_load_backup(dst, token, res_backup["fichier"]))
                else:
                    show_result("ERREUR CLONAGE", res_backup)
        
        input(f"\n{GRAY}Appuyez sur Entrée pour revenir...{RESET}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{RED}Fermeture...{RESET}")
