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


class UserCocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCocktail
        fields = '__all__'


class UserTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTab
        fields = '__all__'


class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = '__all__'


class UserShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShopping
        fields = '__all__'