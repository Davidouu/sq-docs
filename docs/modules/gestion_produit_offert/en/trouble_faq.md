---
title: "TroubleShooting & FAQ"
---
[Modifier cette page](/documentation/docs/admin/#/collections/modules/entries/gestion_produit_offert/en/trouble_faq)

# TroubleShooting & FAQ

## Common Errors: Causes and Solutions
| Code/message | Probable Cause |
|--------------|----------------|
| #label_err_occurs# | Server connection issue or request error. Check the connection and settings. |
| #label_err_doublon_marque# | Attempt to add an already existing product. Check the product identifiers. |
| #label_err_update# | Error during data update. Check permissions and data integrity. |
| #label_err_insert# | Error during the insertion of a new product. Check mandatory fields. |
| #label_err_delete# | Error during product deletion. Check if the product is linked to other entities. |

## Frequently Asked Questions
- **How to activate the offered products management module?**
  To activate the module, access the configuration settings and enable the corresponding option.

- **Do offered products appear in the customer's cart?**
  No, offered products are added in the background and are not visible in the cart.

- **How to define eligibility conditions for offered products?**
  Conditions can be defined in the module settings by specifying criteria such as order value or number of orders.

- **Can I limit the number of offered products per order?**
  Yes, it is possible to set a limit in the module configuration settings.

- **How to manage the stock of offered products?**
  Stocks can be managed through the integrated logistics module, ensuring that quantities are updated during orders.

- **Can new customers benefit from the offers?**
  Yes, it is possible to define offers reserved for new customers in the settings.

- **How to check if a product is eligible for an offer?**
  Use the eligibility check function in the module to test the defined criteria.

- **What to do if I encounter an error while updating an offer?**
  Check the displayed error messages and ensure that all required data is correctly filled out.

- **How to delete an offered product?**
  Access the list of offered products and use the associated delete option.

- **Can I modify an existing offer?**
  Yes, it is possible to modify the details of an offer by accessing the offer management section.

- **How to retrieve information about offered products for a specific customer?**
  Use the `getInfoProduitOffertClient` function to retrieve the necessary data.

- **How to manage connection errors when using the module?**
  Check the server connection and ensure that the connection settings are correct.

- **Can offered products be associated with specific promotions?**
  Yes, offered products can be linked to promotions defined in the system.

- **How to display the details of an offer?**
  Access the offers section and select the desired offer to display its details.

- **What are the best practices for managing offered products?**
  Ensure that eligibility conditions are clear, regularly check stock levels, and update offers based on customer feedback.
---