# Introduction

# Préambule

Tout au long de ce document plusieurs notation concernant le cube seront utilisées, cette section a pour but de définir le contexte utile à la bonne compréhension des différents chapitres qui vont suivres.

## Notation rubik's cube

Dans la litérature du cube, la notation du cube est codifier de manière standard par les appelations suivantes : `U(pper), L(eft), F(front), R(ight), B(ack), D(own)` ces différentes lettres correspondent chaucune à une face du cube.

![Décomposition des faces d'un rubik's cube](assets\20210503_223725_image.png)

Les couleurs ne sont pas fixées par rapport aux différentes lettres. Ainsi dans la suite du document et pour la résolution du rubik's cube en fin de traitement, il faudra tenir compte du fait que les mouvements de résolution seront donnés en partant du principe que la face F(ront) est la face rouge (l'élément central doit être rouge) et la face U(pper) est jaune. Une fois que ces deux éléments sont déterminés toutes les autres positions sont fixées ainsi on a que :

* L(eft) : face blue
* R(ight) : face verte
* B(ack) : face orange
* D(own) : face blance

évidemment cela n'est vrai que s'il s'agit d'un rubiks cube standard.

## Etape de conception

L'idée final est de pouvoir analyser le rubik's cube en temps réel (vidéo) afin de detecter les différentes faces et d'y detecter les différentes couleurs associèce aux neuf carrés qui composent une face.

voici les grandes étapes de conception pour la résolution de notre problématique 

* Pré-traiter l'image
* Détection de contours
* Détection de carré
* Détection des couleurs
* Convertion matricielle
* Résolution du rubik's cube

Les "points chauds" sont la détection  de contours et de couleurs qui sont très sensibles aux conditions dans lesquels sont menés les différents tests (condition de luminosité, type de caméra, fish eye, etc...). Il sera donc très difficile de trouver une solution qui sera assez générale pour convenir à tout type de caméra. Nous limiterons donc à l'utilisation de nos caméras intégrées à nos PC portables pour effectuer les tests ainsi que d'une bonne condition lumineuse (typiquement nous ne traitrons pas les cas de basses luminosité).

# Pré-traitement

Le prétraitement des données est une phase importante du traitement d'image, des images de bonnes qualités offre souvent une meilleure angle d'attaque pour entamer un travail en traitement d'image. Dans cette section nous expliquerons tout d'abord comment l'acquisition des images a été réalisé et avec quel type d'images nous avons travaillés tout au long de ce travail pratique avant de passer en phase final sur de la vidéo en temps réel.

## Acquisition des données

Le premier objectif de ce travail a été de constituer un dataset sur lequel travail pour formuler nos premières ébauches de travail, c'est pourquoi nous avons choisi dans premier temps de prendre des images issue

# Conclusion
