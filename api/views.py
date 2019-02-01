from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from .models import *

class CocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows cocktails to be viewed or edited. """
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows ingredients to be viewed or edited. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CocktailIngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint for the CocktailIngredient join table. """
    queryset = CocktailIngredient.objects.all()
    serializer_class = CocktailIngredientSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows products to be viewed or edited. """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserCocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the cocktails saved by the current user. """
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)
    serializer_class = UserCocktailSerializer


class UserTabViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrives the cocktails queued to be made by the current user. """
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)
    serializer_class = UserTabSerializer


class UserProductViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the products in the current user's inventory."""
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)
    serializer_class = UserProductSerializer


class UserShoppingViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the products/ingredients in the current user's shopping list."""
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)
    serializer_class = UserShoppingSerializer