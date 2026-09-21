# EnForme! 🔥

Coach d'entraînement personnel en PWA (Progressive Web App) : souplesse, force musculaire, et **puissance golf en priorité** — avec le minimum de matériel (tapis, élastique, 2 haltères de 1 kg, vélo elliptique).

100 % local : aucune donnée n'est envoyée à un serveur. Tout est stocké dans le navigateur de l'appareil (`localStorage`), avec export/import JSON pour la sauvegarde et le transfert entre appareils.

## Installation (usage)

### Sur iPhone (Safari)
1. Ouvrir l'URL du site déployé (voir "Déploiement" ci-dessous) dans Safari.
2. Appuyer sur le bouton Partager → **Sur l'écran d'accueil**.
3. L'app s'ouvre ensuite en plein écran, comme une app native.

### Sur Chrome (desktop ou Android)
1. Ouvrir l'URL du site.
2. Cliquer sur l'icône d'installation dans la barre d'adresse (ou menu ⋮ → **Installer l'application**).

### En développement local
La PWA doit être servie en HTTP (le `fetch()` des fichiers JSON échoue en `file://`) :
```bash
cd enforme
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement (GitHub Pages)

1. Pousser ce dossier sur la branche `main` d'un dépôt GitHub.
2. Dans les réglages du dépôt → **Pages** → source : branche `main`, dossier `/ (root)`.
3. Le site est servi en HTTPS à `https://<utilisateur>.github.io/<repo>/` — condition nécessaire pour l'installation PWA sur iPhone.

## Structure du projet

```
enforme/
├── index.html          # Page unique, toutes les vues (menu sandwich + écrans)
├── manifest.json        # Manifest PWA (nom, icônes, couleurs)
├── sw.js                 # Service worker (cache hors-ligne)
├── css/style.css        # Design system (tokens couleur, layout, composants)
├── js/
│   ├── app.js           # Logique applicative : navigation, séances, rendu
│   └── storage.js       # Couche de persistance (localStorage + export/import)
├── data/
│   ├── exercises.json   # Bibliothèque d'exercices (source de vérité)
│   └── programmes.json  # Programmes prédéfinis (enchaînements d'exercices)
└── icons/                # Icônes PWA (192, 512, maskable)
```

## Fonctionnalités (V0)

- **Menu sandwich** (ouverture à droite) : Réglages, Nouvel entraînement, Reprendre un entraînement, Historique, Statistiques.
- **Réglages** : profil du pratiquant (âge, sexe, niveau, blessures, fréquence visée), matériel disponible, curseurs de pondération par objectif (golf en priorité par défaut), export/import JSON, effacement des données.
- **Nouvel entraînement** : choix parmi 5 programmes prédéfinis (Golf Express, Mobilité du matin, Renforcement complet, Cardio fractionné, Stabilité glisse), chacun basé sur les objectifs et le matériel disponible.
- **Séance guidée** : un exercice à la fois (description, consignes, format séries/reps, lien de recherche vidéo YouTube), progression sauvegardée en continu.
- **Reprendre un entraînement** : reprend une séance interrompue exactement où elle s'est arrêtée.
- **Historique** : liste des séances effectuées avec ressenti.
- **Statistiques** : nombre de séances (total, 7 derniers jours), répartition par objectif.

## Contenu des exercices

La bibliothèque V0 (`data/exercises.json`) a été constituée à partir d'une synthèse (reformulée, non copiée) de sources de préparation physique golf et de kinésithérapie sportive (GOLF.com, Denver Golf Fitness, DRVN Golf, Physiophyx, The Prehab Guys, GOWOD, Utah Health, Swyng), croisées avec des méthodes classiques d'étirement et d'entraînement fractionné. Chaque exercice indique le matériel requis, en cohérence avec l'équipement disponible (tapis, élastique, haltères 1 kg, vélo elliptique).

**Vidéos** : pour l'instant, chaque exercice ouvre une recherche YouTube pré-remplie (`videoQuery`) plutôt qu'un lien fixe, pour éviter de pointer vers une vidéo non vérifiée ou qui pourrait disparaître. Une fois vos tutoriels préférés identifiés, il est facile de remplacer `videoQuery` par un lien direct dans `exercises.json`.

## Feuille de route (V1+)

Voir aussi `CLAUDE.md` pour le contexte destiné à un futur développeur (humain ou IA).

- [ ] Minuteur intégré pour les exercices chronométrés (gainage, étirements)
- [ ] Bibliothèque d'exercices consultable librement (hors séance), avec filtres
- [ ] Schémas/illustrations SVG par exercice (en plus des vidéos)
- [ ] Vidéos curées (liens directs vérifiés) pour les exercices prioritaires golf
- [ ] Programmes générés dynamiquement à partir des curseurs d'objectifs du profil (au lieu de programmes fixes)
- [ ] Graphiques de progression plus riches (tendance dans le temps)
- [ ] Rappel/notification locale pour respecter la fréquence hebdomadaire visée
- [ ] Mode sombre/clair automatique (actuellement thème sombre chaud fixe)

## Licence / usage

Projet à usage privé.
