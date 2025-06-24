---
title: "Documentation technique"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/fr/doc_tech)

# Documentation technique

## Glossaire métier
Ce glossaire présente les termes et concepts clés associés au module `gestion_produit_offert` de Solusquare Commerce Cloud.

### Description du module
Le module `gestion_produit_offert` permet d'ajouter un produit offert dans les commandes clients sous certaines conditions. Ce produit est intégré dans le processus logistique sans être visible par le client dans son panier. Cela facilite la gestion des promotions et des offres spéciales tout en maintenant une expérience utilisateur fluide.

Ce module est essentiel pour les équipes techniques, car il nécessite une intégration précise avec les systèmes de gestion des commandes et de logistique. Les fonctionnalités incluent la définition des critères d'éligibilité pour les produits offerts et la gestion des stocks associés.

### Concepts clés
- **Produit offert** : Produit ajouté à la commande sans visibilité pour le client.
- **Conditions d'éligibilité** : Critères définissant quand un produit peut être offert.
- **Logistique** : Processus de gestion des stocks et des livraisons associés aux produits offerts.

### Entités
#### ProduitOffert
**Définition** : Représente un produit offert dans une commande.
**Type** : table
**Champs** :
- `offre_id` : int • Identifiant unique de l'offre.
- `produit_id` : int • Identifiant du produit offert.
- `valeur_commande` : decimal • Valeur minimale de commande pour l'offre.
- `nombre_commandes` : int • Nombre de commandes requises pour l'éligibilité.
- `date_debut` : datetime • Date de début de l'offre.
- `date_fin` : datetime • Date de fin de l'offre.
- `liste_pays_livraison` : varchar • Liste des pays éligibles pour la livraison.
- `limit_produit_by_x` : int • Limite de produits offerts par commande.
- `liste_civilite_livraison` : varchar • Liste des civilités éligibles pour la livraison.
- `nouveaux_clients` : bit • Indique si l'offre est réservée aux nouveaux clients.
- `nb_max_utilisation` : int • Nombre maximal d'utilisations de l'offre par client.
- `liste_livreur_id` : varchar • Liste des livreurs associés à l'offre.

## Fonctions
Cette section décrit les fonctions du module `gestion_produit_offert` de Solusquare Commerce Cloud, permettant d'ajouter des produits offerts dans les commandes clients sans les afficher dans le panier.

### Function : getPourClient
*Paramètres :*
- `typeClient` : int • Identifiant du type de client.

*Retour :*
- `Retour` : void • Aucune valeur retournée.

*Dépendances internes :*
- `jQuery` : Utilisé pour les appels AJAX.

*But :* Récupérer les informations spécifiques au type de client.

*Description :*
La fonction `getPourClient` est utilisée pour obtenir les informations relatives à un type de client spécifique. Elle effectue une requête AJAX vers un endpoint pour récupérer les données. En fonction du type de client (1 ou 2), elle met à jour l'interface utilisateur en affichant les informations pertinentes. La fonction gère également les erreurs potentielles en alertant l'utilisateur en cas de problème lors de la récupération des données. Les résultats sont ensuite intégrés dans le formulaire correspondant.

*Améliorations & optimisations :*
- Ajouter des messages d'erreur plus détaillés.
- Implémenter un mécanisme de cache pour éviter des requêtes répétées.

*Code de la fonction :*
```javascript
function getPourClient(typeClient) {
    var url = "/Ajax/gestion_produit_offert/index.cfm?ajaxAction=getTypeClient";

    jQuery(".span_type_client").css('display', 'none');
    jQuery(".span_type_client").html('');

    if (typeClient == 1 || typeClient == 2) {
        jQuery.ajax({
            type: "GET",
            url: url + "&typeClient=" + typeClient,
            error: function(error) {
                alert("#label_err_occurs#");
            },
            success: function(data) {
                jQuery(".span_type_client").html(data);
                jQuery("form[name='dsp_offre_form']").on("submit", function() {
                    return recherche_input();
                });
                jQuery('.selectpicker').selectpicker();
                jQuery(".span_type_client").css('display', 'inline-block');
            }
        });
    }
}
```

### Function : doselMultiple
*Paramètres :*
- Aucun.

*Retour :*
- `Retour` : void • Aucune valeur retournée.

*Dépendances internes :*
- `#script#` : Placeholder pour le code à ajouter.

*But :* Fonctionnalité non spécifiée.

*Description :*
La fonction `doselMultiple` est un placeholder pour une fonctionnalité à définir. Actuellement, elle ne contient pas de logique opérationnelle. Il est recommandé de spécifier son but et d'implémenter la logique nécessaire.

*Améliorations & optimisations :*
- Définir clairement le but de la fonction.
- Ajouter la logique nécessaire pour son fonctionnement.

*Code de la fonction :*
```javascript
function doselMultiple() {
    #script#
}
```

### Function : getlivreur_id
*Paramètres :*
- Aucun.

*Retour :*
- `Retour` : void • Aucune valeur retournée.

*Dépendances internes :*
- `jQuery` : Utilisé pour les appels AJAX.

*But :* Récupérer l'identifiant du livreur.

*Description :*
La fonction `getlivreur_id` permet de récupérer les identifiants des livreurs disponibles en fonction des sélections faites par l'utilisateur. Elle envoie une requête AJAX pour obtenir les données et met à jour l'interface utilisateur en conséquence. En cas d'erreur, un message d'alerte est affiché. Les résultats sont intégrés dans le formulaire, et la fonction gère également l'affichage d'un indicateur de chargement pendant le traitement.

*Améliorations & optimisations :*
- Ajouter des validations pour les sélections de l'utilisateur.
- Optimiser les appels AJAX pour réduire le temps de réponse.

*Code de la fonction :*
```javascript
function getlivreur_id() {
    jQuery(".span_liste_livreur_id").html("");
    jQuery("#waiting_selection_livreur_id").show();
    var url = "/Ajax/gestion_livreur/index.cfm?ajaxAction=getlivreur_id",
        liste_livreur_id = jQuery("#liste_livreur_id").val(),
        liste_partner_id = jQuery("[name=liste_partner_id]").val(),
        liste_pays_livraison = jQuery("[name=liste_pays_livraison]").val();

    url = url + "&liste_livreur_id=" + liste_livreur_id + "&liste_partner_id=" + liste_partner_id + "&liste_pays_livraison=" + liste_pays_livraison;

    jQuery.ajax({
        type: "GET",
        url: url,
        error: function(error) {
            alert("#label_err_occurs#");
            jQuery("#waiting_selection_livreur_id").hide();
        },
        success: function(data) {
            jQuery(".span_liste_livreur_id").html(data);
            jQuery("form[name='dsp_offre_form']").on("submit", function() {
                return recherche_input();
            });
            jQuery('.selectpicker').selectpicker();
            jQuery("#waiting_selection_livreur_id").hide();
        }
    });
}
```

### Function : checkdate
*Paramètres :*
- `datet` : string • Date à vérifier.

*Retour :*
- `Retour` : struct • Résultat de la vérification.

*Dépendances internes :*
- `isdate` : Fonction pour vérifier les dates.

*But :* Vérifier la validité d'une date.

*Description :*
La fonction `checkdate` vérifie si une date fournie est valide. Elle utilise la fonction `isdate` pour effectuer cette vérification. Si la date est valide, elle renvoie un objet struct contenant la date convertie. En cas d'erreur, elle renvoie un message d'erreur approprié. Cette fonction est essentielle pour garantir que les dates saisies par les utilisateurs sont correctes avant d'être traitées.

*Améliorations & optimisations :*
- Ajouter des formats de date supplémentaires pour la vérification.
- Améliorer la gestion des erreurs pour des cas spécifiques.

*Code de la fonction :*
```coldfusion
function checkdate(required string datet) {
    if (not isdate(Left(datet, 8)) and datet neq "") {
        return {ok: false, raison: "isdate false"};
    } else {
        try {
            arr = ListToArray(RTRIM(datet), " ");
            if (arraylen(arr) != 2) {
                return {ok: false, raison: "arraylen <> 2"};
            } else {
                date_d = arr[1];
                time_d = arr[2];
                date_d = mid(date_d, 7, 2) & mid(date_d, 4, 2) & mid(date_d, 1, 2);
                time_d = mid(time_d, 1, 2) & mid(time_d, 4, 2);
                if (!isnumeric(date_d) OR !isnumeric(time_d)) {
                    return {ok: false, raison: "!isnumeric " & date_d & " " & time_d};
                } else {
                    return {ok: true, dateconv: date_d & time_d};
                }
            }
        } catch (Any e) {
            return {ok: false, erreur: e};
        }
    }
}
```

## Requêtes
Cette section présente les requêtes utilisées dans le module `gestion_produit_offert` de Solusquare Commerce Cloud, permettant d'ajouter des produits offerts dans les commandes clients.

### Requête : deleteOffreClient
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Supprimer une offre client existante.
*Améliorations & optimisations :*
- Utiliser des transactions pour garantir l'intégrité des données.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="deleteOffreClient" datasource="#request.datasource#">
    DELETE FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Requête : insert_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Insérer un produit offert dans la base de données.
*Améliorations & optimisations :*
- Vérifier l'existence du produit avant insertion.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="insert_produit_offert" datasource="#request.datasource#">
    INSERT INTO bo_produit_offert (produit_id, client_id, date_creation)
    VALUES (
        <cfqueryparam value="#produit_id#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#now()#" cfsqltype="cf_sql_timestamp">
    )
</cfquery>
```

### Requête : getInfoProduitOffertClient
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les informations des produits offerts pour un client spécifique.
*Améliorations & optimisations :*
- Ajouter des index sur les colonnes fréquemment interrogées.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="getInfoProduitOffertClient" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert_client
    WHERE client_id = <cfqueryparam value="#client_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Requête : insClient
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Insérer un nouveau client dans la base de données.
*Améliorations & optimisations :*
- Utiliser des transactions pour garantir l'intégrité des données.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="insClient" datasource="#request.datasource#">
    INSERT INTO ud_client (nom, prenom, email, date_creation)
    VALUES (
        <cfqueryparam value="#nom#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#prenom#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#email#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#now()#" cfsqltype="cf_sql_timestamp">
    )
</cfquery>
```

### Requête : getGroupeClient
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les groupes de clients associés à un produit offert.
*Améliorations & optimisations :*
- Ajouter des index sur les colonnes fréquemment interrogées.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="getGroupeClient" datasource="#request.datasource#">
    SELECT * FROM bo_groupe_client
    WHERE produit_id = <cfqueryparam value="#produit_id#" cfsqltype="cf_sql_integer">
</cfquery>
```

### Requête : getLivreursNom
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les noms des livreurs associés aux produits offerts.
*Améliorations & optimisations :*
- Utiliser des transactions pour garantir l'intégrité des données.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="getLivreursNom" datasource="#request.datasource#">
    SELECT nom FROM bo_livreur
    WHERE actif = 1
</cfquery>
```

### Requête : pays_livre
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les pays de livraison disponibles pour les produits offerts.
*Améliorations & optimisations :*
- Ajouter des index sur les colonnes fréquemment interrogées.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="pays_livre" datasource="#request.datasource#">
    SELECT * FROM ud_pays
    WHERE actif = 1
</cfquery>
```

### Requête : getCat
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les catégories de produits disponibles.
*Améliorations & optimisations :*
- Ajouter des index sur les colonnes fréquemment interrogées.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="getCat" datasource="#request.datasource#">
    SELECT * FROM ud_categorie
</cfquery>
```

### Requête : getOffre
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Récupérer les offres disponibles pour les produits offerts.
*Améliorations & optimisations :*
- Ajouter des index sur les colonnes fréquemment interrogées.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="getOffre" datasource="#request.datasource#">
    SELECT * FROM bo_produit_offert
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_partner_id" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_partner_id
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_civilite
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des civilités pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_civilite" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_civilite
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_client_goodies
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des goodies clients.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_client_goodies" datasource="#request.datasource#">
    ALTER TABLE bo_client_goodies
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_selection
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des sélections de produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_selection" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_selection
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_pays_liv
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des pays de livraison pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```coldfusion
<cfquery name="alter_table_bo_produit_offert_pays_liv" datasource="#request.datasource#">
    ALTER TABLE bo_produit_offert_pays_liv
    ADD COLUMN nouveau_champ VARCHAR(255)
</cfquery>
```

### Requête : alter_table_bo_produit_offert_partner_id
*Paramètres :*
- `datasource` : string • Source de données pour la requête
*But :* Modifier la structure de la table des partenaires pour les produits offerts.
*Améliorations & optimisations :*
- Vérifier les dépendances avant modification.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la

## Dépendances
Cette section décrit les dépendances nécessaires au bon fonctionnement du module `gestion_produit_offert` de Solusquare Commerce Cloud.

### Dépendance : allow_update.cfm
*Fichier :* `allow_update.cfm`  
*Type :* Inclusion de template  
*But :* Permet de gérer les mises à jour des offres de produits.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="#request.libroot#/allow_update.cfm">
```

### Dépendance : qry_get_offre.cfm
*Fichier :* `qry_get_offre.cfm`  
*Type :* Inclusion de template  
*But :* Récupère les offres de produits disponibles dans la base de données.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_offre.cfm">
```

### Dépendance : qry_get_langues.cfm
*Fichier :* `qry_get_langues.cfm`  
*Type :* Inclusion de template  
*But :* Récupère les langues disponibles pour les produits.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_langues.cfm">
```

### Dépendance : qry_get_cat.cfm
*Fichier :* `qry_get_cat.cfm`  
*Type :* Inclusion de template  
*But :* Récupère les catégories de produits disponibles.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_cat.cfm">
```

### Dépendance : qry_get_all_type_produit.cfm
*Fichier :* `qry_get_all_type_produit.cfm`  
*Type :* Inclusion de template  
*But :* Récupère tous les types de produits disponibles.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_all_type_produit.cfm">
```

### Dépendance : qry_get_all_partners.cfm
*Fichier :* `qry_get_all_partners.cfm`  
*Type :* Inclusion de template  
*But :* Récupère tous les partenaires disponibles.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_all_partners.cfm">
```

### Dépendance : qry_verif_produit.cfm
*Fichier :* `qry_verif_produit.cfm`  
*Type :* Inclusion de template  
*But :* Vérifie l'existence d'un produit dans la base de données.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_verif_produit.cfm">
```

### Dépendance : qry_get_designation.cfm
*Fichier :* `qry_get_designation.cfm`  
*Type :* Inclusion de template  
*But :* Récupère la désignation d'un produit donné.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="qry_get_designation.cfm">
```

### Dépendance : dsp_offre.cfm
*Fichier :* `dsp_offre.cfm`  
*Type :* Inclusion de template  
*But :* Affiche les détails des offres de produits.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="dsp_offre.cfm">
```

### Dépendance : dsp_offre_form.cfm
*Fichier :* `dsp_offre_form.cfm`  
*Type :* Inclusion de template  
*But :* Gère le formulaire d'ajout ou de modification d'une offre.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="dsp_offre_form.cfm">
```

### Dépendance : dsp_offre_search.cfm
*Fichier :* `dsp_offre_search.cfm`  
*Type :* Inclusion de template  
*But :* Gère la recherche d'offres de produits.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="dsp_offre_search.cfm">
```

### Dépendance : dsp_offre_header.cfm
*Fichier :* `dsp_offre_header.cfm`  
*Type :* Inclusion de template  
*But :* Affiche l'en-tête de la page des offres.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="dsp_offre_header.cfm">
```

### Dépendance : dsp_offre_footer.cfm
*Fichier :* `dsp_offre_footer.cfm`  
*Type :* Inclusion de template  
*But :* Affiche le pied de page de la page des offres.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="dsp_offre_footer.cfm">
```

### Dépendance : ajax/getTypeClient.cfm
*Fichier :* `getTypeClient.cfm`  
*Type :* Inclusion de template  
*But :* Gère la sélection du type de client pour les offres.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="ajax/getTypeClient.cfm">
```

### Dépendance : index.cfm
*Fichier :* `index.cfm`  
*Type :* Inclusion de template  
*But :* Point d'entrée principal pour le module de gestion des produits offerts.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="index.cfm">
```

### Dépendance : err_offre_entry.cfm
*Fichier :* `err_offre_entry.cfm`  
*Type :* Inclusion de template  
*But :* Gère les erreurs lors de l'entrée des offres.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="err_offre_entry.cfm">
```

### Dépendance : _insert_goodies_xerox_ne_pas_toucher_alain.cfm
*Fichier :* `_insert_goodies_xerox_ne_pas_toucher_alain.cfm`  
*Type :* Inclusion de template  
*But :* Insère des goodies dans le panier et la commande.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="_insert_goodies_xerox_ne_pas_toucher_alain.cfm">
```

Cette documentation présente les dépendances essentielles pour le module `gestion_produit_offert`, permettant ainsi une intégration et un fonctionnement optimaux au sein de Solusquare Commerce Cloud.

## Gestion d'erreurs
Cette section décrit les erreurs potentielles dans le module gestion_produit_offert de Solusquare Commerce Cloud.

### Bloc : Mise à jour d'un produit offert
*Fichier :* `act_offre.cfm`
*Erreurs traitées :*
- Erreurs de doublon de marque
- Erreurs de mise à jour

*Comportement :*
- Affiche un message d'erreur approprié.

*Propagation des erreurs :*
- Les erreurs sont capturées et stockées dans la variable `ERROR`.

*Améliorations & Optimisations :*
- Ajouter des logs pour un meilleur suivi des erreurs.

*Code de l'inclusion :* 
```coldfusion
<cftry>
    <cfquery datasource="#request.datasource#">
        UPDATE bo_produit_offert 
        SET produit_id = '#attributes.produit_id#',
            ...
        WHERE offre_id = #attributes.offre_id#
    </cfquery>
    <cfcatch type="database">
        <cfdump var="#cfcatch#">
        <cfif CFCATCH.SQLSTATE EQ 23000>
            <cfset ERROR = "#label_err_doublon_marque#<br/>">
        <cfelse>
            <cfset ERROR = "#label_err_update#<br/>">
        </cfif>
    </cfcatch>
</cftry>
```

### Bloc : Insertion d'un produit offert
*Fichier :* `act_offre.cfm`
*Erreurs traitées :*
- Erreurs d'insertion de produit

*Comportement :*
- Affiche un message d'erreur approprié.

*Propagation des erreurs :*
- Les erreurs sont capturées et stockées dans la variable `ERROR`.

*Améliorations & Optimisations :*
- Implémenter une gestion des erreurs plus granulaire.

*Code de l'inclusion :* 
```coldfusion
<cftry>
    <cfquery name="insert_produit_offert" datasource="#request.datasource#">
        INSERT INTO bo_produit_offert (
            produit_id,
            ...
        )
        VALUES (
            '#attributes.produit_id#',
            ...
        )
        select @@identity as offreid
    </cfquery>
    <cfcatch type="database">
        <cfdump var="#cfcatch#">
        <cfif CFCATCH.SQLSTATE EQ 23000>
            <cfset ERROR = "#label_err_doublon_marque#<br/>">
        <cfelse>
            <cfset ERROR = "#label_err_insert#<br/>">
        </cfif>
    </cfcatch>
</cftry>
```

### Bloc : Suppression d'un produit offert
*Fichier :* `act_offre.cfm`
*Erreurs traitées :*
- Erreurs de suppression

*Comportement :*
- Affiche un message d'erreur approprié.

*Propagation des erreurs :*
- Les erreurs sont capturées et stockées dans la variable `ERROR`.

*Améliorations & Optimisations :*
- Ajouter des notifications pour les erreurs critiques.

*Code de l'inclusion :* 
```coldfusion
<cftry>
    <cfquery datasource="#request.datasource#">
        delete bo_produit_offert 
        where offre_id = #attributes.offre_id#
    </cfquery>
    <cfcatch type="database">
        <cfif CFCATCH.SQLSTATE EQ 23000>
            <cfset ERROR = "#label_err_doublon_marque#<br/>">
        <cfelse>
            <cfset ERROR = "#label_err_update#<br/>">
        </cfif>
    </cfcatch>
</cftry>
```

## Interface
Ce module permet d'ajouter un produit offert dans les commandes clients, sans que le client ne le voie dans son panier, facilitant ainsi la gestion logistique.

### Composant : dsp_offre.cfm
*Fichier :* `dsp_offre.cfm`
*But :* Afficher les offres de produits offerts et gérer les erreurs de recherche.

*Champs :*
- `criteria` : Critères de recherche pour filtrer les produits offerts.
- `error` : Message d'erreur à afficher si une erreur survient.

*Evénements & Actions :*
- Affichage des résultats de recherche.
- Gestion des erreurs lors de la recherche.

*Dépendances visuelles :*
- Utilisation de styles CSS pour la mise en forme des notifications et des tableaux.

*Améliorations & optimisations :*
- Optimisation des requêtes pour réduire le temps de chargement.
- Amélioration de l'interface utilisateur pour une meilleure expérience.

*Code de la requête :*
```coldfusion
<cfquery name="qry_get_offre" datasource="#request.datasource#">
    SELECT bo_produit_offert.*, 
           ISNULL(ud_option1.libelle,ud_produit1.designation) AS designation
    FROM bo_produit_offert WITH (NOLOCK)  
    INNER JOIN ud_produit1 WITH (NOLOCK) ON ud_produit1.produit_id = bo_produit_offert.produit_id
    WHERE 0=0
    <CFIF #ATTRIBUTES.CRITERIA# NEQ ''>
        #PreserveSingleQuotes(attributes.Criteria)#
    </CFIF>
    ORDER BY bo_produit_offert.produit_id
</cfquery>
```

### Composant : dsp_offre_form.cfm
*Fichier :* `dsp_offre_form.cfm`
*But :* Gérer l'ajout et la modification des produits offerts.

*Champs :*
- `produit_id` : Identifiant du produit offert.
- `code_ean` : Code EAN du produit.
- `valeur_commande` : Valeur minimale de commande pour bénéficier de l'offre.

*Evénements & Actions :*
- Soumission du formulaire pour ajouter ou modifier une offre.
- Validation des champs obligatoires.

*Dépendances visuelles :*
- Utilisation de JavaScript pour la validation dynamique des champs.

*Améliorations & optimisations :*
- Ajout de messages d'erreur clairs pour les utilisateurs.
- Amélioration de la réactivité du formulaire.

*Code de la requête :*
```coldfusion
<cfquery name="insert_produit_offert" datasource="#request.datasource#">
    INSERT INTO bo_produit_offert (
        produit_id,
        code_ean,
        valeur_commande
    ) VALUES (
        '#attributes.produit_id#',
        '#attributes.code_ean#',
        #attributes.valeur_commande#
    )
</cfquery>
```

### Composant : dsp_offre_search.cfm
*Fichier :* `dsp_offre_search.cfm`
*But :* Permettre la recherche de produits offerts selon divers critères.

*Champs :*
- `Crit1_Value` : Valeur du produit offert.
- `Crit2_Value` : Type de produit.

*Evénements & Actions :*
- Soumission de la recherche.
- Affichage des résultats.

*Dépendances visuelles :*
- Tableaux pour afficher les résultats de recherche.

*Améliorations & optimisations :*
- Filtrage des résultats pour une meilleure pertinence.
- Pagination des résultats pour une navigation facile.

*Code de la requête :*
```coldfusion
<cfquery name="qry_get_offre" datasource="#request.datasource#">
    SELECT bo_produit_offert.*, 
           ISNULL(ud_option1.libelle,ud_produit1.designation) AS designation
    FROM bo_produit_offert WITH (NOLOCK)  
    WHERE 0=0
    <CFIF #ATTRIBUTES.CRITERIA# NEQ ''>
        #PreserveSingleQuotes(attributes.Criteria)#
    </CFIF>
    ORDER BY bo_produit_offert.produit_id
</cfquery>
```

### Composant : act_offre.cfm
*Fichier :* `act_offre.cfm`
*But :* Gérer les actions d'insertion, de mise à jour et de suppression des produits offerts.

*Champs :*
- `offre_id` : Identifiant de l'offre à modifier ou supprimer.

*Evénements & Actions :*
- Traitement des actions de l'utilisateur sur les offres.

*Dépendances visuelles :*
- Notifications pour indiquer le succès ou l'échec des actions.

*Améliorations & optimisations :*
- Gestion des erreurs pour éviter les doublons.
- Optimisation des requêtes pour améliorer la performance.

*Code de la requête :*
```coldfusion
<cfquery name="deleteOffreClient" datasource="#request.datasource#">
    DELETE FROM bo_produit_offert_client
    WHERE offre_id = #attributes.offre_id#
</cfquery>
```

Cette documentation fournit une vue d'ensemble des composants du module `gestion_produit_offert`, facilitant ainsi la compréhension et l'utilisation par les équipes techniques de Solusquare.

## Requêtes AJAX
Cette section décrit les requêtes AJAX utilisées dans le module `gestion_produit_offert` de Solusquare Commerce Cloud, permettant d'ajouter des produits offerts dans les commandes clients.

### Requête : getTypeClient
*Paramètres :*
- `typeClient` : entier • Identifiant du type de client sélectionné.
*But :* Récupérer et afficher la liste des groupes de clients en fonction du type sélectionné.
*Améliorations & optimisations :*
- Utiliser des requêtes AJAX asynchrones pour améliorer la réactivité de l'interface.
*Risques SQL & Sécurité :*
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.

*Code de la requête :*
```javascript
jQuery.ajax({
    type: "GET",
    url: url + "&typeClient=" + typeClient,
    error: function(error) {
        alert("#label_err_occurs#");
    },
    success: function(data) {
        jQuery(".span_type_client").html(data);
        jQuery("form[name='dsp_offre_form']").on("submit", function(){
            return recherche_input();
        });
        jQuery('.selectpicker').selectpicker();
        jQuery(".span_type_client").css('display','inline-block');
    }
});
```

### Requête : getLivreur
*Paramètres :*
- `url` : chaîne • URL pour récupérer la liste des livreurs.
*But :* Charger et afficher la liste des livreurs disponibles.
*Améliorations & optimisations :*
- Implémenter un mécanisme de cache pour éviter des requêtes répétées.
*Risques SQL & Sécurité :*
- Vérifier les permissions d'accès aux données des livreurs.

*Code de la requête :*
```javascript
jQuery.ajax({
    type: "GET",
    url: url,
    error: function(error) {
        alert("#label_err_occurs#");
        jQuery("#waiting_selection_livreur_id").hide();
    },
    success: function(data) {
        jQuery(".span_liste_livreur_id").html(data);
        jQuery("form[name='dsp_offre_form']").on("submit", function(){
            return recherche_input();
        });
        jQuery('.selectpicker').selectpicker();
        jQuery("#waiting_selection_livreur_id").hide();
    }
});
```

### Requête : index
*Paramètres :*
- `ajaxAction` : chaîne • Action AJAX à exécuter.
*But :* Gérer les différentes actions AJAX en fonction de la requête.
*Améliorations & optimisations :*
- Centraliser la gestion des erreurs pour une meilleure maintenance.
*Risques SQL & Sécurité :*
- Validation des actions pour éviter les appels non autorisés.

*Code de la requête :*
```coldfusion
<cfswitch expression="#url.ajaxAction#">
    <cfcase value="getTypeClient">
        <cfparam name="url.typeClient" default="0">
        <cfinclude template="getTypeClient.cfm">
    </cfcase>
    <cfdefaultcase>
        <cfoutput>ERROR in lib/ajaxfunctions/index.cfm : Unknown AJAX action provided : #url.ajaxAction# !</cfoutput>
    </cfdefaultcase>
</cfswitch>
```

## Logique métier
Ce module gère l'ajout de produits offerts dans les commandes clients, sans que ces produits soient visibles dans le panier du client. Cela permet à la logistique de les intégrer tout en respectant les conditions définies.

### Logiques name
*Explication :* Cette logique détermine les conditions sous lesquelles un produit offert peut être ajouté à une commande. Les critères incluent la valeur de la commande, le nombre de commandes passées, et des dates spécifiques.

#### Contraintes :
1. Les produits offerts ne doivent pas apparaître dans le panier du client.
2. Les conditions d'éligibilité doivent être vérifiées avant l'ajout du produit.
3. Les données doivent être correctement formatées pour l'intégration dans la base de données.

#### Code sous forme de chunks :
```coldfusion
{"source": "act_offre.cfm", "start": 2, "end": 2, "code": "<cfset ERROR=\"\">\n"}
{"source": "act_offre.cfm", "start": 6, "end": 6, "code": "<cfif attributes.offre_id neq \"\">\n"}
{"source": "act_offre.cfm", "start": 21, "end": 21, "code": "\t\t\t\t\t<cfif isdefined(\"param_client.langue_goodies\") and param_client.langue_goodies>\n"}
{"source": "act_offre.cfm", "start": 28, "end": 28, "code": "\t\t\t\t\tvaleur_commande \t\t= <cfif valeur_commande eq \"\">NULL<cfelse>#valeur_commande#</cfif>,\n"}
{"source": "act_offre.cfm", "start": 29, "end": 29, "code": "\t\t\t\t\tnombre_commandes \t\t= <cfif nombre_commandes eq \"\">NULL<cfelse>#nombre_commandes#</cfif>,\n"}
{"source": "act_offre.cfm", "start": 30, "end": 30, "code": "\t\t\t\t\tdate_debut \t\t\t\t= <cfif date_debut eq \"\">NULL<cfelse>{ts '20#mid( date_debut, 7,2)#-#mid( date_debut, 4,2)#-#mid( date_debut, 1,2)# #mid( date_debut, 10,5)#:00.000'}</cfif>,\n"}
{"source": "act_offre.cfm", "start": 31, "end": 31, "code": "\t\t\t\t\tdate_fin \t\t\t\t= <cfif date_fin eq \"\">NULL<cfelse>{ts '20#mid( date_fin, 7,2)#-#mid( date_fin, 4,2)#-#mid( date_fin, 1,2)#  #mid( date_fin, 10,5)#:00.000'}</cfif>,\n"}
{"source": "act_offre.cfm", "start": 34, "end": 34, "code": "\t\t\t\t\tmois_derniere_cde \t\t= <cfif mois_derniere_cde eq \"\">NULL<cfelse>#mois_derniere_cde#</cfif>,\n"}
{"source": "act_offre.cfm", "start": 35, "end": 35, "code": "\t\t\t\t\tmois_inscription \t\t= <cfif mois_inscription eq \"\">NULL<cfelse>#mois_inscription#</cfif>,\n"}
{"source": "act_offre.cfm", "start": 36, "end": 36, "code": "\t\t\t\t\tliste_partner_id \t\t= <cfif attributes.liste_partner_id eq \",,\">NULL<cfelse>'#attributes.liste_partner_id#'</cfif>,\n"}
{"source": "act_offre.cfm", "start": 37, "end": 37, "code": "\t\t\t\t\tlimit_produit_by_x \t\t= <cfif isdefined(\"attributes.limit_produit_by_x\") AND val(attributes.limit_produit_by_x) gt 0>#val(attributes.limit_produit_by_x)#<cfelse>NULL</cfif>,\n"}
{"source": "act_offre.cfm", "start": 38, "end": 38, "code": "\t\t\t\t\tliste_pays_livraison \t= <cfif isdefined(\"attributes.liste_pays_livraison\") AND attributes.liste_pays_livraison neq \",,\">'#attributes.liste_pays_livraison#'<cfelse>NULL</cfif>,\n"}
{"source": "act_offre.cfm", "start": 40, "end": 40, "code": "\t\t\t\t\ttout_les_x_produit_commande = <cfif val(attributes.tout_les_x_produit_commande) eq 0>NULL<cfelse>#val(attributes.tout_les_x_produit_commande)#</cfif>,\n"}
{"source": "act_offre.cfm", "start": 41, "end": 41, "code": "\t\t\t\t\tnombre_commandes_recurrence = <cfif isdefined(\"attributes.nombre_commandes_recurrence\")>1<cfelse>0</cfif>,\n"}
{"source": "act_offre.cfm", "start": 42, "end": 42, "code": "                    liste_civilite_livraison    = <cfif isdefined(\"attributes.liste_civilite_livraison\") AND attributes.liste_civilite_livraison neq \",,\">'#attributes.liste_civilite_livraison#'<cfelse>NULL</cfif>,\n"}
{"source": "act_offre.cfm", "start": 43, "end": 43, "code": "\t\t\t\t\tnouveaux_clients  = <cfif isdefined(\"attributes.type_client\") and attributes.type_client eq 3>1<cfelse>NULL</cfif>,\n"}
{"source": "act_offre.cfm", "start": 44, "end": 44, "code": "\t\t\t\t\tnb_max_utilisation  = <cfif isdefined(\"attributes.nb_max_utilisation\") and attributes.nb_max_utilisation neq \"\" and attributes.nb_max_utilisation neq \"0\">#attributes.nb_max_utilisation#<cfelse>NULL</cfif>,\n"}
{"source": "act_offre.cfm", "start": 45, "end": 45, "code": "\t\t\t\t\tliste_livreur_id \t\t= <cfif isdefined(\"attributes.liste_livreur\") and attributes.liste_livreur neq \",,\" and attributes.liste_livreur neq \"\">'#attributes.liste_livreur#'<cfelse>NULL</cfif>\n"}
```

