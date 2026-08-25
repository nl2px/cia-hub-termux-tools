# Cia Hub OSINT

Outil CLI Python pour Termux et Android, destiné aux recherches OSINT autorisées : DNS, RDAP/WHOIS, IP, sous-domaines, BIN, IBAN, MAC, Roblox, Minecraft et vérification de présence publique.

## Installation Termux

```sh
pkg update
pkg install python git
git clone <URL_DU_DEPOT>
cd "Cia Hub - Tools Osint2026"
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python Tools.py
```

Sur Termux, utilisez `python` et non `python3` si votre installation ne fournit pas ce dernier alias.

## Clés API facultatives

Ne mettez jamais de clé dans le code ni dans GitHub. Configurez seulement les services souhaités dans le shell Termux :

```sh
export PHONE_API_KEY_OMKAR="..."
export EMAIL_API_KEY="..."
export WHOIS_API_KEY="..."
export DISCORD_BOT_TOKEN="..."
```

Les clés absentes désactivent proprement le service concerné. Un fichier `.env` local est également ignoré par Git.

## Limites de sécurité

La copie de sites et la duplication de serveurs Discord sont désactivées dans la version publique : ces fonctions peuvent servir à l’usurpation, au phishing ou à l’accès non autorisé. N’ajoutez pas les dossiers `clone_*` ou `DB/` à un dépôt public ; ils sont exclus par `.gitignore` et peuvent contenir des données ou des pages sensibles.

Utilisez les fonctions réseau uniquement sur des cibles vous appartenant ou avec une autorisation explicite. Respectez les conditions d’utilisation des services consultés et les lois locales.

## Dépendances

- `requests`
- `dnspython`
