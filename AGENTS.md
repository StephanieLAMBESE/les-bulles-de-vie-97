# Instructions de maintenance

Ce dépôt héberge le site vitrine statique de l'association Les Bulles de Vie 97, publié sur Netlify depuis la branche `main`.

## Principes d'édition

- Conserver le français comme langue principale du site.
- Préserver un HTML sémantique, une navigation au clavier fonctionnelle et des contrastes lisibles.
- Ajouter un texte alternatif pertinent à chaque image informative.
- Mettre à jour le titre, la meta description et les données structurées lorsqu'une évolution majeure du contenu le justifie.
- Optimiser les images avant leur ajout dans `assets/` et éviter les fichiers inutilement lourds.
- Ne pas introduire de dépendance ou de système de build sans besoin explicite.

## Avant publication

Suivre la checklist de `docs/local/runbook.md`, notamment la vérification des coordonnées, liens, affichage mobile et du déploiement Netlify.

## Documentation de fin de tâche

À la fin de chaque tâche, mettre à jour la documentation qui décrit le changement réalisé, en priorité `docs/local/runbook.md`. Y consigner les décisions prises, les éléments restants à faire et les vérifications effectuées, afin que le suivi du projet reste fiable.

## Informations sensibles

Ne jamais enregistrer dans ce dépôt de clés, mots de passe, exports contenant des données personnelles ou notes internes. Les notes locales peuvent être placées dans `docs/local/` ou `docs/private/`, qui ne sont pas versionnés.
