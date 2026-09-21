# CLAUDE.md — Contexte pour l'évolution du projet EnForme!

Ce fichier est destiné à toute personne (ou instance de Claude) qui reprendrait ce projet plus tard. Il explique les décisions prises, pourquoi, et comment poursuivre sans casser la cohérence de l'ensemble.

## Contexte produit

- **Utilisateur unique**, chef d'entreprise, pratique le golf (objectif prioritaire : puissance du swing), et dans une moindre mesure la voile légère, le kitesurf et le ski. Recherche aussi le maintien de la souplesse et de la force musculaire générale.
- **Matériel disponible, volontairement minimal** : un tapis de gymnastique, un élastique de résistance, deux haltères de 1 kg, un vélo elliptique. **Ne jamais proposer d'exercice nécessitant un autre matériel** sans le signaler explicitement comme optionnel/alternatif.
- Usage **privé**, pas de multi-utilisateur, pas de compte, pas de serveur backend.

## Décisions d'architecture (et pourquoi)

| Décision | Raison |
|---|---|
| PWA en HTML/CSS/JS natif, sans framework | Choix explicite de l'utilisateur (simplicité, maintenabilité, pas de build step) |
| Stockage `localStorage`, pas de backend | Confidentialité (données d'entraînement/santé), simplicité de déploiement (GitHub Pages suffit) |
| Export/import JSON manuel | Fait office de sauvegarde et de synchronisation multi-appareils en l'absence de backend |
| Vidéos = lien de recherche YouTube (`videoQuery`), pas de lien fixe | Aucune vidéo YouTube spécifique n'a été vérifiée comme stable/pérenne lors de la création de V0 ; un lien fixe non vérifié risquerait de pointer vers un contenu erroné ou disparu. À améliorer (voir feuille de route). |
| Palette chaude (braise/orange/or) définie en variables CSS dans `css/style.css` | Demande explicite de l'utilisateur ; **toute nouvelle vue doit réutiliser les tokens existants** (`--flame`, `--gold`, `--bg`, etc.) plutôt que d'introduire de nouvelles couleurs |
| Un seul fichier `app.js` (pas de modules ES / bundler) | Cohérence avec le choix "natif sans build step" ; si le fichier devient trop volumineux, envisager un découpage par vue en gardant le même mécanisme de chargement `<script>` simple (pas de bundler sans en discuter avec l'utilisateur) |

## Modèle de données

### Profil (`Store.getProfile()` / `enforme:profile`)
```js
{
  age: number|null,
  sexe: string,
  niveauForme: "debutant"|"intermediaire"|"avance",
  blessures: string,
  frequenceHebdo: number,
  materielDispo: string[],       // sous-ensemble de ["tapis","elastique","halteres","velo"]
  objectifs: {                   // pondération 0-100, "golf" est prioritaire par défaut
    golf, souplesse, force, voile, kite, ski
  }
}
```

### Exercice (`data/exercises.json`)
Chaque exercice a : `id`, `nom`, `objectifs[]` (parmi les clés d'objectif du profil, `endurance` en plus), `materiel[]`, `niveau`, `categorie`, `description`, `consignes[]`, `series` (texte libre, ex. "3 séries de 10"), `videoQuery`, `source`.

**Pour ajouter un exercice** : l'ajouter dans `data/exercises.json` avec un `id` unique préfixé `ex-`, puis l'inclure dans un ou plusieurs `exercices[]` de `data/programmes.json`. Aucune modification de code n'est nécessaire (le rendu est piloté par les données).

### Programme (`data/programmes.json`)
`id`, `nom`, `objectifPrincipal`, `dureeMin`, `description`, `exercices[]` (liste d'`id` d'exercices, dans l'ordre d'exécution).

### Historique (`Store.getHistory()` / `enforme:history`)
Tableau d'entrées `{ date, programmeId, programmeNom, nbExercices, ressenti }`, la plus récente en premier.

### Séance en cours (`Store.getOngoingSession()` / `enforme:ongoing-session`)
`{ programmeId, programmeNom, startedAt, exerciceIndex, exercices[] }`. Sauvegardée à chaque changement d'exercice, ce qui permet la reprise exacte.

## Conventions de code

- Français pour tout ce qui est visible par l'utilisateur (UI, données) ; identifiants techniques (variables, fonctions, clés JSON) en anglais/français mixte existant, rester cohérent avec l'existant plutôt que de tout renommer.
- Pas de dépendance externe (CDN ou npm) sans en discuter avec l'utilisateur au préalable — le projet doit rester utilisable hors-ligne et sans étape de build.
- Le service worker (`sw.js`) liste explicitement les fichiers de l'app shell dans `APP_SHELL` : **tout nouveau fichier statique ajouté au projet doit être ajouté à cette liste**, sinon il ne sera pas disponible hors-ligne.
- Incrémenter `CACHE_NAME` (ex. `enforme-cache-v2`) à chaque changement de contenu des fichiers mis en cache, pour forcer la mise à jour côté utilisateur.

## Processus de versioning

Chaque évolution significative doit :
1. Être commitée avec un message clair (`feat:`, `fix:`, `data:` pour un changement de contenu d'exercices, `docs:` pour la documentation).
2. Mettre à jour `README.md` si une fonctionnalité visible par l'utilisateur change.
3. Mettre à jour ce fichier (`CLAUDE.md`) si une décision d'architecture ou le modèle de données change.
4. Être poussée vers le dépôt GitHub distant.

## Historique des sessions de développement

- **V0 (initiale)** : scaffolding complet — menu sandwich, réglages avec profil/objectifs/export-import, 5 programmes prédéfinis, 16 exercices (recherche synthétisée), séance guidée avec sauvegarde de progression, historique, statistiques basiques, PWA installable (manifest + service worker), icônes générées.
- **V1.1** : minuteur intégré (`js/timer.js`, trois types de config : `attente`, `intervalle`, `duree` — voir champ `timer` dans `exercises.json`), sans dépendance externe (bip via Web Audio, vibration via `navigator.vibrate`).
- **V1.2** : bibliothèque d'exercices consultable (`view-bibliotheque`), filtrage par objectif/matériel + recherche texte, détail en panneau superposé (`.detail-overlay`). À cette occasion, correction de données : les `objectifs[]` des exercices ne portaient que les tags sport (golf/ski/voile/kite), sans `souplesse`/`force`/`endurance` — corrigé via une règle `categorie → objectif` dans `tools/generate_diagrams.py`'s voisin (voir historique git) pour rester cohérent avec les curseurs du profil.
- **V1.3** : pictogrammes SVG par exercice (`js/diagrams.js`, généré par `tools/generate_diagrams.py`). Convention : trait or = posture, trait flamme = segment qui travaille, pointillés = élastique/trajectoire. **Ne pas éditer `js/diagrams.js` à la main** : modifier les coordonnées dans le script Python et relancer `python3 tools/generate_diagrams.py`, pour garder les deux fichiers synchronisés.

## Notes techniques utiles pour la suite

- Pour prévisualiser tous les pictogrammes en une planche contact (utile après une modification de `tools/generate_diagrams.py`) : le script peut être appelé puis son JSON extrait et rendu en PNG via `cairosvg` (`pip install cairosvg --break-system-packages`). Voir la session de développement V1.3 dans l'historique git pour un exemple de script de planche contact.
- Le service worker doit voir son `CACHE_NAME` incrémenté (`v3`, `v4`, ...) à chaque ajout/modification de fichier statique, sans quoi les utilisateurs ayant déjà installé la PWA garderont une version en cache.

## Idées explorées puis écartées (pour éviter de les reproposer sans raison)

- **React/framework** : écarté car l'utilisateur a choisi explicitement le natif HTML/CSS/JS.
- **Liens vidéo YouTube fixes dans V0** : écarté faute de pouvoir vérifier la validité/pérennité de vidéos spécifiques au moment de la création ; remplacé par un lien de recherche. À revisiter si l'utilisateur valide des vidéos précises.
