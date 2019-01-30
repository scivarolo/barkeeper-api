from rest_framework import serializers

from .models import *

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)


class CocktailIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    class Meta:
        model = CocktailIngredient
        fields = ('ingredient', 'sort_order', 'amount', 'unit')


class CocktailSerializer(serializers.ModelSerializer):
    # Uses the CocktailIngredientSerializer to join with Ingredient including the join table data.
    ingredients = CocktailIngredientSerializer(source="cocktailingredient_set", many=True)

    class Meta:
        model = Cocktail
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'