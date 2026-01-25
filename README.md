# sae_crypto

Jeu d'échecs en Python | Affichage terminal | Partie locale ou en réseau | 2 Joueurs

## 📋 Description

Ce projet est un jeu d'échecs développé en Python avec les fonctionnalités suivantes :
- **Partie locale** : Deux joueurs sur le même ordinateur
- **Partie en réseau** : Deux joueurs sur des machines différentes via un serveur
- **Affichage terminal** : Interface en ligne de commande avec représentation Unicode du plateau

## 🔧 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## 📦 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/korasrar/sae_crypto.git
cd sae_crypto
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🎮 Lancement du jeu

### Mode local (2 joueurs sur le même PC)

```bash
python chess/game.py
```

Puis sélectionnez l'option `1: Partie Locale` dans le menu.

### Mode réseau

#### 1. Démarrer le serveur

```bash
python -m serveur.serveur.py
```

Le serveur vous demandera de choisir un port sur lequel écouter

#### 2. Connecter les clients

Sur chaque machine des joueurs :

```bash
python -m client.client.py
```

Le client vous demandera d'entrer l'adresse ip et le port du serveur sur lequel il veut se connecter (vous pouvez entrer localhost pour l'ip)
Le port doit être celui sur lequel le serveur écoute

## 🎯 Commandes du jeu

### Format des coups

Les coups doivent être entrés au format UCI (Universal Chess Interface) :
- `e2e4` : Déplace la pièce de e2 vers e4
- `e2 e4` : Format alternatif accepté

### Commandes réseau (client)

| Commande | Description |
|----------|-------------|
| `register <nom> <mdp>` | Créer un nouveau compte |
| `connect <nom> <mdp>` | Se connecter à un compte existant |
| `new` | Chercher une nouvelle partie (mise en file d'attente) |
| `leave` | Abandonner / quitter la partie en cours |
| `replay` | Demander une revanche |

### Commandes en partie (quand c'est votre tour)

| Commande | Description |
|----------|-------------|
| `move <src> <dst>` | Jouer un coup (ex: `move e2 e4`) |
| `move <src><dst>` | Variante compacte (ex: `move e2e4`) |
| `promote <src> <dst> <piece>` | Promotion (ex: `promote a7 a8 q`) |
| `promote <src><dst> <piece>` | Variante compacte (ex: `promote a7a8 q`) |
| `legal` | Afficher les coups légaux |
| `board` | Afficher le plateau |
| `resign` | Abandonner la partie |
| `replay` | Demander une revanche |
| `quit` | Quitter la partie |
| `help` | Ré-afficher l'aide |

## 📁 Structure du projet

```
sae_crypto/
├── chess/
│   ├── game.py          # Logique du jeu et menu principal
│   └── display_game.py  # Affichage (console)
├── client/
│   └── client.py       # Client réseau
├── crypto/
│   ├── __init__.py
│   ├── aes.py
│   └── diffie_hellman.py
├── serveur/
│   └── serveur.py      # Serveur multijoueur
├── BD.sql              # Schéma de la base de données
├── echecs.db            # Base de données SQLite
├── models.py            # Modèles SQLAlchemy
├── tests/
│   └── test_client_minimal.py
├── requirements.txt    # Dépendances Python
└── README.md
```

## 📚 Dépendances principales

| Package | Version | Description |
|---------|---------|-------------|
| `chess` | 1.11.2 | Bibliothèque Python pour la gestion des règles d'échecs |

## 🗄️ Base de données

Le fichier `BD.sql` contient le schéma pour stocker :
- **JOUEUR** : Informations des joueurs (pseudo, mot de passe)
- **PARTIE** : Historique des parties jouées
- **COUP** : Informations d'un coup
- **STATISTIQUES** : Stats des joueurs (victoires, défaites, nulles)

## 🛠️ Configuration

- Les informations du **serveur** et du **client** sont demandé au lancement du jeu

## 📖 Documentation / Sources

- Threading et Lock en Python :  
  <https://stackoverflow.com/questions/10525185/python-threading-how-do-i-lock-a-thread>
- Bibliothèque python-chess :  
  <https://python-chess.readthedocs.io/>

## 👥 Auteurs

- FOUCHER Matteo
- COSME VINOU Ilona
- MAUBERT Célestin
- HUCHE River

## 📄 Licence

Projet universitaire
