""" Defines API models """

from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Ingredient(models.Model):
    """ Defines an ingredient available to all users for use in cocktail recipes. """

    name = models.CharField(max_length=120)
    liquid = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    """ Defines a cocktail """

    name = models.CharField(max_length=120)
    instructions = models.TextField()
    notes = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='CocktailIngredient')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CocktailIngredient(models.Model):
    """ Establishes a relationship between a Cocktail and an Ingredient."""

    cocktail = models.ForeignKey(Cocktail, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    sort_order = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=120)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.ingredient.name} for {self.cocktail.name}"


class Product(models.Model):
    """ Defines a product available for users to add to their inventory. Always related to an ingredient."""

    name = models.CharField(max_length=120)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    size = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.ingredient.name})"


class UserCocktail(models.Model):
    """Defines a relationship between and User and Cocktail. Represents a cocktail the user has saved to their account."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    is_saved = models.BooleanField(default=True)
    make_count = models.PositiveIntegerField()

    class Meta:
        ordering = ['cocktail__name']

    def __str__(self):
        return f"{self.cocktail.name} for {self.user.name}"


class UserTabCocktail(models.Model):
    """ Defines a cocktail that a user has queued for making in their tab."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cocktail.name} in {self.user.username}'s tab"


class UserProduct(models.Model):
    """ Represents product that a user has in their inventory."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount_available = models.DecimalField(max_digits=25, decimal_places=2)

    class Meta:
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name} in {self.user.username}"


class UserShopping(models.Model):
    """ Represents a Product or Ingredient that a User wants to buy. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.ingredient:
            return f"{self.ingredient.name} in {self.user.username}"

        if self.product:
            return f"{self.product.name} in {self.user.username}"


class UserHistory(models.Model):
    """ Contains a record of every Cocktail that a user has made, and when it was made."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cocktail = models.ForeignKey("Cocktail", on_delete=models.PROTECT)
    time = models.DateTimeField(default=timezone.now)