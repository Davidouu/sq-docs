---
title: "TroubleShooting & faq"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/fr/trouble_faq)

# TroubleShooting & faq

## Erreurs courantes : causes et solutions
| Code/message | Cause probable |
|--------------|----------------|
| #label_err_occurs# | Problème de connexion au serveur ou erreur de requête. Vérifier la connexion et les paramètres. |
| #label_err_doublon_marque# | Tentative d'ajouter un produit déjà existant. Vérifier les identifiants de produit. |
| #label_err_update# | Erreur lors de la mise à jour des données. Vérifier les permissions et l'intégrité des données. |
| #label_err_insert# | Erreur lors de l'insertion d'un nouveau produit. Vérifier les champs obligatoires. |
| #label_err_delete# | Erreur lors de la suppression d'un produit. Vérifier si le produit est lié à d'autres entités. |

## Questions fréquentes
- **Comment activer le module de gestion des produits offerts ?**
  Pour activer le module, accéder aux paramètres de configuration et activer l'option correspondante.

- **Les produits offerts apparaissent-ils dans le panier du client ?**
  Non, les produits offerts sont ajoutés en arrière-plan et ne sont pas visibles dans le panier.

- **Comment définir les conditions d'éligibilité pour les produits offerts ?**
  Les conditions peuvent être définies dans les paramètres du module, en spécifiant les critères comme la valeur de commande ou le nombre de commandes.

- **Puis-je limiter le nombre de produits offerts par commande ?**
  Oui, il est possible de définir une limite dans les paramètres de configuration du module.

- **Comment gérer les stocks des produits offerts ?**
  Les stocks peuvent être gérés via le module de logistique intégré, en s'assurant que les quantités sont mises à jour lors des commandes.

- **Les nouveaux clients peuvent-ils bénéficier des offres ?**
  Oui, il est possible de définir des offres réservées aux nouveaux clients dans les paramètres.

- **Comment vérifier si un produit est éligible pour une offre ?**
  Utiliser la fonction de vérification d'éligibilité dans le module pour tester les critères définis.

- **Que faire si je rencontre une erreur lors de la mise à jour d'une offre ?**
  Vérifier les messages d'erreur affichés et s'assurer que toutes les données requises sont correctement renseignées.

- **Comment supprimer un produit offert ?**
  Accéder à la liste des produits offerts et utiliser l'option de suppression associée.

- **Puis-je modifier une offre existante ?**
  Oui, il est possible de modifier les détails d'une offre en accédant à la section de gestion des offres.

- **Comment récupérer les informations des produits offerts pour un client spécifique ?**
  Utiliser la fonction `getInfoProduitOffertClient` pour récupérer les données nécessaires.

- **Comment gérer les erreurs de connexion lors de l'utilisation du module ?**
  Vérifier la connexion au serveur et s'assurer que les paramètres de connexion sont corrects.

- **Les produits offerts peuvent-ils être associés à des promotions spécifiques ?**
  Oui, les produits offerts peuvent être liés à des promotions définies dans le système.

- **Comment afficher les détails d'une offre ?**
  Accéder à la section des offres et sélectionner l'offre souhaitée pour afficher ses détails.

- **Quelles sont les meilleures pratiques pour gérer les produits offerts ?**
  S'assurer que les conditions d'éligibilité sont claires, vérifier régulièrement les stocks et mettre à jour les offres en fonction des retours clients.