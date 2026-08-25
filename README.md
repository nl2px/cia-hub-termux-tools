# Cia Hub

Outil CLI Python pour Termux et Android, destiné aux recherches OSINT autorisées.

## Fonctionnalités

- Recherche DNS, RDAP/WHOIS et sous-domaines
- Informations publiques sur une adresse IP
- Vérification BIN, IBAN et constructeur MAC
- Informations publiques Roblox et Minecraft
- Vérification de présence publique sur certains réseaux
- Recherche locale dans une base de test anonymisée
- Analyse de ports communs sur une cible autorisée

## Installation sur Termux

```sh
pkg update
```

Ensuite, mets Termux à niveau :

```sh
pkg upgrade
```

Installe Python et Git :

```sh
pkg install python git
```

Télécharge le dépôt :

```sh
git clone https://github.com/nl2px/cia-hub-termux-tools
```

Entre dans le dossier :

```sh
cd cia-hub-termux-tools
```

Crée l’environnement Python :

```sh
python -m venv .venv
```

Active-le :

```sh
source .venv/bin/activate
```

Installe les dépendances :

```sh
pip install -r requirements.txt
```

Lance Cia Hub :

```sh
python Tools.py
```

Pour quitter l’environnement virtuel :

```sh
deactivate
```

## Configuration des API

Les clés sont facultatives. Ne les écrivez jamais dans `Tools.py` et ne les envoyez jamais sur GitHub.

```sh
export PHONE_API_KEY_OMKAR="ta_cle"
```

```sh
export EMAIL_API_KEY="ta_cle"
```

```sh
export WHOIS_API_KEY="ta_cle"
```

```sh
export DISCORD_BOT_TOKEN="ton_token"
```

Puis lance le programme :

```sh
python Tools.py
```

Les variables doivent être redéfinies après l’ouverture d’une nouvelle session Termux. Les services sans clé affichent une erreur explicite et les recherches ne nécessitant pas de clé restent disponibles.

## Publication GitHub

Depuis le dossier du projet :

```sh
git init
```

```sh
git add Tools.py README.md requirements.txt .gitignore DB/README.md
```

```sh
git commit -m "Initial release"
```

```sh
git branch -M main
```

```sh
git remote add origin https://github.com/TON-PSEUDO/cia-hub.git
```

```sh
git push -u origin main
```

## Données et sécurité

Les dossiers `DB/` et `clone_*/` peuvent contenir des données privées ou des pages sensibles. Les fichiers de données sont exclus par `.gitignore`; seul `DB/README.md` est prévu pour le dépôt public.

La copie de sites et la duplication de serveurs Discord sont désactivées dans cette version publique. Utilisez les fonctions réseau uniquement sur vos propres systèmes ou avec une autorisation explicite, en respectant les conditions d’utilisation et la législation locale.

## Dépendances

- `requests`
- `dnspython`
