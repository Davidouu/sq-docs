---
---
title: "TroubleShooting & faq"
---

# TroubleShooting & faq

## Common Errors: Causes and Solutions

| Code/Message                          | Probable Cause                                                                                   |
|---------------------------------------|-------------------------------------------------------------------------------------------------|
| Error inserting attribute              | Missing or incorrectly formatted data, duplicate attribute, database connection issue           |
| Error deleting attribute               | The attribute is still linked to product types or options, or incorrect identifier              |
| Error updating attribute               | Incomplete labels in some languages, invalid data, transaction issue                           |
| Error updating attribute options       | Missing labels, invalid color code, multilingual synchronization issue                          |
| Color not accounted for or invalid     | Incorrect color code entry (must be in ##XXXXXX format), lack of visual validation             |
| Attribute not visible on product sheet | Attribute not associated with the relevant product type or inactive status                     |
| Unable to associate an attribute with a product type | Incorrect identifier or existing association                                          |
| Attribute search returns nothing       | Criteria too restrictive or data not yet created                                               |
| Error message "Missing required value" | Required fields not filled in (e.g., associated product types, multilingual labels)            |
| Multilingual display issue             | Labels not provided in all active languages                                                    |

## Frequently Asked Questions

- **How to create a new product attribute?**  
  Fill in the labels in all active languages, select at least one associated product type, and then validate the addition form.

- **Can I associate the same attribute with multiple product types?**  
  Yes, it is possible to associate an attribute with multiple product types for common use.

- **How to modify an existing attribute?**  
  Use the editing form to update labels, external code, and options such as filter or color.

- **How to delete an attribute?**  
  Delete the attribute only if it is no longer associated with any product type or used in product sheets.

- **What does it mean when an attribute is marked as "filter"?**  
  This indicates that the attribute can be used to refine product searches via filters.

- **How to manage the options of an attribute?**  
  Access the options editing form to add, modify, or delete possible values, along with their multilingual labels.

- **How to enter a color for an attribute option?**  
  Enter a color code in hexadecimal format with a double hash, for example `##FF0000`. The entry is validated automatically.

- **What to do if the entered color is not accepted?**  
  Check the format of the color code, correct the entry, or leave it blank to revert to the default black color.

- **How to manage color groups?**  
  Create and modify color groups via the dedicated interface, then associate them with color attribute options.

- **Why does an attribute not appear in the attribute list?**  
  Check the search criteria, the status of the attribute, and its association with product types.

- **Can an attribute be created without labels in all languages?**  
  No, it is mandatory to provide labels in all active languages to ensure multilingual consistency.

- **How to manage the display order of attributes?**  
  The order is defined by a sorting field when associating the attribute with product types.

- **Is it possible to have country-specific attributes?**  
  Yes, each attribute is linked to a country of application, allowing for localized management.

- **How to avoid attribute duplicates?**  
  The system checks for duplicates during creation and displays an error message if a similar attribute already exists.

- **How to search for a specific attribute?**  
  Use the search form by filtering by country, product type, or attribute name to refine the results.

- **What to do in case of a technical error during an operation?**  
  An error message will be displayed, and a notification will be sent to the technical teams for analysis. Contact support if necessary.