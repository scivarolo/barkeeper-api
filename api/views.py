from django.shortcuts import render
from rest_framework import viewsets, filters

from .serializers import *
from .models import *

class CocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows cocktails to be viewed or edited. """
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer
    search_fields = ('name', 'ingredients__name')
    filter_fields = ('name', 'notes', 'ingredients__name')


class IngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows ingredients to be viewed or edited. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name',)
    filter_fields = ('name',)

class CocktailIngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint for the CocktailIngredient join table. """
    # TODO: Does this need to be an available endpoint if I can include them in Cocktail
    queryset = CocktailIngredient.objects.all()
    serializer_class = CocktailIngredientSerializer
    filter_fields = '__all__'

class ProductViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows products to be viewed or edited. """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ('size', 'unit', 'ingredient', 'name')
    search_fields = ('name', 'ingredient')

class UserCocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the cocktails saved by the current user. """
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)
    serializer_class = UserCocktailSerializer
    filter_fields = ('cocktail', 'is_saved', 'user', 'make_count')
    search_fields = ('cocktail__name')


class UserTabViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrives the cocktails queued to be made by the current user. """
    def get_queryset(self):
        return UserTabCocktail.objects.filter(user=self.request.user)
    serializer_class = UserTabSerializer
    filter_fields = ('cocktail', 'user')
    search_fields = ('cocktail__name')


class UserProductViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the products in the current user's inventory."""
    def get_queryset(self):
        return UserProduct.objects.filter(user=self.request.user)
    serializer_class = UserProductSerializer
    filter_fields = ('product__name', 'product', 'amount_available', 'user')
    search_fields = ('product__name')

class UserShoppingViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the products/ingredients in the current user's shopping list."""
    def get_queryset(self):
        return UserShopping.objects.filter(user=self.request.user)
    serializer_class = UserShoppingSerializer
    filter_fields = ('product', 'ingredient', 'product__name', 'ingredient__name', 'user')
    search_fields = ('product__name', 'ingredient__name')
