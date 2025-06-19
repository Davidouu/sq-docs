# TroubleShooting & faq

## Erreurs courantes : causes et solutions

| Code/message                         | Cause probable                                                                                   |
|------------------------------------|------------------------------------------------------------------------------------------------|
| Erreur lors de l'insertion d'attribut | Données manquantes ou mal formatées, doublon d'attribut, problème de connexion à la base         |
| Erreur lors de la suppression d'attribut | L’attribut est encore lié à des types de produits ou options, ou identifiant incorrect           |
| Erreur lors de la mise à jour d'attribut | Libellés incomplets dans certaines langues, données invalides, problème de transaction          |
| Erreur lors de la mise à jour des options d'attribut | Libellés manquants, code couleur invalide, problème de synchronisation multilingue               |
| Couleur non prise en compte ou invalide | Saisie incorrecte du code couleur (doit être au format ##XXXXXX), absence de validation visuelle  |
| Attribut non visible sur fiche produit | Attribut non associé au type de produit concerné ou statut inactif                              |
| Impossible d’associer un attribut à un type de produit | Identifiant erroné ou association déjà existante                                                |
| Recherche d’attribut ne retourne rien | Critères trop restrictifs ou données non encore créées                                         |
| Message d’erreur « Valeur obligatoire manquante » | Champs obligatoires non remplis (ex : types de produits associés, libellés multilingues)        |
| Problème d’affichage multilingue | Libellés non renseignés dans toutes les langues actives                                         |

## Questions fréquentes

- **Comment créer un nouvel attribut produit ?**  
  Remplir les libellés dans toutes les langues actives, sélectionner au moins un type de produit associé, puis valider le formulaire d’ajout.

- **Puis-je associer un même attribut à plusieurs types de produits ?**  
  Oui, il est possible d’associer un attribut à plusieurs types de produits pour une exploitation commune.

- **Comment modifier un attribut existant ?**  
  Utiliser le formulaire d’édition pour mettre à jour les libellés, le code externe, et les options comme le filtre ou la couleur.

- **Comment supprimer un attribut ?**  
  Supprimer l’attribut uniquement s’il n’est plus associé à aucun type de produit ni utilisé dans les fiches produits.

- **Que signifie un attribut marqué comme « filtre » ?**  
  Cela indique que l’attribut peut être utilisé pour affiner la recherche produit via des filtres.

- **Comment gérer les options d’un attribut ?**  
  Accéder au formulaire d’édition des options pour ajouter, modifier ou supprimer les valeurs possibles, avec leurs libellés multilingues.

- **Comment saisir une couleur pour une option d’attribut ?**  
  Entrer un code couleur au format hexadécimal avec un double dièse, par exemple `##FF0000`. La saisie est validée automatiquement.

- **Que faire si la couleur saisie n’est pas acceptée ?**  
  Vérifier le format du code couleur, corriger la saisie ou laisser vide pour revenir à la couleur noire par défaut.

- **Comment gérer les groupes de couleurs ?**  
  Créer et modifier des groupes de couleurs via l’interface dédiée, puis les associer aux options d’attributs couleur.

- **Pourquoi un attribut n’apparaît-il pas dans la liste des attributs ?**  
  Vérifier les critères de recherche, le statut de l’attribut, et son association aux types de produits.

- **Peut-on créer un attribut sans libellé dans toutes les langues ?**  
  Non, il est obligatoire de renseigner les libellés dans toutes les langues actives pour assurer une cohérence multilingue.

- **Comment gérer l’ordre d’affichage des attributs ?**  
  L’ordre est défini par un champ de tri lors de l’association de l’attribut aux types de produits.

- **Est-il possible d’avoir des attributs spécifiques à un pays ?**  
  Oui, chaque attribut est lié à un pays d’application, ce qui permet une gestion localisée.

- **Comment éviter les doublons d’attributs ?**  
  Le système vérifie les doublons lors de la création et affiche un message d’erreur si un attribut similaire existe déjà.

- **Comment rechercher un attribut spécifique ?**  
  Utiliser le formulaire de recherche en filtrant par pays, type de produit ou nom d’attribut pour affiner les résultats.

- **Que faire en cas d’erreur technique lors d’une opération ?**  
  Un message d’erreur s’affiche, et une notification est envoyée aux équipes techniques pour analyse. Contacter le support si nécessaire.