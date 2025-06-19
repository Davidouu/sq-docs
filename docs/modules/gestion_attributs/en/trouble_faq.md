# TroubleShooting & faq

## Common Errors: Causes and Solutions

| Code/Message                         | Probable Cause                                                                                   |
|------------------------------------|------------------------------------------------------------------------------------------------|
| Error inserting attribute           | Missing or improperly formatted data, duplicate attribute, database connection issue            |
| Error deleting attribute            | Attribute still linked to product types or options, or incorrect identifier                      |
| Error updating attribute            | Incomplete labels in some languages, invalid data, transaction problem                           |
| Error updating attribute options    | Missing labels, invalid color code, multilingual synchronization issue                           |
| Color not applied or invalid        | Incorrect color code entry (must be in ##XXXXXX format), lack of visual validation               |
| Attribute not visible on product sheet | Attribute not associated with the relevant product type or inactive status                      |
| Unable to associate attribute with a product type | Incorrect identifier or association already exists                                  |
| Attribute search returns no results | Criteria too restrictive or data not yet created                                                |
| Error message "Required value missing" | Mandatory fields not filled (e.g., associated product types, multilingual labels)             |
| Multilingual display issue          | Labels not provided in all active languages                                                     |

## Frequently Asked Questions

- **How to create a new product attribute?**  
  Fill in the labels in all active languages, select at least one associated product type, then submit the addition form.

- **Can I associate the same attribute with multiple product types?**  
  Yes, an attribute can be associated with multiple product types for shared use.

- **How to modify an existing attribute?**  
  Use the edit form to update labels, external code, and options such as filter or color.

- **How to delete an attribute?**  
  Delete the attribute only if it is no longer associated with any product type nor used in product sheets.

- **What does it mean when an attribute is marked as a "filter"?**  
  It indicates that the attribute can be used to refine product searches via filters.

- **How to manage an attribute’s options?**  
  Access the options edit form to add, modify, or delete possible values along with their multilingual labels.

- **How to enter a color for an attribute option?**  
  Enter a hexadecimal color code with a double hash, for example `##FF0000`. The entry is validated automatically.

- **What to do if the entered color is not accepted?**  
  Check the color code format, correct the entry, or leave it empty to revert to the default black color.

- **How to manage color groups?**  
  Create and modify color groups via the dedicated interface, then associate them with color attribute options.

- **Why does an attribute not appear in the attribute list?**  
  Check the search criteria, attribute status, and its association with product types.

- **Can an attribute be created without labels in all languages?**  
  No, it is mandatory to provide labels in all active languages to ensure multilingual consistency.

- **How to manage the display order of attributes?**  
  The order is defined by a sorting field when associating the attribute with product types.

- **Is it possible to have country-specific attributes?**  
  Yes, each attribute is linked to an application country, allowing localized management.

- **How to avoid duplicate attributes?**  
  The system checks for duplicates during creation and displays an error message if a similar attribute already exists.

- **How to search for a specific attribute?**  
  Use the search form filtering by country, product type, or attribute name to refine results.

- **What to do in case of a technical error during an operation?**  
  An error message is displayed, and a notification is sent to the technical teams for analysis. Contact support if necessary.