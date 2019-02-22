# Barkeeper API

Built with Python, Django, and the DjangoREST Framework, Barkeeper API serves data to Barkeeper. Token authentication prevents anonymous users from interacting with the API, and allows users to only interact with data that pertains to them.

## Endpoints
```javascript
{
    "cocktails": "/api/cocktails/",
    "ingredients": "/api/ingredients/",
    "cocktailingredients": "/api/cocktailingredients/",
    "products": "/api/products/",
    "user_cocktails": "/api/user_cocktails/",
    "user_tab": "/api/user_tab/",
    "user_products": "/api/user_products/",
    "user_shopping": "/api/user_shopping/"
}
```
---
### /api/cocktails
Includes all information necessary to display a cocktail, including ingredients.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "id": 1,
  "ingredients": [
    {
      "ingredient": {
        "name": "Gin",
        "id": 1,
        "liquid": true
      },
      "sort_order": 1,
      "amount": "0.75",
      "unit": "oz"
    },
    {
      "ingredient": {
        "name": "Green Chartreuse",
        "id": 2,
        "liquid": true
      },
      "sort_order": 2,
      "amount": "0.75",
      "unit": "oz"
    },
    {
      "ingredient": {
        "name": "Maraschino Liqueur",
        "id": 3,
        "liquid": true
      },
      "sort_order": 3,
      "amount": "0.75",
      "unit": "oz"
    },
    {
      "ingredient": {
        "name": "Lime Juice",
        "id": 4,
        "liquid": true
      },
      "sort_order": 4,
      "amount": "0.75",
      "unit": "oz"
    }
  ],
  "name": "Last Word",
  "instructions": "Shake with ice and strain into a chilled coupe.",
  "notes": "This is a really good cocktail.",
  "created_by": 1
}
```
---
### /api/ingredients/
Returns ingredient information.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "name": "Campari",
  "id": 5,
  "liquid": true
}
```
---
### /api/cocktailingredients/
Returns relationships between cocktails and ingredients with ingredient information embedded.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "ingredient": {
    "name": "Gin",
    "id": 1,
    "liquid": true
  },
  "sort_order": 1,
  "amount": "0.75",
  "unit": "oz"
}
```
---
### /api/products/
Returns information about products

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "id": 16,
  "name": "Another Gin",
  "size": 750,
  "unit": "ml",
  "ingredient": 1,
  "created_by": 1
},
```
---
### /api/user_cocktails/
Returns the current user's saved cocktails. Cocktail and ingredients are embedded in the request. Requires token.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
```javascript
{
  "id": 20,
  "cocktail": {
    "id": 1,
    "ingredients": [
      {
        "ingredient": {
          "name": "Gin",
          "id": 1,
          "liquid": true
        },
        "sort_order": 1,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Green Chartreuse",
          "id": 2,
          "liquid": true
        },
        "sort_order": 2,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Maraschino Liqueur",
          "id": 3,
          "liquid": true
        },
        "sort_order": 3,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Lime Juice",
          "id": 4,
          "liquid": true
        },
        "sort_order": 4,
        "amount": "0.75",
        "unit": "oz"
      }
    ],
    "name": "Last Word",
    "instructions": "Shake with ice and strain into a chilled coupe.",
    "notes": "This is a really good cocktail.",
    "created_by": 1
  },
  "cocktail_id": 1,
  "is_saved": true,
  "make_count": 4,
  "user": 1
}
```
---
### /api/user_tab/
Returns cocktails a user has queued to make. Cocktail information is embedded in the request. Token required.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
```javascript
{
  "id": 15,
  "cocktail": {
    "id": 1,
    "ingredients": [
      {
        "ingredient": {
          "name": "Gin",
          "id": 1,
          "liquid": true
        },
        "sort_order": 1,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Green Chartreuse",
          "id": 2,
          "liquid": true
        },
        "sort_order": 2,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Maraschino Liqueur",
          "id": 3,
          "liquid": true
        },
        "sort_order": 3,
        "amount": "0.75",
        "unit": "oz"
      },
      {
        "ingredient": {
          "name": "Lime Juice",
          "id": 4,
          "liquid": true
        },
        "sort_order": 4,
        "amount": "0.75",
        "unit": "oz"
      }
    ],
    "name": "Last Word",
    "instructions": "Shake with ice and strain into a chilled coupe.",
    "notes": "This is a really good cocktail.",
    "created_by": 1
  },
  "cocktail_id": 1,
  "quantity": 1,
  "user": 1
}
```
---
### /api/user_products/
Returns products that a user has in their invenetory. Product information is embedded in the request. Token required.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "id": 22,
  "quantity": 1,
  "product": {
    "id": 17,
    "name": "Campari 2",
    "size": 750,
    "unit": "ml",
    "ingredient": 5,
    "created_by": 1
  },
  "product_id": 17,
  "user": 1,
  "amount_available": "586.00"
}
```
---
### /api/user_shopping/

Returns products and ingredients that are in a user's inventory. Ingredient/Product information is embedded in the request. Token required.

Allowed: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

```javascript
{
  "id": 20,
  "product": null,
  "product_id": null,
  "ingredient": {
    "name": "Green Chartreuse",
    "id": 2,
    "liquid": true
  },
  "ingredient_id": 2,
  "quantity": 1,
  "user": 1
},
{
  "id": 21,
  "product": {
    "id": 17,
    "name": "Campari 2",
    "size": 750,
    "unit": "ml",
    "ingredient": 5,
    "created_by": 1
  },
  "product_id": 17,
  "ingredient": null,
  "ingredient_id": null,
  "quantity": 1,
  "user": 1
}
```
