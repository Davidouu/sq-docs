---
title: "Technical Documentation Index"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/en/index)

# Technical Documentation Index

## 1. Management of Offered Product
- **Module Description**: Overview of the features of the `gestion_produit_offert` module.
- **Key Concepts**: Definitions of essential terms such as "offered product", "eligibility conditions", and "logistics".
- **Entities**: Details about the `ProduitOffert` entity and its fields.

## 2. Functions
- **getPourClient**: Retrieval of information specific to the type of client.
- **doselMultiple**: Placeholder for a feature to be defined.
- **getlivreur_id**: Retrieval of the deliverer's ID.
- **checkdate**: Validation of a date.

## 3. Queries
- **deleteOffreClient**: Deletion of an existing client offer.
- **insert_produit_offert**: Insertion of an offered product into the database.
- **getInfoProduitOffertClient**: Retrieval of information on offered products for a specific client.
- **insClient**: Insertion of a new client into the database.
- **getGroupeClient**: Retrieval of client groups associated with an offered product.
- **getLivreursNom**: Retrieval of the names of deliverers associated with offered products.
- **pays_livre**: Retrieval of available delivery countries for offered products.
- **getCat**: Retrieval of available product categories.
- **getOffre**: Retrieval of available offers for offered products.

## 4. Dependencies
- **allow_update.cfm**: Management of product offer updates.
- **qry_get_offre.cfm**: Retrieval of product offers.
- **qry_get_langues.cfm**: Retrieval of available languages.
- **qry_get_cat.cfm**: Retrieval of product categories.
- **qry_get_all_type_produit.cfm**: Retrieval of all product types.
- **qry_get_all_partners.cfm**: Retrieval of all partners.
- **qry_verif_produit.cfm**: Verification of the existence of a product.
- **dsp_offre.cfm**: Display of product offer details.
- **dsp_offre_form.cfm**: Management of the add or modify offer form.
- **dsp_offre_search.cfm**: Management of product offer search.
- **dsp_offre_header.cfm**: Display of the offer page header.
- **dsp_offre_footer.cfm**: Display of the offer page footer.
- **ajax/getTypeClient.cfm**: Management of client type selection.
- **index.cfm**: Main entry point for the module.
- **err_offre_entry.cfm**: Management of errors during offer entry.
- **_insert_goodies_xerox_ne_pas_toucher_alain.cfm**: Insertion of goodies into the cart.

## 5. Error Management
- **Updating an offered product**: Management of update errors.
- **Inserting an offered product**: Management of insertion errors.
- **Deleting an offered product**: Management of deletion errors.

## 6. Interface
- **dsp_offre.cfm**: Display of product offers.
- **dsp_offre_form.cfm**: Management of adding and modifying offered products.
- **dsp_offre_search.cfm**: Search for offered products.
- **act_offre.cfm**: Management of actions on offers.

## 7. AJAX Queries
- **getTypeClient**: Retrieval of the list of client groups.
- **getLivreur**: Loading of the list of deliverers.
- **index**: Management of AJAX actions.

## 8. Business Logic
- **Logiques name**: Eligibility conditions for adding offered products.

This indexing plan allows for quick and efficient navigation through the technical documentation of the `gestion_produit_offert` module of Solusquare Commerce Cloud.
---