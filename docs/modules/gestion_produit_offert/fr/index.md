---
title: "Index de la Documentation Technique"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/fr/index)

# Index de la Documentation Technique

## 1. Gestion du Produit Offert
- **Description du Module** : Présentation des fonctionnalités du module `gestion_produit_offert`.
- **Concepts Clés** : Définitions des termes essentiels comme "produit offert", "conditions d'éligibilité", et "logistique".
- **Entités** : Détails sur l'entité `ProduitOffert` et ses champs.

## 2. Fonctions
- **getPourClient** : Récupération des informations spécifiques au type de client.
- **doselMultiple** : Placeholder pour une fonctionnalité à définir.
- **getlivreur_id** : Récupération de l'identifiant du livreur.
- **checkdate** : Vérification de la validité d'une date.

## 3. Requêtes
- **deleteOffreClient** : Suppression d'une offre client existante.
- **insert_produit_offert** : Insertion d'un produit offert dans la base de données.
- **getInfoProduitOffertClient** : Récupération des informations des produits offerts pour un client spécifique.
- **insClient** : Insertion d'un nouveau client dans la base de données.
- **getGroupeClient** : Récupération des groupes de clients associés à un produit offert.
- **getLivreursNom** : Récupération des noms des livreurs associés aux produits offerts.
- **pays_livre** : Récupération des pays de livraison disponibles pour les produits offerts.
- **getCat** : Récupération des catégories de produits disponibles.
- **getOffre** : Récupération des offres disponibles pour les produits offerts.

## 4. Dépendances
- **allow_update.cfm** : Gestion des mises à jour des offres de produits.
- **qry_get_offre.cfm** : Récupération des offres de produits.
- **qry_get_langues.cfm** : Récupération des langues disponibles.
- **qry_get_cat.cfm** : Récupération des catégories de produits.
- **qry_get_all_type_produit.cfm** : Récupération de tous les types de produits.
- **qry_get_all_partners.cfm** : Récupération de tous les partenaires.
- **qry_verif_produit.cfm** : Vérification de l'existence d'un produit.
- **dsp_offre.cfm** : Affichage des détails des offres de produits.
- **dsp_offre_form.cfm** : Gestion du formulaire d'ajout ou de modification d'une offre.
- **dsp_offre_search.cfm** : Gestion de la recherche d'offres de produits.
- **dsp_offre_header.cfm** : Affichage de l'en-tête de la page des offres.
- **dsp_offre_footer.cfm** : Affichage du pied de page de la page des offres.
- **ajax/getTypeClient.cfm** : Gestion de la sélection du type de client.
- **index.cfm** : Point d'entrée principal pour le module.
- **err_offre_entry.cfm** : Gestion des erreurs lors de l'entrée des offres.
- **_insert_goodies_xerox_ne_pas_toucher_alain.cfm** : Insertion des goodies dans le panier.

## 5. Gestion d'Erreurs
- **Mise à jour d'un produit offert** : Gestion des erreurs de mise à jour.
- **Insertion d'un produit offert** : Gestion des erreurs d'insertion.
- **Suppression d'un produit offert** : Gestion des erreurs de suppression.

## 6. Interface
- **dsp_offre.cfm** : Affichage des offres de produits.
- **dsp_offre_form.cfm** : Gestion de l'ajout et de la modification des produits offerts.
- **dsp_offre_search.cfm** : Recherche de produits offerts.
- **act_offre.cfm** : Gestion des actions sur les offres.

## 7. Requêtes AJAX
- **getTypeClient** : Récupération de la liste des groupes de clients.
- **getLivreur** : Chargement de la liste des livreurs.
- **index** : Gestion des actions AJAX.

## 8. Logique Métier
- **Logiques name** : Conditions d'éligibilité pour l'ajout de produits offerts.

Ce plan d'indexation permet une navigation rapide et efficace dans la documentation technique du module `gestion_produit_offert` de Solusquare Commerce Cloud.