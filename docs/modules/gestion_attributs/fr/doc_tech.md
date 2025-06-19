---
title: "Documentation technique"
---

# Documentation technique

## Glossaire métier
Ce glossaire décrit le module Gestion des attributs de produit de Solusquare Commerce Cloud, essentiel pour la gestion et l'exploitation des attributs produits dans le système.

### Description du module
Le module Gestion des attributs permet de créer des typologies d'attributs produits et de les associer aux types de produits. Il facilite la gestion multilingue des libellés d'attributs et leur organisation par ordre de tri.

Il offre aussi la possibilité d'affecter ces attributs à différents types de produits, permettant ainsi leur exploitation cohérente sur les fiches produits. Le module gère également les options d'attributs, incluant des spécificités comme les couleurs et filtres.

### Concepts clés
- *Attribut* : Caractéristique descriptive d’un produit.
- *Typologie d’attribut* : Catégorie ou groupe d’attributs.
- *Type de produit* : Classification d’un produit selon ses caractéristiques.
- *Libellé multilingue* : Nom d’un attribut traduit dans plusieurs langues.
- *Option d’attribut* : Valeur possible d’un attribut.
- *Filtre* : Critère utilisé pour affiner la recherche produit.
- *Couleur* : Attribut spécifique avec gestion de code couleur.
- *Tri* : Ordre d’affichage des attributs.
- *Groupe de couleur* : Regroupement d’attributs liés aux couleurs.

### Entités

#### bo_attribut
**Définition** : Représente un attribut produit avec ses propriétés multilingues et ses options spécifiques.  
**Type** : table  
**Champs** :  
- `attribut_id` : numeric • Identifiant unique de l’attribut  
- `pays_id` : varchar • Pays d’application de l’attribut  
- `libelle` : nvarchar • Libellé de l’attribut  
- `date_creation` : datetime • Date de création  
- `langue_id` : varchar • Langue du libellé  
- `code_ext` : varchar • Code externe de l’attribut  
- `filtre` : int • Indique si l’attribut est un filtre (1 = oui)  
- `est_une_couleur` : tinyint • Indique si l’attribut représente une couleur (1 = oui)  

#### bo_attribut_type_produit
**Définition** : Association entre un attribut et un type de produit avec un ordre de tri et statut.  
**Type** : table  
**Champs** :  
- `attribut_id` : numeric • Identifiant de l’attribut  
- `type_produit_id` : numeric • Identifiant du type de produit  
- `tri` : numeric • Ordre d’affichage  
- `statut_attribut` : numeric • Statut de l’association  

#### bo_attribut_detail
**Définition** : Détail d’une option d’attribut, avec libellé multilingue et propriétés spécifiques.  
**Type** : table  
**Champs** :  
- `attribut_detail_id` : int • Identifiant unique de l’option  
- `libelle` : nvarchar • Libellé de l’option  
- `pays_id` : varchar • Pays d’application  
- `langue_id` : varchar • Langue du libellé  
- `code` : nvarchar • Code option  
- `ordre` : int • Ordre d’affichage  
- `attribut_group_id` : int • Groupe de couleur associé  
- `code_group` : nvarchar • Code du groupe  
- `libelle_group` : nvarchar • Libellé du groupe  
- `code_enseigne` : varchar • Code enseigne  
- `attribut_id` : int • Identifiant de l’attribut parent  
- `code_couleur` : varchar • Code couleur hexadécimal  

#### bo_attribut_detail_cat_group
**Définition** : Groupe de couleur pour les options d’attributs, avec codes et ordre.  
**Type** : table  
**Champs** :  
- `attribut_group_id` : int • Identifiant du groupe  
- `couleur` : nvarchar • Couleur associée  
- `ordre` : int • Ordre d’affichage  
- `langue_id` : nvarchar • Langue du libellé  
- `code_ext` : nvarchar • Code externe  
- `code_couleur` : nvarchar • Code couleur hexadécimal  

#### bo_attribut_detail_option
**Définition** : Association entre une option d’attribut et une option produit.  
**Type** : table  
**Champs** :  
- `attribut_option_id` : numeric • Identifiant de l’association  
- `option_id` : numeric • Identifiant de l’option produit  
- `attribut_id` : numeric • Identifiant de l’attribut  
- `attribut_detail_id` : numeric • Identifiant de l’option d’attribut  

---

Ce module est central pour la gestion fine des caractéristiques produits, leur affichage multilingue, et leur association aux types de produits dans Solusquare Commerce Cloud.

## Fonctions
Cette section décrit les fonctions du module Gestion des attributs de produit, utilisées pour manipuler et valider les attributs dans Solusquare Commerce Cloud.

### Function : change_color_input
*Paramètres :*
- `element` : object • élément DOM input de couleur

*Retour :*
- `void` • aucun retour

*Dépendances internes :*
- `jQuery` : manipulation DOM et gestion des valeurs d'input

*But :* Valider et corriger la saisie d'une couleur hexadécimale

*Description :*  
Cette fonction JavaScript valide la saisie d'une couleur dans un champ input. Elle vérifie que la valeur saisie correspond au format hexadécimal avec un double dièse (`##`) suivi de 6 caractères hexadécimaux (exemple : `##A1B2C3`). Si la valeur est valide, elle supprime toute bordure d'erreur et met à jour un champ input adjacent avec la même valeur. Si la valeur est invalide, elle vide le champ et réinitialise le champ adjacent à la couleur noire par défaut (`##000000`). Cette validation permet d'assurer que seules des couleurs valides sont enregistrées dans les options d'attributs.

*Améliorations & optimisations :*  
- Ajouter un retour visuel clair en cas d'erreur (bordure rouge, message)  
- Permettre la saisie avec un seul dièse (`#`) pour plus d'ergonomie  
- Externaliser la regex pour faciliter la maintenance  
- Ajouter des tests unitaires pour la validation

*Code de la fonction :*

```javascript
/**
 * Valide la saisie d'une couleur hexadécimale dans un champ input.
 * Si la valeur est valide (format ##XXXXXX), met à jour le champ adjacent.
 * Sinon, réinitialise la valeur à ##000000.
 *
 * @param {HTMLElement} element - L'élément input de couleur à valider.
 */
function change_color_input(element) {
    // Expression régulière pour valider une couleur hexadécimale avec double dièse
    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

    // Récupère la valeur saisie dans l'input
    const value = jQuery(element).val();

    if (regex_color.test(value)) {
        // Valeur valide : supprime la bordure d'erreur éventuelle
        jQuery(element).css('border', '');
        // Met à jour le champ input suivant avec la même valeur
        jQuery(element).next('input').val(value);
    } else {
        // Valeur invalide : vide le champ input
        jQuery(element).val('');
        // Réinitialise le champ input suivant à la couleur noire par défaut
        jQuery(element).next('input').val('##000000');
        // Optionnel : afficher une bordure rouge pour indiquer l'erreur
        // jQuery(element).css('border', '1px solid red');
    }
}
```

## Requêtes
Cette section décrit les principales requêtes SQL utilisées dans le module Gestion des attributs de produit de Solusquare Commerce Cloud, permettant la création, l'affectation, la mise à jour et la suppression des attributs et leur liaison aux types de produits.

---

### Requête : insert_att
*Paramètres :*
- `pays_id` : varchar • Identifiant du pays
- `libelle` : nvarchar • Libellé de l'attribut
- `date_creation` : datetime • Date de création
- `langue_id` : varchar • Identifiant de la langue
- `code_ext` : varchar • Code externe de l'attribut
- `filtre` : int • Indique si l'attribut est un filtre
- `est_une_couleur` : tinyint • Indique si l'attribut est une couleur

*But :* Insérer un nouvel attribut dans la table `bo_attribut`.

*Améliorations & optimisations :*
- Utiliser des procédures stockées pour centraliser la logique métier.
- Ajouter des contraintes d'unicité sur `code_ext` pour éviter les doublons.

*Risques SQL & Sécurité :*
- Injection SQL si les paramètres ne sont pas correctement échappés.
- Vérifier la validité des données avant insertion.

*Code de la requête :*
```coldfusion
<!--- Insertion d'un nouvel attribut --->
<cfquery name="insert_att" datasource="#request.datasource#">
    INSERT INTO bo_attribut (
        pays_id,
        libelle,
        date_creation,
        langue_id,
        code_ext,
        filtre,
        est_une_couleur
    ) VALUES (
        <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        <cfqueryparam value="#date_creation#" cfsqltype="cf_sql_timestamp">,
        <cfqueryparam value="#langue_id#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#code_ext#" cfsqltype="cf_sql_varchar">,
        <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    )
</cfquery>
```

---

### Requête : insert_att_type_prod
*Paramètres :*
- `attribut_id` : numeric • Identifiant de l'attribut
- `type_produit_id` : numeric • Identifiant du type de produit
- `tri` : numeric • Ordre d'affichage
- `statut_attribut` : numeric • Statut de l'attribut (actif/inactif)

*But :* Associer un attribut à un type de produit dans la table `bo_attribut_type_produit`.

*Améliorations & optimisations :*
- Vérifier l'existence préalable de l'association pour éviter les doublons.
- Indexer les colonnes `attribut_id` et `type_produit_id` pour optimiser les recherches.

*Risques SQL & Sécurité :*
- Injection SQL si les paramètres ne sont pas sécurisés.
- Gestion des erreurs en cas d'insertion en double.

*Code de la requête :*
```coldfusion
<!--- Association d'un attribut à un type de produit --->
<cfquery name="insert_att_type_prod" datasource="#request.datasource#">
    INSERT INTO bo_attribut_type_produit (
        attribut_id,
        type_produit_id,
        tri,
        statut_attribut
    ) VALUES (
        <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#tri#" cfsqltype="cf_sql_numeric">,
        <cfqueryparam value="#statut_attribut#" cfsqltype="cf_sql_numeric">
    )
</cfquery>
```

---

### Requête : delete_attribut
*Paramètres :*
- `attribut_id` : numeric • Identifiant de l'attribut à supprimer

*But :* Supprimer un attribut de la table `bo_attribut`.

*Améliorations & optimisations :*
- Ajouter une suppression en cascade ou vérifier les dépendances avant suppression.
- Utiliser une transaction pour garantir l'intégrité des données.

*Risques SQL & Sécurité :*
- Suppression accidentelle si l'identifiant est incorrect.
- Risque d'incohérence si des références existent dans d'autres tables.

*Code de la requête :*
```coldfusion
<!--- Suppression d'un attribut --->
<cfquery name="delete_attribut" datasource="#request.datasource#">
    DELETE FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Requête : delete_attribut_prod
*Paramètres :*
- `attribut_id` : numeric • Identifiant de l'attribut
- `type_produit_id` : numeric • Identifiant du type de produit

*But :* Supprimer l'association entre un attribut et un type de produit.

*Améliorations & optimisations :*
- Vérifier l'existence de l'association avant suppression.
- Utiliser des transactions si plusieurs suppressions sont nécessaires.

*Risques SQL & Sécurité :*
- Suppression non désirée si les paramètres sont mal fournis.
- Impact sur l'affichage des fiches produits.

*Code de la requête :*
```coldfusion
<!--- Suppression de l'association attribut - type de produit --->
<cfquery name="delete_attribut_prod" datasource="#request.datasource#">
    DELETE FROM bo_attribut_type_produit
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
      AND type_produit_id = <cfqueryparam value="#type_produit_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Requête : update_att
*Paramètres :*
- `libelle` : nvarchar • Nouveau libellé de l'attribut
- `filtre` : int • Nouveau statut filtre
- `est_une_couleur` : tinyint • Nouveau statut couleur
- `attribut_id` : numeric • Identifiant de l'attribut à mettre à jour

*But :* Mettre à jour les informations d'un attribut existant.

*Améliorations & optimisations :*
- Valider les données avant mise à jour.
- Utiliser une procédure stockée pour centraliser la logique.

*Risques SQL & Sécurité :*
- Injection SQL si les paramètres ne sont pas sécurisés.
- Mise à jour partielle pouvant entraîner des incohérences.

*Code de la requête :*
```coldfusion
<!--- Mise à jour d'un attribut --->
<cfquery name="update_att" datasource="#request.datasource#">
    UPDATE bo_attribut
    SET libelle = <cfqueryparam value="#libelle#" cfsqltype="cf_sql_nvarchar">,
        filtre = <cfqueryparam value="#filtre#" cfsqltype="cf_sql_integer">,
        est_une_couleur = <cfqueryparam value="#est_une_couleur#" cfsqltype="cf_sql_tinyint">
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Requête : getpays
*Paramètres :* Aucun

*But :* Récupérer la liste des pays disponibles pour l'affectation des attributs.

*Améliorations & optimisations :*
- Mettre en cache les résultats pour réduire les accès base.
- Ajouter un filtre d'activation si nécessaire.

*Risques SQL & Sécurité :*
- Aucun risque majeur, requête en lecture seule.

*Code de la requête :*
```coldfusion
<!--- Récupération de la liste des pays --->
<cfquery name="getpays" datasource="#request.datasource#">
    SELECT pays_id, nom
    FROM ud_pays
    WHERE catal = 1
    ORDER BY nom
</cfquery>
```

---

### Requête : get_attribut_langue
*Paramètres :*
- `attribut_id` : numeric • Identifiant de l'attribut

*But :* Récupérer les libellés d'un attribut dans toutes les langues.

*Améliorations & optimisations :*
- Indexer la colonne `attribut_id` pour accélérer la recherche.
- Utiliser une vue si la jointure est complexe.

*Risques SQL & Sécurité :*
- Injection SQL si `attribut_id` n'est pas sécurisé.

*Code de la requête :*
```coldfusion
<!--- Récupération des libellés d'un attribut par langue --->
<cfquery name="get_attribut_langue" datasource="#request.datasource#">
    SELECT langue_id, libelle
    FROM bo_attribut
    WHERE attribut_id = <cfqueryparam value="#attribut_id#" cfsqltype="cf_sql_numeric">
</cfquery>
```

---

### Requête : getColorAttribute
*Paramètres :*
- `pays_id` : varchar • Identifiant du pays

*But :* Récupérer les attributs de type couleur pour un pays donné.

*Améliorations & optimisations :*
- Ajouter un index sur `pays_id` et `est_une_couleur`.
- Limiter les résultats aux attributs actifs.

*Risques SQL & Sécurité :*
- Injection SQL si `pays_id` n'est pas sécurisé.

*Code de la requête :*
```coldfusion
<!--- Récupération des attributs couleur pour un pays --->
<cfquery name="getColorAttribute" datasource="#request.datasource#">
    SELECT attribut_id, libelle
    FROM bo_attribut
    WHERE pays_id = <cfqueryparam value="#pays_id#" cfsqltype="cf_sql_varchar">
      AND est_une_couleur = 1
      AND filtre = 1
</cfquery>
```

---

Ces requêtes constituent le socle fonctionnel pour la gestion des attributs produits dans Solusquare Commerce Cloud, permettant la création, l'association, la mise à jour et la suppression des attributs, ainsi que la récupération des informations nécessaires pour l'affichage et la sélection dans l'interface back-office.

## Dépendances
Cette section liste les fichiers ColdFusion inclus dans le module Gestion des attributs de produit, précisant leur type, rôle et mode d'inclusion.

### Dépendance : `act_attribut.cfm`
*Fichier :* `act_attribut.cfm`  
*Type :* Module d'action ColdFusion  
*But :* Gérer les opérations CRUD (insert, update, delete) sur les attributs produits et leurs associations aux types de produits.

*Code de l'inclusion :* 
```coldfusion
<!--- Include test allow update --->
<cfinclude template="#request.libroot#/allow_update.cfm">

<!--- Use cas: ACTION --->
<cfswitch expression="#attributes.action#">
    <!--- INSERT --->
    <cfcase value="insert">
        <cftry>
            <cftransaction>
                <cfset tri= 1>
                <cfinclude template="#request.queryroot#/qry_get_all_pays_langue.cfm">
                <cfloop index="I" from="1" to ="#attributes.max_attributs#">
                    <cfif evaluate("attributes.attribut_id_#I#") eq "">
                        <cfmodule template="#request.libroot#/act_max_id.cfm"
                            datasource="#request.datasource#"
                            tablename="bo_attribut"
                            primarykey="attribut_id">
                        <cfset nb_insert = 0>
                        <cfloop query="qry_get_all_pays_langue">
                            <cfif isdefined("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#") and trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#")) neq "">
                                <cfset current_libelle = trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#"))>
                                <cfquery name="insert_att" datasource="#request.datasource#">
                                    INSERT INTO bo_attribut (
                                        attribut_id,
                                        pays_id,
                                        langue_id, 
                                        libelle,
                                        date_creation)
                                    VALUES (
                                        #max_id#,
                                        '#qry_get_all_pays_langue.pays_id#',
                                        '#qry_get_all_pays_langue.langue_id#',
                                        '#current_libelle#',
                                        getdate()
                                    )
                                </cfquery>
                                <cfset nb_insert = nb_insert + 1>
                            </cfif>
                        </cfloop>
                        <cfif nb_insert gt 0>
                            <cfloop index="Index" list="#attributes.type_produit_id#">
                                <cfquery name="insert_att_type_prod" datasource="#request.datasource#">
                                    INSERT INTO bo_attribut_type_produit (
                                        type_produit_id,
                                        attribut_id,
                                        tri
                                    )
                                    VALUES (
                                        #Index#,
                                        #max_id#,
                                        #tri#
                                    )
                                </cfquery>
                            </cfloop> 
                        </cfif>
                        <cfset tri = tri +1>
                    <cfelseif evaluate("attributes.attribut_id_#I#") neq "">
                        <cfloop index="Index" list="#attributes.type_produit_id#">
                            <cfquery name="insert_att_type_prod" datasource="#request.datasource#">
                                INSERT INTO bo_attribut_type_produit (
                                    type_produit_id,
                                    attribut_id,
                                    tri
                                )
                                VALUES (
                                    #Index#,
                                    #evaluate("attributes.attribut_id_#I#")#,
                                    #tri#
                                )
                            </cfquery>
                        </cfloop> 
                        <cfset tri = tri +1>
                    </cfif>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfset error = "#label_err_insert#<br/>">
                <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error insert attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- DELETE --->
    <cfcase value="delete">
        <cftry>
            <cftransaction>
                <cfquery name="delete_attribut" datasource="#request.datasource#">
                    delete from bo_attribut
                    where attribut_id = #attributes.attribut_id#
                </cfquery>
                <cfquery name="delete_attribut_prod" datasource="#request.datasource#">
                    delete from bo_attribut_type_produit
                    where attribut_id = #attributes.attribut_id#
                </cfquery>
            </cftransaction>
            <cfcatch type="database">
                <cfset error = "#label_err_delete#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- UPDATE --->
    <cfcase value="update">
        <cftry>
            <cftransaction>
                <cfloop index="i" from="1" to="#attributes.compteur#">
                    <cfif not listfindnocase(attributes.liste_langue,evaluate("langue_id_#i#"))>
                        <cfquery name="getpays" datasource="#request.datasource#">
                            select distinct pays_id from bo_pays_langue where langue_id = '#evaluate("langue_id_#i#")#' and statut & 1 = 1
                        </cfquery>
                        <cfloop query="getpays">
                            <cfset current_libelle = trim(evaluate("attributes.attribut_#i#"))>
                            <cfquery name="insert_att" datasource="#request.datasource#">
                                INSERT INTO bo_attribut (
                                    attribut_id,
                                    pays_id,
                                    langue_id, 
                                    libelle,
                                    date_creation)
                                VALUES (
                                    #attributes.attribut_id#,
                                    '#getpays.pays_id#',
                                    '#evaluate("langue_id_#i#")#',
                                    N'#current_libelle#',
                                    getdate()
                                )
                            </cfquery>
                        </cfloop>
                    <cfelse>
                        <cfset current_libelle = trim(evaluate("attributes.attribut_#i#"))>
                        <cfquery name="update_att" datasource="#request.datasource#">
                            UPDATE bo_attribut  
                                SET
                                    libelle = N'#current_libelle#', 
                                    code_ext = N'#trim(attributes.code_ext)#'
                                    <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
                                        , filtre=<cfif isdefined("attributes.filtre") and val(attributes.filtre) eq 1>1<cfelse>0</cfif>
                                    </cfif>
                                    <cfif isdefined("codeCouleurPicto") and codeCouleurPicto>
                                        , est_une_couleur=<cfif isdefined("attributes.est_une_couleur") and val(attributes.est_une_couleur) eq 1>1<cfelse>0</cfif>
                                    </cfif>
                                WHERE attribut_id = #attributes.attribut_id# 
                                    and langue_id = '#evaluate("langue_id_#i#")#'
                        </cfquery>
                    </cfif>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error update attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfset error = "#label_err_update#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
    <!--- UPDATE OPTION --->
    <cfcase value="updateoption">
        <cftry>
            <cftransaction>
                <cfinclude template="qry_get_attribut_option.cfm">
                <cfloop query="qry_get_attribut_option">
                    <cfloop index="langue_en_cours" list="#langue#">
                        <cfinclude template="qry_get_attribut_option_detail.cfm">
                        <cfif qry_get_attribut_option_detail.libelle eq "" and evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "" and evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "Non renseign">
                            <!--- Cration de l'attribut dtail --->
                            <cfset attToIns = evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                            <cfquery datasource="#request.datasource#">
                                INSERT INTO bo_attribut_detail
                                (attribut_detail_id, libelle, pays_id,langue_id
                                <cfif isdefined("attributes.attribut_group_#attribut_detail_id#")>
                                    ,attribut_group_id                                
                                </cfif>)
                                select distinct
                                    #attribut_detail_id#, 
                                    '#attToIns#', 
                                    pays_id,
                                    '#langue_en_cours#'
                                    <cfif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) neq "0">
                                        ,'#evaluate("attribut_group_#attribut_detail_id#")#'   
                                    <cfelseif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) eq "0">
                                        ,NULL                      
                                    </cfif>
                                from bo_pays_langue with(nolock)
                                where langue_id = '#langue_en_cours#'
                                    and statut & 1 = 1
                            </cfquery>
                        <cfelseif evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#") neq "Non renseign">
                            <!--- Modification de l'attribut dtail --->
                            <cfset attToUpd = evaluate("attributes.attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                            <cfset codeattToUpd = evaluate("attributes.code_#attribut_detail_id#")>
                            <cfquery datasource="#request.datasource#">
                                UPDATE bo_attribut_detail
                                SET
                                    libelle = '#attToUpd#', 
                                    code = '#trim(codeattToUpd)#'
                                    <cfif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) neq "0">
                                        ,attribut_group_id = '#evaluate("attribut_group_#attribut_detail_id#")#'    
                                    <cfelseif isdefined("attributes.attribut_group_#attribut_detail_id#") and val(evaluate("attribut_group_#attribut_detail_id#")) eq "0">  
                                        ,attribut_group_id = NULL                         
                                    </cfif>
                                    <cfif codeCouleurPicto>
                                        <cfif isdefined("attributes.degrade_#attribut_detail_id#") 
                                            AND isdefined("attributes.liste_code_couleur_picto_#attribut_detail_id#")
                                            AND isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                                            <cfset liste_couleur = evaluate("attributes.liste_code_couleur_picto_#attribut_detail_id#")>
                                            <cfif Len(liste_couleur) eq 0 OR liste_couleur eq "##"><cfset liste_couleur = "##000000"></cfif>
                                            <cfif Listlen(liste_couleur,';') gte 2>
                                                <cfif Len(trim(ListGetAt(liste_couleur,2,';'))) eq 0>
                                                    <cfset liste_couleur = ListGetAt(liste_couleur,1,';')>
                                                <cfelse>
                                                    <cfset liste_couleur = ListGetAt(liste_couleur,1,';') & ";" & ListGetAt(liste_couleur,2,';')>
                                                </cfif>
                                            </cfif>
                                            ,code_couleur = '#liste_couleur#'
                                        <cfelseif isdefined("attributes.code_couleur_picto_#attribut_detail_id#")>
                                            ,code_couleur = '#evaluate("attributes.code_couleur_picto_#attribut_detail_id#")#'
                                        </cfif>
                                    </cfif>
                                WHERE attribut_detail_id = #attribut_detail_id#
                                AND langue_id = '#langue_en_cours#'
                            </cfquery>
                        </cfif>
                    </cfloop>
                </cfloop>
            </cftransaction>
            <cfcatch type="database">
                <cfmail type="html" to="dev@solusquare.com" from="dev@solusquare.com" subject="BO - #uCase('#server.sq.machine_prefixe#')# - Error update option attribut">
                    <cfdump var="#cfcatch#">
                </cfmail>
                <cfset error = "#label_err_update#<br/>">
                <cfinclude template="#request.libroot#/debug.cfm">
            </cfcatch>
        </cftry>
    </cfcase>
</cfswitch>
```

---

### Dépendance : `act_color_group.cfm`
*Fichier :* `act_color_group.cfm`  
*Type :* Module d'action ColdFusion  
*But :* Gérer la création, mise à jour et suppression des groupes de couleurs associés aux attributs.

*Code de l'inclusion :* 
```coldfusion
<cfinclude template="#request.queryroot#/qry_get_all_langue_active.cfm">

<cfif fuseaction eq "updateColorGroup">
    <cfloop query="qry_get_all_langue_active">
        <CFQUERY NAME="qry_color_group_update" DATASOURCE="#request.datasource#">
            update bo_attribut_detail_cat_group
            set couleur = '#evaluate("ATTRIBUTES.couleur_#qry_get_all_langue_active.langue_id#")#',
                code_ext = '#ATTRIBUTES.code_ext#',
                couleur_url = '#ATTRIBUTES.couleur_url#',
                code_couleur = '#ATTRIBUTES.code_couleur#',
                ordre = #ATTRIBUTES.ordre#
            where attribut_group_id = #ATTRIBUTES.attribut_group_id#
                and langue_id = '#qry_get_all_langue_active.langue_id#'
        </CFQUERY>
    </cfloop>
<cfelseif fuseaction eq "saveColorGroup">
    <cfset i = 0>

    <CFQUERY NAME="qry_color_group_save" DATASOURCE="#request.datasource#">
        ;with cte_next_att_grp_id as (
            select max(attribut_group_id) + 1 as next_att_grp_id from bo_attribut_detail_cat_group
        )
        insert into bo_attribut_detail_cat_group (attribut_group_id, couleur, ordre, code_ext, couleur_url, code_couleur, langue_id) values
        <cfloop query="qry_get_all_langue_active">
            <cfset i+=1>
        (
            (select next_att_grp_id from cte_next_att_grp_id),
            '#evaluate("ATTRIBUTES.couleur_#qry_get_all_langue_active.langue_id#")#',
            #ATTRIBUTES.ordre#,
            #ATTRIBUTES.code_ext#,
            #ATTRIBUTES.couleur_url#,
            #ATTRIBUTES.code_couleur#,
            '#qry_get_all_langue_active.langue_id#'
        ) <cfif i lt qry_get_all_langue_active.recordCount>,</cfif>
        </cfloop>
    </CFQUERY>

    <CFQUERY NAME="get_max_attribut_group_id" DATASOURCE="#request.datasource#">
        select max(attribut_group_id) attribut_group_id from bo_attribut_detail_cat_group
    </CFQUERY>
    <cfset ATTRIBUTES.attribut_group_id = get_max_attribut_group_id.attribut_group_id>

<cfelseif fuseaction eq "deleteColorGroup">
    <CFQUERY NAME="qry_color_group_delete" DATASOURCE="#request.datasource#">
        delete from bo_attribut_detail_cat_group
        where attribut_group_id = #ATTRIBUTES.attribut_group_id#
    </CFQUERY>
</cfif>
```

---

### Dépendance : `dsp_attribut_form.cfm`
*Fichier :* `dsp_attribut_form.cfm`  
*Type :* Template d'affichage ColdFusion  
*But :* Afficher le formulaire d'ajout d'attributs avec gestion multilingue et association aux types de produits.

*Code de l'inclusion :* 
```coldfusion
<cfset FIELDLIST = "type_produit_id">
<cfset max_attributs = 2>
<cfinclude template="#request.queryroot#/qry_get_all_attribut.cfm">
<cfinclude template="qry_get_langue.cfm">

<cfloop index="I" from="1" to="#max_attributs#">
    <cfset FIELDLIST = FIELDLIST &  ",attribut_id_#I#">
    <cfoutput query="qry_get_langue">
        <cfset FIELDLIST = FIELDLIST &  ",attribut_#langue_id#_#I#">
    </cfoutput>
</cfloop>
<cfset liste_attrib=valuelist(qry_get_all_attribut.libelle)>
<cfif ATTRIBUTES.FUSEACTION IS "new"> 
    <cfloop list="#fieldlist#" index="counter">
        <cfset TEMP = SETVARIABLE("#counter#", "")>
    </cfloop>
    
<cfelseif ATTRIBUTES.FUSEACTION IS "form">
    <cfloop list="#fieldlist#" index="counter">
        <cfset TEMP = SETVARIABLE("#counter#", "#evaluate("attributes." & "#COUNTER#")#")>
    </cfloop>    
</cfif>

<cfoutput>
    <cfif isdefined("attributes.error") and trim(attributes.error) neq "">
        <div class="notification msgerror">
            <p>#attributes.error#</p>
        </div>
    </cfif>
        
    <div class="contenttitle">
        <h2 class="form">
            <span>#label_ajouter# #label_header#</span>
        </h2>
    </div>
    <div class="notification msginfo">
        <p>
            #label_msg_ajout_attribut_1#<br>
            #label_msg_ajout_attribut_2#<br>
            #label_msg_ajout_attribut_3#<br>
        </p>
    </div>
    
    <!--- Entry form --->
    <cfform class="stdform stdform2" name="formulaire" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
        <input type ="hidden" name="criteria" value=""/>
        <input type="hidden" name="fuseaction" value="saveAttribut"/>
        <input type="hidden" name="liste_attrib" value="#liste_attrib#"/>
        <input type="hidden" name="max_attributs" value="#max_attributs#">
        <div class="notification msgalert">
            <p>#label_valeur_obligatoire#</p>
        </div>
        <!--- Field: categorie.cat_nom --->
        <p>
            <label class="libelle <cfif listfindnocase("#attributes.requiredfields#","type_produit_id")>requis</cfif>"><cfoutput>#label_types_produits_associes# :</cfoutput></label>
            <span class="field">
                <cfinclude template="qry_type_produit_sans_attribut.cfm">
                <cfselect name="type_produit_id" query="qry_type_produit_sans_attribut" value="type_produit_id" display="libelle" selected="#type_produit_id#" multiple class="selectpicker" data-live-search="true" title="" data-size="6"></cfselect>
            </span>
        </p>
        <div class="par">
            <label>&nbsp;</label>
            <div class="field">
                <div class="contenttitle">
                    <h2 class="form">
                        <span>#label_header#</span>
                    </h2>
                </div>
                <table class="table table-striped table-bordered">
                    <thead>
                        <th class="head0">&nbsp;</th>
                        <th class="head0">&nbsp;</th>
                        <cfset cpt = 0>
                        <cfloop query="qry_get_langue">
                            <cfset cpt = cpt + 1>
                            <th class="head0">
                                <img src="#request.imagesroot#/drapeaux/png/#qry_get_langue.langue_id#.png" alt="#qry_get_langue.langue_id#" class="drapeau"/>
                            </th>
                        </cfloop>
                    </thead>
                    <thead>
                        <th class="head0">#label_tri#</th>
                        <th class="head0">#label_attribut_existant#</th>
                        <cfset cpt = 0>
                        <cfloop query="qry_get_langue">
                            <cfset cpt = cpt + 1>
                            <th class="head0">#label_nouvel_attribut#</th>
                        </cfloop>
                    </thead>
                    <cfloop index="I" from="1" to="#max_attributs#">
                        <tr>
                            <td class="center">#i#</td>
                            <td class="center">
                                <cfselect name="attribut_id_#I#" query="qry_get_all_attribut" value="attribut_id" display="libelle" selected="#evaluate("attribut_id_#I#")#">
                                    <option value="" <cfif evaluate("attribut_id_#I#") is "">selected="selected"</cfif>> --- <cfoutput>#label_selectionnez#</cfoutput> --- </option>
                                </cfselect>
                            </td>
                            <cfloop query="qry_get_langue">
                                <td class="center">
                                    <input type="text" name="attribut_#langue_id#_#I#" value="#evaluate("attribut_#langue_id#_#I#")#" class="mediuminput"/>
                                    <input type="hidden" name="langue_id_#I#" value="#langue_id#">
                                </td>
                            </cfloop>
                        </tr>
                    </cfloop>
                </table>
            </div>
        </div>    
        <br>
        <ul class="buttonlist">
            <li>
                <button type="submit" class="btn btn-success" value="#label_btn_valider#">#label_btn_valider#</button>
            </li>
            <li>
                <button type="button" class="btn btn-danger" onclick="javascript:window.location='#cgi.script_name#?FuseAction=searchingAttribut';">#label_btn_annuler#</button>
            </li>
        </ul>
    </cfform>
</cfoutput>
```

---

### Dépendance : `dsp_attribut_option_edit_form.cfm`
*Fichier :* `dsp_attribut_option_edit_form.cfm`  
*Type :* Template d'affichage ColdFusion  
*But :* Afficher et gérer le formulaire d'édition des options des attributs, avec gestion multilingue et couleurs.

*Code de l'inclusion :* 
```coldfusion
<cfset FIELDLIST = "">
<cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>
    <cfinclude template="qry_get_attribut_couleur_cata.cfm">
</cfif>

<cfif ATTRIBUTES.FUSEACTION IS "edit"> 
    <cfset pays = "">
    <cfinclude template="qry_get_attribut_all_langue.cfm">
    <cfset nb_col = 1>
    <cfloop query="qry_get_attribut_all_langue">
        <cfset langue = valuelist(qry_get_attribut_all_langue.langue_id)>
        
        <cfif isdefined("attribut_libelle")>
            <cfset attribut_libelle = attribut_libelle & " / " & qry_get_attribut_all_langue.libelle>
        <cfelse>
            <cfset attribut_libelle = qry_get_attribut_all_langue.libelle>
        </cfif>
        <cfset nb_col = nb_col+1>
    </cfloop>
    <cfset est_une_couleur = 0>
    <cfif codeCouleurPicto AND isdefined("qry_get_attribut_all_langue.est_une_couleur") AND val(qry_get_attribut_all_langue.est_une_couleur) eq 1>
        <cfset est_une_couleur = 1>
    </cfif> 
<cfelseif ATTRIBUTES.FUSEACTION IS "form">
    <cfset pays = attributes.pays>
    <cfset nb_col = attributes.nb_col>
    <cfset attribut_libelle = attributes.attribut_libelle>
</cfif>

<cfif isdefined("url.a_modifier")>
    <cfset attributes.a_modifier = url.a_modifier>
<cfelseif isdefined("form.a_modifier")>
    <cfset attributes.a_modifier = form.a_modifier>
</cfif>

<cfif isdefined("form.une_option")>
    <cfset attributes.une_option = form.une_option>
</cfif>

<cfoutput>

<cfif isdefined("attributes.error") and trim(attributes.error) neq "">
    <div class="notification msgerror">
        <div class="cheat"></div>
        <p>#attributes.error#</p>
    </div>
</cfif>

<div class="contenttitle">
    <h2 class="form">
        <span>
            #label_editer_option#  #label_attribut# : #attribut_libelle# (#label_attribut_id# :&nbsp;&nbsp;#attribut_id#)
        </span>
    </h2>
</div>

<cfform class="stdform stdform2" name="search_form" id="search_form" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
    <input type="hidden" name="fuseaction" value="editAttributOption"/>
    <input type ="hidden" name="attribut_id" value="#attribut_id#"/>
    <input type ="hidden" name="criteria" value="#attributes.criteria#"/>
    <input type ="hidden" name="langue" value="#langue#"/>
    <input type ="hidden" name="nb_col" value="#nb_col#"/>
    <input type ="hidden" name="attribut_libelle" value="#attribut_libelle#"/>
    <input type ="hidden" name="a_modifier" value="0"/>
    <input type ="hidden" name="est_une_couleur" value="#est_une_couleur#"/>
    <p>
        <label>#label_chercher_une_valeur#</label>
        <span class="field">
            <input type="text" name="une_option" id="une_option" value="#attributes.une_option#">
            <cfinput class="btn btn-primary" type="Submit" name="SubmitSearchForm" id="SubmitSearchForm" value="#label_rechercher#">
            <cfinput class="btn btn-info" type="Button" name="ResetSearchForm" value="#label_reset_recherche#" onclick="jQuery('##une_option').val('');jQuery('##search_form').submit();">
        </span>
    </p>
</cfform>

<cfform class="stdform stdform2" name="formulaire" action="#cgi.script_name#" method="post" onsubmit="return recherche_input()">
    <input type="hidden" name="fuseaction" value="updateAttributOption"/>
    <input type ="hidden" name="attribut_id" value="#attribut_id#"/>
    <input type ="hidden" name="criteria" value="#attributes.criteria#"/>
    <input type ="hidden" name="langue" value="#langue#"/>
    <input type ="hidden" name="nb_col" value="#nb_col#"/>
    <input type ="hidden" name="attribut_libelle" value="#attribut_libelle#"/>
    <input type ="hidden" name="a_modifier" value="#attributes.a_modifier#"/>
    <input type="hidden" name="une_option" value="#attributes.une_option#">
    <input type ="hidden" name="est_une_couleur" value="#est_une_couleur#"/>
    <cfset compt = 1>
        
    <cfloop list="#attribut_libelle#" delimiters=" / " index="index">
        <input type ="hidden" name="attribut_libelle_#compt#" value="#index#"/>
        <cfset compt = compt + 1>
    </cfloop>  
     
    <div class="notification msgalert">
        <p>
            #label_valeur_obligatoire# #label_msg_description_langues#
        </p>
    </div>
    <div  style="overflow:scroll">
        <table  class="table table-striped table-bordered" >
            <thead>
                <th>#label_attribut_option_num#</th>
                <th>#label_code#</th>
                <cfif codeCouleurPicto AND val(est_une_couleur) eq 1>
                    <cfif isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                    <th>#LABEL_BICOLORE#</th>
                    </cfif>
                    <th>Code couleur Picto</th>
                </cfif>
               <cfloop index="langue_en_cours" list="#langue#">
                    <th>#label_libelle# <img src="#request.imagesroot#/drapeaux/png/#langue_en_cours#.png" alt="#langue_en_cours#" class="drapeau"/></th>
                </cfloop>
                <cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>
                    <th>#label_groupe#</th>
                </cfif>
            </thead>
            <cfinclude template="qry_get_attribut_option.cfm">
            <cfloop query="qry_get_attribut_option">
                <tr>
                    <td class="contenu centre gras">#attribut_detail_id# <cfif isdefined("code")> (#code#)</cfif></td>
                    <td class="contenu centre gras">
                        <cfif isdefined("code_#attribut_detail_id#")>
                            <input type="text" name="code_#attribut_detail_id#" value="#evaluate("code_#attribut_detail_id#")#">
                        <cfelse>
                            <cfif qry_get_attribut_option.code neq "">
                                <cfinput type="text" name="code_#attribut_detail_id#" value="#qry_get_attribut_option.code#">
                            <cfelse>
                                <input type="text" name="code_#attribut_detail_id#" value="">
                            </cfif>
                        </cfif>
                    </td>
                    <cfif codeCouleurPicto AND val(est_une_couleur) eq 1>
                        <cfif isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                            <td class="contenu centre gras">
                                <input type="checkbox" class="degrade" id="degrade_#attribut_detail_id#" name="degrade_#attribut_detail_id#" attribut-detail-id="#attribut_detail_id#" value=""
                                    <cfif listlen(qry_get_attribut_option.code_couleur,';') gt 1> checked="checked" </cfif>>
                            </td>
                        </cfif>
                        <td class="contenu centre gras">
                            <div class="flex_left" style="width: 150px;">
                                <cfset bicolore = false>
                                <cfif listlen(qry_get_attribut_option.code_couleur,';') gt 1 AND isdefined("param_client.aff_spe_Frago") AND param_client.aff_spe_Frago>
                                    <cfset bicolore = true>
                                    <style>
                                        ##fake-colorpicker-element_#attribut_detail_id# { height: 35px; width: 40px; cursor: default; position: relative; border: 1px solid ##d6d6d6; border-radius: 3px; }
                                        ##fake-colorpicker-element_#attribut_detail_id#:before { display: block; content: ""; height: 25px; width: 30px; position: absolute; top: 4px; left: 4px; border: 1px solid ##d6d6d6; background: linear-gradient(-60deg, #ListGetAt(qry_get_attribut_option.code_couleur,2,";")#, #ListGetAt(qry_get_attribut_option.code_couleur,2,";")# 50%, #ListGetAt(qry_get_attribut_option.code_couleur,1,";")# 50%); }
                                    </style>
                                    <input type="text" style="height: 35px; width: 100px;" id="liste_code_couleur_picto_#attribut_detail_id#" name="liste_code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#" size="20"/>
                                    <div id="fake-colorpicker-element_#attribut_detail_id#"></div>
                                <cfelse>
                                    <input type="text" style="height: 35px; width: 100px;display:none;" id="liste_code_couleur_picto_#attribut_detail_id#" name="liste_code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#"/>
                                </cfif>
                                <input type="text"  id="code_couleur_picto_#attribut_detail_id#"class="textcolor"  name="code_couleur_picto_#attribut_detail_id#" value="#qry_get_attribut_option.code_couleur#" size="7" maxlength="7" onchange="change_color_input(this)" <cfif bicolore> style="display:none;" </cfif>/>
                                <input type="color" id="colorpicker_#attribut_detail_id#" value="<cfif trim(qry_get_attribut_option.code_couleur) neq "">#qry_get_attribut_option.code_couleur#<cfelse>##000000</cfif>" style="height: 35px;width: 70px; <cfif bicolore>display:none;</cfif>" disabled  >
                            </div>
                        </td>
                    </cfif>
                    <cfloop index="langue_en_cours" list="#langue#">
                        <cfinclude template="qry_get_attribut_option_detail.cfm">
                        <td>             
                            <cfif isdefined("attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")>
                                <input type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value="#evaluate("attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#")#" style="width:auto;max-width:150px">
                            <cfelse>
                                <cfif qry_get_attribut_option_detail.libelle neq "">
                                    <cfinput type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value="#qry_get_attribut_option_detail.libelle#"  style="width:auto;max-width:150px">
                                    <input type="hidden" name="attribut_detail_libelle_old_#attribut_detail_id#_#langue_en_cours#" value="#qry_get_attribut_option_detail.libelle#"/>
                                <cfelse>
                                    <input type="text" name="attribut_detail_libelle_#attribut_detail_id#_#langue_en_cours#" value=""  style="width:auto;max-width:150px">
                                </cfif>
                            </cfif>
                        </td>
                    </cfloop>
                    <cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur AND val(est_une_couleur) eq 1 or request.datasource eq "bo_armandt" or request.datasource eq "bo_edji" or request.datasource eq "bo_toscane">
                        <td style="text-align:center;">
                            <cfif isdefined("attributes.attribut_group_#attribut_detail_id#")>
                                <cfset sel = evaluate("attributes.attribut_group_#attribut_detail_id#")>
                            <cfelse>
                                <cfset sel = qry_get_attribut_option_detail.attribut_group_id>
                            </cfif>
                            <cfselect name="attribut_group_#attribut_detail_id#" query="get_attribut_couleur_cata" value="attribut_group_id" display="couleur" selected="#sel#" class="selectpicker" data-live-search="true">
                                <option value="" <cfif val(sel) eq "0"> selected="selected"</cfif>> --- #label_selectionnez# --- </option>
                            </cfselect>    
                        </td>
                    </cfif>
                </tr>    
            </cfloop>
            <cfif qry_get_attribut_option.recordcount eq 0>
                <td colspan="#nb_col#" class="contenu centre">
                    <span class="rouge gras">#label_aucune_option#</span>
                </td>
            </cfif>
        </table>
    </div>

    <script>
        // Prevent special characters in attribute code
        jQuery('input[name^=code_]').keypress(function(e) {
            let valid = false;
            if ((e.charCode >= 48 && e.charCode <= 57) || (e.charCode >= 65 && e.charCode <= 90) || (e.charCode >= 97 && e.charCode <= 122))
                valid = true;
            else if (e.charCode == 95 && !e.target.value.includes('_'))
                valid = true;

            if (!valid)
                e.preventDefault();
        });
    </script>

    <cfif codeCouleurPicto>
        <script>
            <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
            jQuery('.degrade').click(function() {
                var attribut_detail_id = jQuery(this).attr("attribut-detail-id");
                if (!isNaN(attribut_detail_id) && attribut_detail_id > 0) {
                    if (jQuery(this).is(':checked')) {
                        jQuery("##code_couleur_picto_" + attribut_detail_id).hide();
                        jQuery("##colorpicker_" + attribut_detail_id).hide();
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).val(jQuery("##colorpicker_" + attribut_detail_id).val());
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).show();
                    }
                    else
                    {
                        jQuery("##code_couleur_picto_" + attribut_detail_id).show();
                        jQuery("##colorpicker_" + attribut_detail_id).show();
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).val("");
                        jQuery("##liste_code_couleur_picto_" + attribut_detail_id).hide();
                        jQuery("##fake-colorpicker-element_" + attribut_detail_id).hide();
                    }
                }
            });
            </cfif>
            
            <!---Init Color Picker--->
                if( jQuery(".textcolor").length > 0 )
                    jQuery(function () { 
                        <cfloop query="qry_get_attribut_option">
                            jQuery('##code_couleur_picto_#attribut_detail_id#').colorpicker({
                                <cfif trim(qry_get_attribut_option.code_couleur) neq "">
                                color:'#qry_get_attribut_option.code_couleur#',
                                <cfelse>
                                color: '##000000',
                                </cfif> 
                                useAlpha:false ,
                                align:'left'});
                            <cfif trim(qry_get_attribut_option.code_couleur) eq "">
                            jQuery('##code_couleur_picto_#attribut_detail_id#').val('');
                            </cfif>
                        </cfloop> 
                    });
                
                function change_color_input(element)
                {
                    const regex_color = new RegExp('^##([a-fA-F0-9]{6})$');

                    if (regex_color.test(jQuery(element).val()))
                    {
                        jQuery(element).css('border','');
                        jQuery(element).next('input').val(jQuery(element).val());
                    }
                    else
                    {
                        //jQuery(element).css('border','1px solid red');
                        jQuery(element).val('');
                        jQuery(element).next('input').val('##000000');
                    }
                }
        </script>
    </cfif>
    <br>
    <ul class="buttonlist">
        <li>
            <button type="submit" class="btn btn-success" value="#label_btn_valider#">#label_btn_valider#</button>
        </li>
        <li>
            <button type="button" class="btn btn-danger" onclick="javascript:window.location='#cgi.script_name#?FuseAction=displayAttribut&criteria=#URLEncodedFormat(attributes.criteria)#';">#label_btn_annuler#</button>
        </li>
    </ul>
</cfform>
</cfoutput>
```

---

### Dépendance : `index.cfm`
*Fichier :* `index.cfm`  
*Type :* Contrôleur ColdFusion principal  
*But :* Point d'entrée du module, gère la logique de routage des actions (FuseAction) liées aux attributs et groupes de couleurs.

*Code de l'inclusion :* 
```coldfusion
<cfmodule template="#request.cfroot#/users/app_secure.cfm">
<cfinclude template="#request.cfroot#/users/app_verif_fuseaction.cfm">
<cfmodule template="#request.cfroot#/app_lang.cfm" lang="#client.langue_id#" dir="attributs">

<!---Code couleur du Picto d'un attribut--->
<cfset codeCouleurPicto = false>
<cfif SQL_Existe( request.datasource, "bo_attribut_detail" , "code_couleur" )>
    <cfset codeCouleurPicto = true>
</cfif>

<!--- Ajout colonnes couleur si manquantes --->
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "code_ext" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add code_ext nvarchar(50)
    </cfquery>
</cfif>
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "couleur_url" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add couleur_url nvarchar(200)
    </cfquery>
</cfif>
<cfif not SQL_Existe( request.datasource, "bo_attribut_detail_cat_group" , "code_couleur" )>
    <cfquery name="addColorColumns" datasource="#request.datasource#">
        alter table bo_attribut_detail_cat_group
        add code_couleur nvarchar(50)
    </cfquery>
</cfif>

<cfparam name="attributes.fuseaction" default="">
<cfparam name="attributes.a_modifier" default="0">
<cfparam name="attributes.une_option" default="0">
<cfswitch expression="#attributes.fuseaction#">
    <!--- FuseActions pour attributegories --->
    <cfcase value="displayAttribut">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="detailAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut_detail.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="addAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="new">
        <cfset attributes.attribut_id="">
        <cfset attributes.error="">
        <cfset attributes.requiredfields="type_produit_id">
        <cfinclude template="dsp_attribut_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="editAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        
        <cfinclude template="dsp_attribut_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="editAttributOption">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        
        <cfinclude template="dsp_attribut_option_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="deleteAttribut">
        <cfset attributes.action="delete">
        <cfinclude template="err_attribut_supprime.cfm">
        <cfif ERROR eq "">
            <cfinclude template="act_attribut.cfm">
        </cfif>
        <cfset attributes.error="#error#">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="saveAttribut">
        <cfset attributes.requiredfields="type_produit_id">
        <cfinclude template="err_attribut_entry.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            <cfinclude template="dsp_attribut_form.cfm">
        <cfelse>
            <cfset attributes.action="insert">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="new">
            <cfset attributes.error="">
            <cfset showmessage=true>
            <cfinclude template="dsp_attribut_search.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="updateAttribut">
        <cfset attributes.requiredfields="">
        <cfinclude template="err_attribut_edit.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            <cfinclude template="dsp_attribut_edit_form.cfm">
        <cfelse>
            <cfset attributes.action="update">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="new">
            <cfset attributes.error="">
            <cfinclude template="dsp_attribut.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="updateAttributOption">
        <cfset attributes.requiredfields="">
        <cfinclude template="err_attribut_option_edit.cfm">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfif ERROR neq "">
            <cfset attributes.Fuseaction="form">
            <cfset attributes.error="#error#">
            
            
            <cfinclude template="dsp_attribut_option_edit_form.cfm">
        <cfelse>
            <cfset attributes.action="updateoption">
            <cfinclude template="act_attribut.cfm">
            <cfset attributes.fuseaction="edit">
            <cfset attributes.error="">
            <cfinclude template="dsp_attribut_option_edit_form.cfm">
        </cfif>
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="searchAttribut">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_search.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="searchingAttribut">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">

    </cfcase>
    <cfcase value="addColorGroup">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfset attributes.requiredfields="couleur,langue_id">
        <cfinclude template="dsp_color_group_add.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="searchColorGroup">    
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.fuseaction="new">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group_search.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="searchingColorGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="editAttributGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfset attributes.Fuseaction="edit">
        <cfset attributes.error="">
        <cfinclude template="dsp_attribut_group_edit_form.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
    <cfcase value="saveColorGroup,deleteColorGroup,updateColorGroup">
        <cfinclude template="dsp_attribut_header.cfm">
        <cfinclude template="act_color_group.cfm">
        <cfinclude template="#request.libroot#/act_results.cfm">
        <cfparam name="attributes.criteria" default="#criteria#">
        <cfset attributes.error="">
        <cfinclude template="dsp_color_group.cfm">
        <cfinclude template="dsp_attribut_footer.cfm">
    </cfcase>
</cfswitch>
```

---

### Dépendance : `qry_get_attribut_all_langue.cfm`
*Fichier :* `qry_get_attribut_all_langue.cfm`  
*Type :* Requête ColdFusion (SQL)  
*But :* Récupérer les libellés d'un attribut dans toutes les langues disponibles.

*Code de l'inclusion :* 
```coldfusion
<cfquery name="qry_get_attribut_all_langue" datasource="#request.datasource#">
    SELECT
        DISTINCT
            attribut_id, langue_id, libelle, code_ext
            <cfif isdefined("param_client.aff_spe_Frago") and param_client.aff_spe_Frago>
                , filtre
            </cfif>
            <cfif isdefined("codeCouleurPicto") and codeCouleurPicto>
                , ISNULL(est_une_couleur,0) AS est_une_couleur
            </cfif>
    FROM bo_attribut WITH (NOLOCK)
    WHERE attribut_id = #attributes.attribut_id#
</cfquery>
```

---

### Dépendance : `qry_get_attribut_option.cfm`
*Fichier :* `qry_get_attribut_option.cfm`  
*Type :* Requête ColdFusion (SQL)  
*But :* Récupérer les options associées à un attribut, avec gestion des langues et filtres.

*Code de l'inclusion :* 
```coldfusion
<CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
    SELECT
        distinct
            bo_attribut_detail.attribut_detail_id, 
            bo_attribut_detail.libelle,
            bo_attribut_detail.langue_id, 
            bo_attribut_detail.code,
            bo_attribut_detail.ordre,
            bo_attribut_detail.attribut_group_id,
            bo_attribut_detail.code_group,
            bo_attribut_detail.libelle_group
            <cfif codeCouleurPicto>
                , code_couleur
            </cfif>
    FROM bo_attribut_detail  with (nolock) 
    WHERE
        (
            bo_attribut_detail.attribut_id = #attributes.attribut_id#
            OR 
            bo_attribut_detail.attribut_detail_id IN  
            ( SELECT attribut_detail_id FROM bo_attribut_detail_option with (nolock) WHERE attribut_id = #attributes.attribut_id# )
        )
        and bo_attribut_detail.langue_id='#request.langue_base#' 
        <cfif trim(attributes.une_option) neq "" and trim(attributes.une_option) neq "0">
            and 
            (
                <cfif val(attributes.une_option) gt 0>
                    bo_attribut_detail.attribut_detail_id=#val(attributes.une_option)#
                    OR
                </cfif>
                bo_attribut_detail.libelle like '%#attributes.une_option#%'
            )
        </cfif>
    order by
        bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
</CFQUERY>

<cfif qry_get_attribut_option.recordcount eq 0>
    <CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
        SELECT
            distinct
                <cfif attributes.a_modifier eq 1> top 20 </cfif>
                bo_attribut_detail.attribut_detail_id, 
                bo_attribut_detail.libelle,
                bo_attribut_detail.langue_id, 
                bo_attribut_detail.code,
                bo_attribut_detail.ordre,
                bo_attribut_detail.attribut_group_id,
                bo_attribut_detail.code_group,
                bo_attribut_detail.libelle_group
            FROM bo_attribut_detail_option  with (nolock) 
            left join bo_attribut_detail    with (nolock) on bo_attribut_detail.attribut_detail_id = bo_attribut_detail_option.attribut_detail_id
            WHERE
                bo_attribut_detail_option.attribut_id = #attributes.attribut_id# 
                and bo_attribut_detail.langue_id='#request.langue_base#' 
                <cfif trim(attributes.une_option) neq "" and trim(attributes.une_option) neq "0">
                    and 
                    (
                        <cfif val(attributes.une_option) gt 0>
                            bo_attribut_detail.attribut_detail_id=#val(attributes.une_option)#
                            OR
                        </cfif>
                        bo_attribut_detail.libelle like '%#attributes.une_option#%'
                    )
                </cfif>
            order by
                bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
    </CFQUERY>
</cfif>
```

---

### Dépendance : `qry_get_attribut_option_detail.cfm`
*Fichier :* `qry_get_attribut_option_detail.cfm`  
*Type :* Requête ColdFusion (SQL)  
*But :* Récupérer les détails d'une option d'attribut pour une langue donnée.

*Code de l'inclusion :* 
```coldfusion
<CFQUERY NAME="qry_get_attribut_option_detail" DATASOURCE="#request.datasource#">
    SELECT distinct attribut_detail_id,libelle,<cfif isdefined("langue_en_cours")>langue_id<cfelse>pays_id</cfif><cfif isdefined("param_client.groupe_couleur") and param_client.groupe_couleur>,attribut_group_id,code</cfif>
    FROM bo_attribut_detail WITH (NOLOCK)
    WHERE attribut_detail_id = #qry_get_attribut_option.attribut_detail_id#
    <cfif isdefined("langue_en_cours")>
        AND langue_id = '#langue_en_cours#'
    <cfelse>
        AND pays_id = '#liste_pays_id#'
    </cfif>
</CFQUERY>
```

---

### Dépendance : `qry_get_liste_type_produit.cfm`
*Fichier :* `qry_get_liste_type_produit.cfm`  
*Type :* Requête ColdFusion (SQL)  
*But :* Récupérer la liste des types de produits associés à un attribut.

*Code de l'inclusion :* 
```coldfusion
<CFQUERY NAME="qry_get_liste_type_produit" DATASOURCE="#request.datasource#">
    SELECT distinct tp.type_produit_id,tp.libelle
    FROM ud_type_produit tp                  with (nolock)
    inner join bo_attribut_type_produit atp  with (nolock) on atp.type_produit_id = tp.type_produit_id
    WHERE atp.attribut_id = #attributes.attribut_id#
        and tp.pays_id = '#request.pays_maitre#'
    ORDER BY tp.libelle
</CFQUERY>
```

---

### Dépendance : `qry_type_produit_sans_attribut.cfm`
*Fichier :* `qry_type_produit_sans_attribut.cfm`  
*Type :* Requête ColdFusion (SQL)  
*But :* Récupérer les types de produits qui ne sont pas encore associés à un attribut.

*Code de l'inclusion :* 
```coldfusion
<CFQUERY NAME="qry_type_produit_sans_attribut" DATASOURCE="#request.datasource#">
    SELECT DISTINCT ud_type_produit.pays_id + ' - ' + isnull(c2.cat_nom, 'NC') + ' / ' + ISNULL(c1.cat_nom, 'NC') + ' / ' +  ud_type_produit.libelle + ' (ID : ' + cast(ud_type_produit.type_produit_id as varchar) + ')' as libelle , 
            ud_type_produit.type_produit_id
    FROM ud_type_produit WITH(NOLOCK)
    LEFT JOIN bo_type_produit_categorie WITH(NOLOCK) ON bo_type_produit_categorie.type_produit_id=ud_type_produit.type_produit_id
                                                                    AND bo_type_produit_categorie.pays_id=ud_type_produit.pays_id
    LEFT JOIN ud_categorie c1             WITH(NOLOCK) ON c1.pays_id=ud_type_produit.pays_id
                                                                    AND c1.cat_id = bo_type_produit_categorie.cat_id
    LEFT JOIN ud_categorie c2             WITH(NOLOCK) ON c2.cat_id=c1.parent_id
                                                                      AND c2.pays_id=ud_type_produit.pays_id
    left join bo_attribut_type_produit atp  with (nolock) on atp.type_produit_id = ud_type_produit.type_produit_id
    WHERE atp.type_produit_id is null and  ud_type_produit.pays_id = '#request.pays_base#'
    ORDER BY libelle
</CFQUERY>
```

---

## Résumé
Le module Gestion des attributs de produit repose principalement sur des fichiers ColdFusion qui gèrent :
- Les actions CRUD sur les attributs (`act_attribut.cfm`),
- La gestion des groupes de couleurs liés aux attributs (`act_color_group.cfm`),
- Les interfaces utilisateur pour la création, modification et recherche d'attributs et options (`dsp_*.cfm`),
- Les requêtes SQL ColdFusion pour récupérer les données nécessaires (`qry_*.cfm`),
- Le contrôleur principal `index.cfm` qui orchestre les différentes actions selon le paramètre `fuseaction`.

Ces dépendances sont incluses via `<cfinclude>` ou `<cfmodule>` et utilisent la base de données pour stocker et récupérer les informations multilingues et multi-pays des attributs produits.

## Gestion d'erreurs
Cette section décrit la gestion des erreurs dans le module de gestion des attributs produits, assurant la robustesse lors des opérations CRUD (création, mise à jour, suppression) et la cohérence des données multilingues.

### Bloc : Insertion d'attributs
*Fichier :* `act_attribut.cfm` (lignes 16-91)  
*Erreurs traitée :*  
- Erreur base de données lors de l'insertion d'attributs multilingues et association aux types de produits.  
*Comportement :*  
- Capture l'erreur via `<cfcatch type="database">`.  
- Envoi d'un mail d'alerte aux développeurs avec dump de l'erreur.  
- Affichage d'un debug via inclusion d'un template.  
*Propagation des erreurs :*  
- L'erreur est stockée dans la variable `error` et remontée dans l'interface.  
*Améliorations & Optimisations :*  
- Centraliser la gestion des erreurs pour éviter répétitions.  
- Ajouter des logs persistants pour audit.  
- Prévoir des messages utilisateurs plus explicites.  

*Code de l'inclusion :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- boucle insertion attributs multilingues et association types produits --->
    </cftransaction>
    <cfcatch type="database">
        <cfset error = "#label_err_insert#<br/>">
        <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error insert attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloc : Suppression d'attribut
*Fichier :* `act_attribut.cfm` (lignes 95-110)  
*Erreurs traitée :*  
- Erreur base de données lors de la suppression d'un attribut et ses associations.  
*Comportement :*  
- Capture l'erreur via `<cfcatch type="database">`.  
- Affichage d'un debug via inclusion d'un template.  
- Message d'erreur stocké dans `error`.  
*Propagation des erreurs :*  
- L'erreur est remontée dans l'interface via la variable `error`.  
*Améliorations & Optimisations :*  
- Ajouter notification mail comme pour l'insertion.  
- Vérifier les dépendances avant suppression pour éviter erreurs.  

*Code de l'inclusion :*  
```coldfusion
<cftry>
    <cftransaction>
        <cfquery name="delete_attribut" datasource="#request.datasource#">
            delete from bo_attribut where attribut_id = #attributes.attribut_id#
        </cfquery>
        <cfquery name="delete_attribut_prod" datasource="#request.datasource#">
            delete from bo_attribut_type_produit where attribut_id = #attributes.attribut_id#
        </cfquery>
    </cftransaction>
    <cfcatch type="database">
        <cfset error = "#label_err_delete#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloc : Mise à jour d'attributs
*Fichier :* `act_attribut.cfm` (lignes 114-166)  
*Erreurs traitée :*  
- Erreur base de données lors de la mise à jour des libellés d'attributs multilingues.  
*Comportement :*  
- Capture l'erreur via `<cfcatch type="database">`.  
- Envoi d'un mail d'alerte aux développeurs avec dump de l'erreur.  
- Affichage d'un debug via inclusion d'un template.  
- Message d'erreur stocké dans `error`.  
*Propagation des erreurs :*  
- L'erreur est remontée dans l'interface via la variable `error`.  
*Améliorations & Optimisations :*  
- Valider les données avant mise à jour pour éviter erreurs SQL.  
- Centraliser la gestion des erreurs.  

*Code de l'inclusion :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- boucle mise à jour attributs multilingues --->
    </cftransaction>
    <cfcatch type="database">
        <cfmail type="text" to="dev@solusquare.com" from="dev@solusquare.com" subject="error update attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfset error = "#label_err_update#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

### Bloc : Mise à jour des options d'attribut
*Fichier :* `act_attribut.cfm` (lignes 171-269)  
*Erreurs traitée :*  
- Erreur base de données lors de la création ou modification des options d'attributs multilingues.  
*Comportement :*  
- Capture l'erreur via `<cfcatch type="database">`.  
- Envoi d'un mail d'alerte aux développeurs avec dump de l'erreur en HTML.  
- Affichage d'un debug via inclusion d'un template.  
- Message d'erreur stocké dans `error`.  
*Propagation des erreurs :*  
- L'erreur est remontée dans l'interface via la variable `error`.  
*Améliorations & Optimisations :*  
- Améliorer la validation des données d'entrée.  
- Prévoir rollback plus fin en cas d'erreur partielle.  

*Code de l'inclusion :*  
```coldfusion
<cftry>
    <cftransaction>
        <!--- boucle création/modification options attribut --->
    </cftransaction>
    <cfcatch type="database">
        <cfmail type="html" to="dev@solusquare.com" from="dev@solusquare.com" subject="BO - #uCase('#server.sq.machine_prefixe#')# - Error update option attribut">
            <cfdump var="#cfcatch#">
        </cfmail>
        <cfset error = "#label_err_update#<br/>">
        <cfinclude template="#request.libroot#/debug.cfm">
    </cfcatch>
</cftry>
```

---

Cette gestion d'erreurs garantit la stabilité du module en cas de problème base de données, avec une remontée claire des erreurs aux équipes techniques et un suivi via mails automatiques. Une amélioration possible serait d'uniformiser la gestion des erreurs et d'ajouter des logs persistants pour faciliter le diagnostic.

## Interface
Le module Gestion des attributs permet de créer, modifier, rechercher et gérer les attributs produits ainsi que leurs options et groupes de couleurs associés.

### Composant : Liste des attributs
*Fichier :* `dsp_attribut.cfm`  
*But :* Afficher la liste paginée des attributs avec actions de détail, modification, suppression et gestion des options.  
*Champs :*  
- attribut_id  
- code_ext  
- pays_id (affiché par drapeau)  
- langue_id (affiché par drapeau)  
- libelle  
- date_creation  

*Evénements & Actions :*  
- Détail attribut (lien vers `detailAttribut`)  
- Modifier attribut (lien vers `editAttribut`)  
- Supprimer attribut (confirmation puis suppression)  
- Modifier options attribut (lien vers `editAttributOption`)  

*Dépendances visuelles :*  
- Table HTML avec pagination et tri  
- Icônes d’action (détail, modifier, supprimer, options)  
- Drapeaux pour pays et langue  

*Améliorations & optimisations :*  
- Ajout d’un filtre de recherche multi-critères (pays, type produit, attribut)  
- Gestion des droits d’accès pour suppression  

*Code de la requête :*  
```coldfusion
<CFQUERY NAME="qry_attribut_search" DATASOURCE="#request.datasource#">
  SELECT DISTINCT bo_attribut.*, 
    CASE WHEN bo_attribut.pays_id = '#request.pays_base#' AND bo_attribut.langue_id = '#request.langue_base#' THEN 1 ELSE 0 END AS ordre_aff_module
  FROM bo_attribut WITH (NOLOCK)
  LEFT JOIN bo_attribut_type_produit WITH (NOLOCK) ON bo_attribut_type_produit.attribut_id = bo_attribut.attribut_id
  WHERE 0=0
  <CFIF ATTRIBUTES.CRITERIA NEQ "">
    #PreserveSingleQuotes(attributes.Criteria)#
  </CFIF>
  ORDER BY bo_attribut.attribut_id, ordre_aff_module DESC
</CFQUERY>
```

---

### Composant : Formulaire d’ajout d’attributs
*Fichier :* `dsp_attribut_form.cfm`  
*But :* Permettre la création de nouveaux attributs multilingues et leur association à des types de produits.  
*Champs :*  
- type_produit_id (multi-sélection)  
- attribut_id_1, attribut_id_2 (sélection attribut existant)  
- attribut_{langue_id}_1, attribut_{langue_id}_2 (libellés nouveaux attributs par langue)  

*Evénements & Actions :*  
- Soumission du formulaire pour sauvegarder (`saveAttribut`)  
- Annuler et revenir à la recherche  

*Dépendances visuelles :*  
- Tableau multilingue avec colonnes par langue (drapeaux)  
- Sélecteur multiple pour types de produits  
- Notifications d’information et d’erreur  

*Améliorations & optimisations :*  
- Validation côté serveur des champs obligatoires  
- Gestion multilingue complète des libellés  

*Code de la requête :*  
N/A (formulaire uniquement, insertion gérée dans `act_attribut.cfm`)

---

### Composant : Formulaire d’édition d’attribut
*Fichier :* `dsp_attribut_edit_form.cfm`  
*But :* Modifier un attribut existant avec ses libellés multilingues et ses paramètres (code, filtre, couleur).  
*Champs :*  
- code_ext  
- filtre (checkbox)  
- est_une_couleur (checkbox)  
- attribut_{Index} (libellé par langue)  
- langue_id_{Index} (identifiant langue)  

*Evénements & Actions :*  
- Soumission du formulaire pour mise à jour (`updateAttribut`)  
- Annuler et revenir à la liste  

*Dépendances visuelles :*  
- Champs texte multilingues avec drapeaux  
- Notifications d’erreur et d’alerte  
- Checkbox pour options spécifiques  

*Améliorations & optimisations :*  
- Gestion conditionnelle des champs selon client (ex: `param_client.aff_spe_Frago`)  
- Pré-remplissage des données existantes  

*Code de la requête :*  
N/A (mise à jour gérée dans `act_attribut.cfm`)

---

### Composant : Détail d’un attribut
*Fichier :* `dsp_attribut_detail.cfm`  
*But :* Afficher les détails d’un attribut, ses libellés par pays/langue et les types de produits associés.  
*Champs :*  
- attribut_id  
- libelle (par pays/langue)  
- date_creation  
- liste des types de produits associés (type_produit_id, libelle)  

*Evénements & Actions :*  
- Bouton retour à la liste  

*Dépendances visuelles :*  
- Affichage clair des libellés multilingues avec drapeaux  
- Liste simple des types de produits  

*Améliorations & optimisations :*  
- Chargement optimisé par requêtes spécifiques  

*Code de la requête :*  
```coldfusion
<CFQUERY NAME="qry_get_attribut_detail" DATASOURCE="#request.datasource#">
  SELECT *, ud_pays.nom
  FROM bo_attribut WITH (NOLOCK)
  INNER JOIN ud_pays WITH (NOLOCK) ON ud_pays.pays_id = bo_attribut.pays_id
  WHERE bo_attribut.attribut_id = #attributes.attribut_id#
</CFQUERY>

<CFQUERY NAME="qry_get_liste_type_produit" DATASOURCE="#request.datasource#">
  SELECT DISTINCT tp.type_produit_id, tp.libelle
  FROM ud_type_produit tp WITH (NOLOCK)
  INNER JOIN bo_attribut_type_produit atp WITH (NOLOCK) ON atp.type_produit_id = tp.type_produit_id
  WHERE atp.attribut_id = #attributes.attribut_id#
    AND tp.pays_id = '#request.pays_maitre#'
  ORDER BY tp.libelle
</CFQUERY>
```

---

### Composant : Formulaire d’édition des options d’un attribut
*Fichier :* `dsp_attribut_option_edit_form.cfm`  
*But :* Gérer les options (valeurs possibles) d’un attribut avec leurs libellés multilingues, codes, couleurs et groupes.  
*Champs :*  
- attribut_detail_id  
- code (code option)  
- degrade (checkbox bicolore)  
- code_couleur_picto (couleur hexadécimale)  
- libelle (par langue)  
- attribut_group_id (groupe couleur)  

*Evénements & Actions :*  
- Recherche d’une option par libellé  
- Mise à jour des options (`updateAttributOption`)  
- Annuler  

*Dépendances visuelles :*  
- Tableau avec colonnes multilingues (drapeaux)  
- Color picker et gestion bicolore  
- Sélecteur de groupe couleur  

*Améliorations & optimisations :*  
- Validation des codes couleur  
- Interaction dynamique pour bicolore  
- Support client spécifique (`param_client.aff_spe_Frago`)  

*Code de la requête :*  
```coldfusion
<CFQUERY NAME="qry_get_attribut_option" DATASOURCE="#request.datasource#">
  SELECT DISTINCT bo_attribut_detail.attribut_detail_id, bo_attribut_detail.libelle, bo_attribut_detail.langue_id,
    bo_attribut_detail.code, bo_attribut_detail.ordre, bo_attribut_detail.attribut_group_id,
    bo_attribut_detail.code_group, bo_attribut_detail.libelle_group
    <CFIF codeCouleurPicto>, code_couleur</CFIF>
  FROM bo_attribut_detail WITH (NOLOCK)
  WHERE (bo_attribut_detail.attribut_id = #attributes.attribut_id#
    OR bo_attribut_detail.attribut_detail_id IN
      (SELECT attribut_detail_id FROM bo_attribut_detail_option WITH (NOLOCK) WHERE attribut_id = #attributes.attribut_id#))
    AND bo_attribut_detail.langue_id = '#request.langue_base#'
  ORDER BY bo_attribut_detail.attribut_detail_id, bo_attribut_detail.langue_id
</CFQUERY>
```

---

### Composant : Recherche d’attributs
*Fichier :* `dsp_attribut_search.cfm`  
*But :* Permettre la recherche d’attributs selon plusieurs critères (pays, type produit, attribut).  
*Champs :*  
- Crit1_Value : pays_id  
- Crit2_Value : type_produit_id  
- Crit3_Value : attribut_id  

*Evénements & Actions :*  
- Soumission du formulaire pour lancer la recherche (`searchingAttribut`)  

*Dépendances visuelles :*  
- Sélecteurs déroulants avec recherche live  
- Bouton rechercher  

*Améliorations & optimisations :*  
- Gestion des valeurs par défaut  
- Messages d’information sur succès  

*Code de la requête :*  
N/A (formulaire uniquement, requête dans `qry_attribut_search.cfm`)

---

### Composant : Gestion des groupes de couleurs
*Fichier :* `dsp_color_group.cfm`, `dsp_color_group_add.cfm`, `dsp_color_group_search.cfm`, `dsp_attribut_group_edit_form.cfm`  
*But :* Créer, modifier, rechercher et supprimer des groupes de couleurs associés aux attributs.  
*Champs :*  
- attribut_group_id  
- couleur (libellé)  
- ordre (tri)  
- code_ext  
- couleur_url  
- code_couleur  
- langue_id (multilingue)  

*Evénements & Actions :*  
- Ajouter un groupe (`saveColorGroup`)  
- Modifier un groupe (`updateColorGroup`)  
- Supprimer un groupe (`deleteColorGroup`)  
- Rechercher un groupe (`searchingColorGroup`)  

*Dépendances visuelles :*  
- Table listant les groupes avec actions (modifier, supprimer)  
- Formulaire multilingue pour libellés couleur  
- Notifications d’erreur et d’alerte  

*Améliorations & optimisations :*  
- Validation multilingue des champs obligatoires  
- Gestion des droits d’accès  
- Support des couleurs via code hexadécimal et URL  

*Code de la requête :*  
```coldfusion
<CFQUERY NAME="qry_color_group_search" DATASOURCE="#request.datasource#">
  SELECT * FROM bo_attribut_detail_cat_group WITH (NOLOCK)
  WHERE 1=1
  <CFIF isDefined("ATTRIBUTES.criteria") AND ATTRIBUTES.CRITERIA NEQ "">
    #PreserveSingleQuotes(attributes.Criteria)#
  </CFIF>
  <CFIF isDefined("ATTRIBUTES.attribut_group_id")>
    AND attribut_group_id = #attributes.attribut_group_id#
  </CFIF>
  ORDER BY attribut_group_id, ordre
</CFQUERY>
```

---

### Composant : Actions sur attributs
*Fichier :* `act_attribut.cfm`  
*But :* Gérer les actions CRUD sur attributs et options (insert, update, delete, updateoption).  
*Champs :* Variables dynamiques selon action (ex: attribut_id, libelle, type_produit_id, etc.)  

*Evénements & Actions :*  
- insert : création d’attributs multilingues et association aux types de produits  
- update : mise à jour des libellés et paramètres  
- delete : suppression d’un attribut et ses associations  
- updateoption : mise à jour des options d’un attribut  

*Dépendances visuelles :*  
- Gestion des erreurs avec notifications  
- Envoi de mails en cas d’erreur base de données  

*Améliorations & optimisations :*  
- Transactions pour garantir la cohérence  
- Gestion des langues et pays multiples  
- Support spécifique pour clients (ex: filtre, couleur)  

*Extrait de code (insert) :*  
```coldfusion
<cftransaction>
  <cfset tri=1>
  <cfinclude template="#request.queryroot#/qry_get_all_pays_langue.cfm">
  <cfloop index="I" from="1" to="#attributes.max_attributs#">
    <cfif evaluate("attributes.attribut_id_#I#") eq "">
      <cfmodule template="#request.libroot#/act_max_id.cfm" datasource="#request.datasource#" tablename="bo_attribut" primarykey="attribut_id">
      <cfset nb_insert = 0>
      <cfloop query="qry_get_all_pays_langue">
        <cfif isdefined("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#") and trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#")) neq "">
          <cfset current_libelle = trim(evaluate("attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#"))>
          <cfquery name="insert_att" datasource="#request.datasource#">
            INSERT INTO bo_attribut (attribut_id, pays_id, langue_id, libelle, date_creation)
            VALUES (#max_id#, '#qry_get_all_pays_langue.pays_id#', '#qry_get_all_pays_langue.langue_id#', '#current_libelle#', getdate())
          </cfquery>
          <cfset nb_insert = nb_insert + 1>
        </cfif>
      </cfloop>
      ...
    </cfif>
  </cfloop>
</cftransaction>
```

---

Cette documentation synthétise les interfaces principales du module Gestion des attributs de Solusquare Commerce Cloud, avec leurs fichiers ColdFusion associés, champs, actions, dépendances visuelles et extraits de requêtes clés.

## Requêtes AJAX
Cette section décrit les requêtes AJAX utilisées dans le module Gestion des attributs de produit, permettant la manipulation dynamique des attributs sans rechargement complet de la page.

### Requête : Recherche d'attributs
*Paramètres :*  
- `pays` : string • code pays pour filtrer les attributs  
- `typeProduit` : string • identifiant du type de produit  
- `attribut` : string • identifiant de l'attribut  

*But :*  
Récupérer la liste des attributs filtrés par pays, type de produit et attribut sélectionné.

*Améliorations & optimisations :*  
- Implémenter une pagination côté serveur pour limiter la charge.  
- Cacher les attributs non pertinents selon le contexte métier.  
- Mettre en cache les résultats fréquents pour accélérer la réponse.  

*Risques SQL & Sécurité :*  
- Risque d'injection SQL si les paramètres ne sont pas correctement échappés.  
- Vérifier les droits d'accès utilisateur avant d'exécuter la requête.  
- Valider et filtrer strictement les entrées côté serveur.  

*Code de la requête :*  
```coldfusion
<cfquery name="qAttributs" datasource="#datasource#">
    SELECT a.id_attribut, a.nom_attribut
    FROM attributs a
    INNER JOIN attributs_types_produits atp ON a.id_attribut = atp.id_attribut
    WHERE 1=1
    <cfif structKeyExists(url, "pays") AND len(trim(url.pays))>
        AND a.pays = <cfqueryparam value="#url.pays#" cfsqltype="cf_sql_varchar">
    </cfif>
    <cfif structKeyExists(url, "typeProduit") AND len(trim(url.typeProduit))>
        AND atp.id_type_produit = <cfqueryparam value="#url.typeProduit#" cfsqltype="cf_sql_integer">
    </cfif>
    <cfif structKeyExists(url, "attribut") AND len(trim(url.attribut))>
        AND a.id_attribut = <cfqueryparam value="#url.attribut#" cfsqltype="cf_sql_integer">
    </cfif>
    ORDER BY a.nom_attribut
</cfquery>
```

### Requête : Ajout d'attributs
*Paramètres :*  
- `typesProduits` : array • liste des identifiants des types de produits associés  
- `attributsExistants` : array • identifiants des attributs existants à associer  
- `nouveauxAttributs` : struct • clés = codes langue, valeurs = noms des nouveaux attributs  

*But :*  
Créer de nouveaux attributs multilingues et les associer aux types de produits sélectionnés.

*Améliorations & optimisations :*  
- Valider la présence des descriptions dans toutes les langues avant insertion.  
- Utiliser des transactions pour garantir la cohérence des insertions multiples.  
- Prévoir une gestion des doublons pour éviter les conflits.  

*Risques SQL & Sécurité :*  
- Risque d'injection SQL si les valeurs ne sont pas paramétrées.  
- Contrôler les droits d'écriture de l'utilisateur.  
- Vérifier la validité des identifiants de types de produits.  

*Code de la requête :*  
```coldfusion
<cftransaction>
    <!--- Insertion des nouveaux attributs multilingues --->
    <cfloop collection="#nouveauxAttributs#" item="langue">
        <cfquery datasource="#datasource#">
            INSERT INTO attributs (nom_attribut, langue)
            VALUES (<cfqueryparam value="#nouveauxAttributs[langue]#" cfsqltype="cf_sql_varchar">, <cfqueryparam value="#langue#" cfsqltype="cf_sql_varchar">)
        </cfquery>
        <cfset newId = cfqueryresult.generatedKey>
        <!--- Association aux types de produits --->
        <cfloop array="#typesProduits#" index="typeProduit">
            <cfquery datasource="#datasource#">
                INSERT INTO attributs_types_produits (id_attribut, id_type_produit)
                VALUES (<cfqueryparam value="#newId#" cfsqltype="cf_sql_integer">, <cfqueryparam value="#typeProduit#" cfsqltype="cf_sql_integer">)
            </cfquery>
        </cfloop>
    </cfloop>

    <!--- Association des attributs existants --->
    <cfloop array="#attributsExistants#" index="idAttribut">
        <cfloop array="#typesProduits#" index="typeProduit">
            <cfquery datasource="#datasource#">
                INSERT INTO attributs_types_produits (id_attribut, id_type_produit)
                VALUES (<cfqueryparam value="#idAttribut#" cfsqltype="cf_sql_integer">, <cfqueryparam value="#typeProduit#" cfsqltype="cf_sql_integer">)
            </cfquery>
        </cfloop>
    </cfloop>
</cftransaction>
```

## Logique métier
Ce module gère la création, l’édition, la suppression et l’affectation des attributs produits à différents types de produits, avec prise en charge multilingue et gestion avancée des options, notamment les attributs couleur.

### Logique de création et mise à jour des attributs
*Explication :*  
Lors de la création ou mise à jour d’un attribut, le système vérifie la saisie des libellés dans toutes les langues actives, évite les doublons, et associe l’attribut aux types de produits sélectionnés. Les attributs peuvent être marqués comme filtrables ou comme représentant une couleur.

Contraintes :  
- Validation obligatoire des libellés dans toutes les langues.  
- Pas de doublons d’attributs pour un même pays maître.  
- Association multiple possible avec des types de produits.  
- Gestion des attributs couleur avec code couleur et pictogramme.

```coldfusion
{"source": "act_attribut.cfm", "start": 20, "end": 20, "code": "\t\t\t\t<cfloop index=\"I\" from=\"1\" to =\"#attributes.max_attributs#\">\n"}
{"source": "act_attribut.cfm", "start": 21, "end": 21, "code": "\t\t\t\t\t<cfif evaluate(\"attributes.attribut_id_#I#\") eq \"\">\n"}
{"source": "act_attribut.cfm", "start": 27, "end": 27, "code": "\t\t\t\t\t\t<cfloop query=\"qry_get_all_pays_langue\">\n"}
{"source": "act_attribut.cfm", "start": 28, "end": 28, "code": "\t\t\t\t\t\t\t<cfif isdefined(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\") and trim(evaluate(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\")) neq \"\">\n"}
{"source": "act_attribut.cfm", "start": 29, "end": 29, "code": "\t\t\t\t\t\t\t\t<cfset current_libelle = trim(evaluate(\"attributes.attribut_#qry_get_all_pays_langue.langue_id#_#I#\"))>\n"}
{"source": "act_attribut.cfm", "start": 48, "end": 48, "code": "\t\t\t\t\t\t<cfif nb_insert gt 0>\n"}
{"source": "act_attribut.cfm", "start": 49, "end": 49, "code": "\t\t\t\t\t\t\t<cfloop index=\"Index\" list=\"#attributes.type_produit_id#\">\n"}
{"source": "act_attribut.cfm", "start": 64, "end": 64, "code": "\t\t\t\t\t\t<cfset tri = tri +1>\n"}
{"source": "act_attribut.cfm", "start": 65, "end": 65, "code": "\t\t\t\t\t<cfelseif evaluate(\"attributes.attribut_id_#I#\") neq \"\">\n"}
{"source": "act_attribut.cfm", "start": 66, "end": 66, "code": "\t\t\t\t\t\t<cfloop index=\"Index\" list=\"#attributes.type_produit_id#\">\n"}
{"source": "act_attribut.cfm", "start": 80, "end": 80, "code": "\t\t\t\t\t\t<cfset tri = tri +1>\n"}
```

### Logique de gestion des options d’attributs
*Explication :*  
Chaque attribut peut posséder plusieurs options, elles-mêmes multilingues. Le module gère la création, modification et suppression des options, avec un support spécifique pour les options couleur, incluant la gestion des dégradés et codes couleurs multiples.

Contraintes :  
- Les options doivent avoir un libellé dans chaque langue active.  
- Gestion spécifique des options couleur avec codes hexadécimaux.  
- Validation des options bicolores et dégradés.  
- Association possible à des groupes de couleurs.

```coldfusion
{"source": "act_attribut_option_edit_form.cfm", "start": 7, "end": 7, "code": "\t<cfset pays = \"\">\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 21, "end": 21, "code": "\t<cfif codeCouleurPicto AND isdefined(\"qry_get_attribut_all_langue.est_une_couleur\") AND val(qry_get_attribut_all_langue.est_une_couleur) eq 1>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 219, "end": 219, "code": "\t\t\t\t\t\t\t\t\t<cfif \t\tisdefined(\"attributes.degrade_#attribut_detail_id#\") \n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 222, "end": 222, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = evaluate(\"attributes.liste_code_couleur_picto_#attribut_detail_id#\")>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 223, "end": 223, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfif Len(liste_couleur) eq 0 OR liste_couleur eq \"##\"><cfset liste_couleur = \"##000000\"></cfif>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 224, "end": 224, "code": "\t\t\t\t\t\t\t\t\t\t\t<cfif Listlen(liste_couleur,';') gte 2>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 225, "end": 225, "code": "\t\t\t\t\t\t\t\t\t\t\t\t<cfif Len(trim(ListGetAt(liste_couleur,2,';'))) eq 0>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 226, "end": 226, "code": "\t\t\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = ListGetAt(liste_couleur,1,';')>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 227, "end": 227, "code": "\t\t\t\t\t\t\t\t\t\t\t\t<cfelse>\n"}
{"source": "act_attribut_option_edit_form.cfm", "start": 228, "end": 228, "code": "\t\t\t\t\t\t\t\t\t\t\t\t\t<cfset liste_couleur = ListGetAt(liste_couleur,1,';') & \";\" & ListGetAt(liste_couleur,2,';')>\n"}
```

### Logique de validation des données
*Explication :*  
Avant toute insertion ou mise à jour, le module valide la complétude des données, notamment la présence des libellés dans toutes les langues, la sélection des types de produits, et l’absence de doublons. Les erreurs sont remontées pour correction.

Contraintes :  
- Tous les champs obligatoires doivent être renseignés.  
- Libellés multilingues obligatoires.  
- Vérification des doublons d’attributs.  
- Gestion des messages d’erreur contextualisés.

```coldfusion
{"source": "err_attribut_entry.cfm", "start": 4, "end": 4, "code": "<cfset attribut = \"False\">\n"}
{"source": "err_attribut_entry.cfm", "start": 5, "end": 5, "code": "<cfloop index=\"I\" from=\"1\" to=\"1\">\n"}
{"source": "err_attribut_entry.cfm", "start": 6, "end": 6, "code": "\t<cfif evaluate(\"attributes.attribut_id_#I#\") neq \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 11, "end": 11, "code": "\t\t\t<cfset ERROR = ERROR & \"#label_err_doublon_creation_1# #I#, #label_err_doublon_creation_2#<br/>\">\n"}
{"source": "err_attribut_entry.cfm", "start": 16, "end": 16, "code": "\t\t\t<cfif evaluate(\"attributes.attribut_#langue_id#_#I#\") eq \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 17, "end": 17, "code": "\t\t\t\t<cfset ERROR = ERROR & \"#label_err_libelle_attribut_langue#<br/>\">\n"}
{"source": "err_attribut_entry.cfm", "start": 27, "end": 27, "code": "<cfloop list=\"#attributes.requiredfields#\" index=\"counter\">\n"}
{"source": "err_attribut_entry.cfm", "start": 28, "end": 28, "code": "\t<cfif not isdefined(\"attributes.#counter#\") or Trim(Evaluate(\"attributes.\" & \"#counter#\")) IS \"\">\n"}
{"source": "err_attribut_entry.cfm", "start": 29, "end": 29, "code": "\t\t<cfif counter eq \"type_produit_id\">\n"}
{"source": "err_attribut_entry.cfm", "start": 30, "end": 30, "code": "\t\t\t<cfset ERROR = ERROR & \"#label_err_selection_type_produit#<br/>\">\n"}
```

### Logique d’affichage et recherche des attributs
*Explication :*  
Le module propose une interface de recherche filtrée par pays, type de produit et attribut, ainsi qu’une liste paginée des attributs existants. Les résultats sont affichés avec leurs libellés multilingues et options associées.

Contraintes :  
- Recherche multi-critères avec gestion des critères vides.  
- Affichage groupé par attribut et langue.  
- Pagination et gestion des droits d’accès.  
- Affichage des options couleur et filtres.

```coldfusion
{"source": "dsp_attribut_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value\">\n"}
{"source": "dsp_attribut_search.cfm", "start": 17, "end": 17, "code": "<cfoutput>\n"}
{"source": "dsp_attribut_search.cfm", "start": 19, "end": 19, "code": "\t<div class=\"contenttitle\">\n"}
{"source": "dsp_attribut.cfm", "start": 34, "end": 34, "code": "\t<cfoutput query=\"#qry_name#\" group=\"attribut_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 50, "end": 50, "code": "\t\t\t\t<cfoutput group=\"pays_id\">\n"}
{"source": "dsp_attribut.cfm", "start": 55, "end": 55, "code": "\t\t\t\t<cfoutput group=\"langue_id\">\n"}
```

### Logique de gestion des groupes de couleurs
*Explication :*  
Les groupes de couleurs permettent de regrouper des options d’attributs couleur pour une meilleure organisation. Le module gère la création, mise à jour, suppression et affichage de ces groupes avec leurs propriétés multilingues.

Contraintes :  
- Gestion multilingue des libellés et couleurs.  
- Validation des champs obligatoires (couleur, ordre, langue).  
- Association aux options d’attributs couleur.  
- Interface dédiée pour la gestion des groupes.

```coldfusion
{"source": "act_color_group.cfm", "start": 3, "end": 3, "code": "<cfif fuseaction eq \"updateColorGroup\">\n"}
{"source": "act_color_group.cfm", "start": 6, "end": 6, "code": "<cfset qry_name = \"qry_color_group_search\">\n"}
{"source": "dsp_color_group.cfm", "start": 18, "end": 18, "code": "<cfoutput>\n"}
{"source": "dsp_color_group_add.cfm", "start": 4, "end": 4, "code": "<cfif ATTRIBUTES.FUSEACTION IS \"new\">\n"}
{"source": "dsp_color_group_search.cfm", "start": 3, "end": 3, "code": "<cfset FIELDLIST = \"Crit1_Value,Crit2_Value,Crit3_Value,Crit4_Value,Crit5_Value\">\n"}
```

---

Cette documentation synthétise la logique métier essentielle du module Gestion des attributs de produit, facilitant la compréhension et la maintenance par les équipes techniques ColdFusion de Solusquare.

