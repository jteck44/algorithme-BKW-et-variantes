# PROJET DE SCIENCE DE L'INFORMATION
# Mission BKW - Laboratoire d'Algorithmes Cryptographiques
  

Une application éducative interactive pour explorer et comprendre les algorithmes BKW (Blum-Kalai-Wasserman) appliqués aux problèmes cryptographiques LPN (Learning Parity with Noise) et LWE (Learning With Errors).

## 📋 Table des Matières

- [À Propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture du Projet](#-architecture-du-projet)
- [Algorithmes Implémentés](#-algorithmes-implémentés)
- [Documentation Technique](#-documentation-technique)
- [Contribuer](#-contribuer)
- [Références](#-références-académiques)
- [Licence](#-licence)

## 🎯 À Propos

**Mission BKW** est un outil pédagogique interactif conçu pour l'apprentissage et l'expérimentation des algorithmes de cryptanalyse BKW. Il offre une interface graphique moderne permettant de visualiser en temps réel le processus de résolution des problèmes LPN et LWE, qui sont fondamentaux en cryptographie post-quantique.

### Objectifs Pédagogiques

- 📚 Comprendre les problèmes LPN et LWE
- 🔍 Explorer différentes variantes de l'algorithme BKW
- 📊 Visualiser l'exécution étape par étape
- 🎓 Comparer les performances des algorithmes
- 🧪 Expérimenter avec des paramètres personnalisés

## ✨ Fonctionnalités

### Interface Utilisateur

- 🎨 **Interface moderne et intuitive** avec design sombre
- 📱 **Design responsive** s'adaptant à différentes tailles d'écran
- 🔄 **Navigation fluide** entre les différents écrans
- 📊 **Console d'exécution** avec logs colorés en temps réel
- 📈 **Barre de progression** pour suivre l'avancement

### Missions Prédéfinies

1. **Formation - Initiation** : Secret 8 bits, bruit faible (τ=0.1)
2. **Opération Standard** : Secret 12 bits, bruit moyen (τ=0.15)
3. **Mission LWE Avancée** : Dimension 8, modulus 31, σ=1.5
4. **Défi Expert** : Secret 16 bits, bruit élevé (τ=0.2)
5. **Cryptanalyse LWE Moderne** : Dimension 12, modulus 31, σ=1.2

### Configuration Personnalisée

- ⚙️ **Paramètres ajustables** : dimension, bruit, structure des blocs
- 🔑 **Secret personnalisé** : définissez votre propre secret à retrouver
- 🎲 **Génération aléatoire** de secrets
- 🔄 **Support LPN et LWE** avec paramètres adaptés

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des Dépendances
```bash
# Cloner le repository
git clone https://github.com/votre-username/mission-bkw.git
cd mission-bkw

# Installer les dépendances
pip install -r requirements.txt
```

### Fichier requirements.txt
```
numpy>=1.21.0
```

**Note** : Tkinter est généralement inclus avec Python. Si vous rencontrez des problèmes :
```bash
# Sur Ubuntu/Debian
sudo apt-get install python3-tk

# Sur macOS (avec Homebrew)
brew install python-tk

# Sur Windows
# Tkinter est inclus par défaut avec Python
```

## 💻 Utilisation

### Démarrage Rapide
```bash
python main.py
```

### Guide d'Utilisation

#### 1. Écran Principal

Au lancement, vous accédez au menu principal avec deux onglets :

- **🎯 Missions Prédéfinies** : Choisissez parmi 5 scénarios préconfigurés
- **⚙️ Configuration** : Créez vos propres configurations

#### 2. Sélection d'une Mission

Cliquez sur "SÉLECTIONNER" sous une mission pour afficher ses détails et passer à l'écran de sélection d'algorithme.

#### 3. Choix de l'Algorithme

Sélectionnez l'algorithme adapté à votre mission :

**Pour LPN** :
- BKW Standard
- LF1 (Walsh-Hadamard)

**Pour LWE** :
- BKW-LWE
- LMS-BKW
- CODED-BKW
- CODED-BKW + Sieving

#### 4. Exécution

L'algorithme s'exécute automatiquement. Vous pouvez suivre :
- 📊 La progression via la barre de progression
- 📝 Les logs détaillés dans la console
- ⏱️ Les étapes en temps réel

#### 5. Résultats

À la fin, comparez :
- Le secret réel vs le secret trouvé
- Le taux de précision
- Les recommandations d'amélioration

### Configuration Personnalisée

#### Définir Vos Paramètres

1. Allez dans l'onglet "⚙️ Configuration"
2. Cliquez sur "Mission Paramétrée"
3. Configurez :
   - Type de problème (LPN/LWE)
   - Dimension du secret
   - Niveau de bruit
   - Structure des blocs (a × b)

#### Définir Votre Secret

1. Cliquez sur "Définir Mon Secret"
2. Choisissez le type (LPN/LWE)
3. Entrez la taille
4. Saisissez votre secret :
   - **LPN** : Format binaire (ex: `10101101`)
   - **LWE** : Format modulaire (ex: `3,5,2,7`)
5. Ou cliquez sur "🎲 Générer Aléatoire"

## 📁 Architecture du Projet
```
mission-bkw/
│
├── main.py                      # Point d'entrée de l'application
│
├── core/                        # Modules fondamentaux
│   ├── __init__.py
│   ├── lpn.py                   # Génération d'instances LPN
│   ├── lwe.py                   # Génération d'instances LWE
│   └── utils.py                 # Fonctions utilitaires
│
├── weapons/                     # Implémentations des algorithmes
│   ├── __init__.py
│   ├── bkw_standard.py          # BKW Standard pour LPN
│   ├── bkw_lf1.py              # LF1 avec Walsh-Hadamard
│   ├── bkw_lwe.py              # BKW adapté pour LWE
│   ├── lms_bkw.py              # LMS-BKW (réduction de modulus)
│   ├── coded_bkw.py            # CODED-BKW (codes linéaires)
│   └── coded_bkw_sieving.py    # CODED-BKW avec sieving
│
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
└── LICENSE                      # Licence MIT
```

### Description des Modules

#### `core/`

**`lpn.py`**
- Classe `LPNInstance` pour générer des instances du problème LPN
- Génération de secrets binaires aléatoires
- Création d'échantillons avec bruit de Bernoulli

**`lwe.py`**
- Classe `LWEInstance` pour générer des instances du problème LWE
- Génération de secrets modulaires
- Création d'échantillons avec bruit gaussien discret

**`utils.py`**
- Fonctions de manipulation de vecteurs (XOR, addition/soustraction modulaire)
- Calcul du poids de Hamming
- Transformée de Walsh-Hadamard
- Fonctions de vraisemblance gaussienne

#### `weapons/`

Implémentations des différents algorithmes BKW, organisées par héritage :
```
BKWStandard (base LPN)
    └── BKWLF1 (Walsh-Hadamard)

BKWLWE (base LWE)
    ├── LMSBKW (réduction de modulus)
    └── CodedBKW (codes linéaires)
        └── CodedBKWSieving (sieving)
```

## 🔬 Algorithmes Implémentés

### Pour LPN (Learning Parity with Noise)

#### 1. BKW Standard

**Principe** : Algorithme classique utilisant la réduction par blocs et le vote majoritaire.

**Complexité** : O(2^(b·a))

**Phases** :
1. **Réduction** : Groupement d'échantillons par blocs et XOR
2. **Résolution** : Vote majoritaire sur échantillons de poids 1
3. **Substitution arrière** : Élimination de la contribution des bits trouvés

**Cas d'usage** : Idéal pour comprendre les bases de BKW

#### 2. LF1 (Walsh-Hadamard)

**Principe** : Utilise la transformée de Walsh-Hadamard pour une résolution plus efficace.

**Amélioration** : Réduit la complexité en exploitant les propriétés de la transformée

**Avantage** : Meilleure performance que BKW standard, surtout pour de petites dimensions

### Pour LWE (Learning With Errors)

#### 3. BKW-LWE

**Principe** : Adaptation de BKW avec vraisemblance gaussienne au lieu du vote majoritaire.

**Spécificités** :
- Test d'hypothèse basé sur la log-vraisemblance
- Gestion du bruit gaussien accumulé
- Réduction modulaire pour les collisions

**Complexité** : O(q^d · m) où d est le nombre de composantes non nulles autorisées

#### 4. LMS-BKW (Lazy Modulus Switching)

**Principe** : Réduit le modulus q pour diminuer la complexité.

**Processus** :
1. Conversion Z_q → Z_p (p < q)
2. Réduction BKW dans Z_p
3. Reconversion Z_p → Z_q

**Avantage** : Efficace pour les grands modulus

#### 5. CODED-BKW

**Principe** : Intègre des codes linéaires pour accélérer la réduction.

**Méthode** :
- Étapes BKW standard (t1)
- Étapes codées avec codes linéaires (t2)
- Mapping vers mots de code proches

**Amélioration** : Réduit plus de positions par étape

#### 6. CODED-BKW + Sieving

**Principe** : Combine codes linéaires et tamisage pour contrôler la norme.

**Processus** :
1. CodeMap standard
2. Sieving : combinaison d'échantillons pour réduire la norme
3. Filtrage par borne B sur la norme

**Avantage** : État de l'art pour LWE difficile

## 📖 Documentation Technique

### Génération d'Instances

#### LPN
```python
from core.lpn import LPNInstance

# Génération automatique du secret
instance = LPNInstance(k=12, tau=0.15)

# Avec secret personnalisé
secret = [1, 0, 1, 1, 0, 0, 1, 0]
instance = LPNInstance(k=8, tau=0.1, secret=secret)

# Générer des échantillons
samples = instance.generate_samples(1000)
```

#### LWE
```python
from core.lwe import LWEInstance

# Génération automatique
instance = LWEInstance(n=8, q=31, sigma=1.5)

# Avec secret personnalisé
secret = [3, 5, 2, 7, 1, 4, 6, 0]
instance = LWEInstance(n=8, q=31, sigma=1.5, secret=secret)

# Générer des échantillons
samples = instance.generate_samples(500)
```

### Utilisation des Algorithmes

#### BKW Standard (LPN)
```python
from weapons.bkw_standard import BKWStandard

params = {
    'k': 12,      # Dimension
    'tau': 0.15,  # Bruit
    'a': 3,       # Nombre de blocs
    'b': 4        # Taille de bloc
}

def log_callback(message, msg_type='info'):
    print(f"[{msg_type}] {message}")

algorithm = BKWStandard(params, log_callback)
found_secret = algorithm.solve(samples, true_secret=secret)
```

#### BKW-LWE
```python
from weapons.bkw_lwe import BKWLWE

params = {
    'n': 8,
    'q': 31,
    'sigma': 1.5,
    'a': 2,
    'b': 4
}

algorithm = BKWLWE(params, log_callback)
found_secret = algorithm.solve(samples, true_secret=secret)
```

### Fonctions Utilitaires
```python
from core.utils import (
    hamming_weight,
    xor_vectors,
    mod_subtract,
    walsh_hadamard_transform,
    log_likelihood
)

# Poids de Hamming
weight = hamming_weight([1, 0, 1, 1, 0])  # Retourne 3

# XOR de vecteurs
result = xor_vectors([1, 0, 1], [0, 1, 1])  # [1, 1, 0]

# Soustraction modulaire
result = mod_subtract([5, 3, 7], [2, 1, 4], q=31)  # [3, 2, 3]

# Walsh-Hadamard
f = [1, -1, 1, 1]
f_hat = walsh_hadamard_transform(f)

# Log-vraisemblance
score = log_likelihood(error=2, sigma=1.5, q=31)
```

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment vous pouvez aider :

### Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé
2. Ouvrez une issue avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs observé
   - Captures d'écran si pertinent
   - Environnement (OS, version Python)

### Proposer une Fonctionnalité

1. Ouvrez une issue de type "Feature Request"
2. Décrivez la fonctionnalité souhaitée
3. Expliquez le cas d'usage
4. Proposez une implémentation si possible

### Soumettre du Code

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de Code

- Suivre PEP 8 pour le style Python
- Ajouter des docstrings pour les nouvelles fonctions
- Commenter le code complexe
- Tester les modifications avant de soumettre

## 📚 Références Académiques

- Blum, A., Kalai, A., & Wasserman, H. (2003). "Noise-tolerant learning, the parity problem, and the statistical query model"
- Regev, O. (2005). "On lattices, learning with errors, random linear codes, and cryptography"
- Albrecht, M., Cid, C., Faugère, J. C., & Perret, L. (2014). "On the complexity of the BKW algorithm on LWE"
- Kirchner, P., & Fouque, P. A. (2015). "An improved BKW algorithm for LWE with applications to cryptography and lattices"

## 🙏 Remerciements

- Les algorithmes sont basés sur les travaux de recherche académique en cryptographie
- Interface inspirée par les standards modernes de design
- Merci à la communauté Python et Tkinter

## 📝 Notes de Version

### v1.0.0 (Janvier 2025)

**Fonctionnalités** :
- ✅ 6 algorithmes BKW implémentés
- ✅ Support LPN et LWE
- ✅ Interface graphique moderne
- ✅ 5 missions prédéfinies
- ✅ Configuration personnalisée
- ✅ Logs en temps réel
- ✅ Analyse détaillée des résultats

**Améliorations futures** :
- 📊 Export des résultats en CSV
- 📈 Graphiques de performance
- 🎨 Thèmes personnalisables
- 🌐 Support multilingue
- 📱 Version web

---

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile sur GitHub !**