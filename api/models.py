from django.conf import settings
from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=120)
    instructions = models.TextField()
    notes = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='CocktailIngredient')
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    sort_order = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    unit = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.ingredient.name} for {self.cocktail.name}"


class Product(models.Model):
    name = models.CharField(max_length=120)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    size = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.ingredient.name})"


class UserCocktail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    is_saved = models.BooleanField(default=True)
    make_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cocktail.name} for {self.user.name}"


class UserTabCocktail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cocktail.name} in {self.user.username}'s tab"


class UserProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} in {self.user.username}"


class UserShopping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.ingredient:
            return f"{self.ingredient.name} in {self.user.username}"

        if self.product:
            return f"{self.product.name} in {self.user.username}"