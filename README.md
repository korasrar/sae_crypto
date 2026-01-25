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

Le serveur démarre par défaut sur le port `15001`.

#### 2. Connecter les clients

Sur chaque machine des joueurs :

```bash
python -m client.client.py
```

Le client se connecte par défaut à `localhost:15001`. Dans une future version, le choix serra donner, modifier dans les fichiers si besoin

## 🎯 Commandes du jeu

### Format des coups

Les coups doivent être entrés au format UCI (Universal Chess Interface) :
- `e2e4` : Déplace la pièce de e2 vers e4
- `e2 e4` : Format alternatif accepté

### Commandes réseau (client)

| Commande | Description |
|----------|-------------|
| `register <nom> <mdp>` | Créer un nouveau compte (nom: 3-10 caractères, mdp: 6+ caractères) |
| `connect <nom> <mdp>` | Se connecter à un compte existant |
| `play` | Rejoindre la file d'attente pour une partie |
| `leave` | Quitter la file d'attente |
| `quit` | Se déconnecter |
| `replay` | Demander une revanche |
| `new` | Chercher une nouvelle partie |

## 📁 Structure du projet

```
sae_crypto/
├── chess/
│   └── game.py         # Logique du jeu et menu principal
├── client/
│   └── client.py       # Client réseau
├── serveur/
│   └── serveur.py      # Serveur multijoueur
├── BD.sql              # Schéma de la base de données
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
