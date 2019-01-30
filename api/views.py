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