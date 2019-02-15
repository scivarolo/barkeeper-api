from rest_framework import serializers

from .models import *

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'id', 'liquid')


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

    def create(self, validated_data):
        # print("user", user)
        # Pull out the ingredient data so we can create the relations.
        ingredients_data = validated_data.pop('cocktailingredient_set')
        print("data", validated_data)
        # Create the cocktail
        cocktail = Cocktail.objects.create(**validated_data)

        # Ingredient entitites will be saved here
        ingredients_list = []

        # Loop through ingredients, and find or create an Ingredient in the database.
        # Return the cocktail_ingredient dict with the Ingredient object in it.
        for ingredient_dict in ingredients_data:
            # print("ingredient", ingredient_dict)
            cocktail_ingredient = dict()
            for key, value in ingredient_dict.items():
                if key is "ingredient":
                    for ing_key, ing_value in value.items():
                        # print("name", ing_key, ing_value)
                        try:
                            ingredient_entity = Ingredient.objects.get(name=ing_value)
                        except Ingredient.DoesNotExist:
                            # grab user from newly created cocktail
                            ingredient_entity = Ingredient.objects.create(name=ing_value, created_by=cocktail.created_by)
                        # print("In Database", ingredient_entity)
                        cocktail_ingredient['ingredient'] = ingredient_entity
                else:
                    cocktail_ingredient[key] = value
            ingredients_list.append(cocktail_ingredient)

        # Create a relation for each cocktail_ingredient
        for cocktail_ingredient in ingredients_list:
            CocktailIngredient.objects.create(**cocktail_ingredient, cocktail=cocktail)

        return cocktail


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
        model = UserTabCocktail
        fields = '__all__'


class UserProductSerializer(serializers.ModelSerializer):
    # Include the product information
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product')

    class Meta:
        model = UserProduct
        fields = ('id', 'quantity', 'product', 'product_id', 'user', 'amount_available',)
        # depth = 1
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
                # perhaps add 'read_only': True here too.
            }
        }


class UserShoppingSerializer(serializers.ModelSerializer):

    #include product or ingredient data
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product',
        allow_null=True
    )
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient',
        allow_null=True
    )

    def validate(self, data):
        '''UserShopping items can be an ingredient OR a product, but not both, and not neither.'''

        if self.context['request']._request.method is "POST":
            product = data['product']
            ingredient = data['ingredient']

            if product is None and ingredient is None:
                raise serializers.ValidationError("Product or Ingredient must be provided.")

            if product is not None and ingredient is not None:
                raise serializers.ValidationError("You cannot provide Product AND Ingredient. Use only one.")

        return data

    class Meta:
        model = UserShopping
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
                # perhaps add 'read_only': True here too.
            }
        }