# Animations d'algèbre

Ce projet est un ensemble de plusieurs animations courtes pour visualiser des notions de base de l'algèbre linéaire.

L'objectif est d'aider à donner une intuition pour mieux comprendre ces objets mathématiques.

#### Avertissement : ce projet est en cours de développement.

## Sommaire

[Installation](#installation)

[Liste des animations](#animations)

## Installation<a name="installation"></a>

Les animations se font grâce à la librairie [ManimCommunity](https://github.com/ManimCommunity/manim).

Il faut d'abord suivre leur tutoriel pour installer Manim.

Il suffit ensuite de télécharger le code des animations et d'utiliser la commande :

```
manim -pqm fichier.py
```

pour générer l'animation correspondant au fichier "fichier.py".

Ici `qm` donne une qualité moyenne. Pour générer plus rapidement l'animation (pour les tests notamment) il est adapté d'utilisé `ql` pour une plus basse qualité.

Pour le rendu final, on peut choisir parmi `qh` ou `qk` pour avoir une qualité optimale.

Exemple :

```
manim -pql det.py
```

## Liste des animations <a name="animations"></a>

Les vidéos des animations terminées sont dans le dossier "videos".

- [x] Déterminant

![Déterminant1](https://github.com/NilsCt/animations-algebre/blob/main/images/det1.png)

![Déterminant2](https://github.com/NilsCt/animations-algebre/blob/main/images/det2.png)

- [ ] Vecteurs propres (en cours)
