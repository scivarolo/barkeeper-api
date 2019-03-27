from rest_framework import serializers

from .models import Ingredient, Cocktail, CocktailIngredient, Product, UserCocktail, UserTabCocktail, UserProduct, UserShopping, UserHistory

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

    def update(self, instance, validated_data):
        # Pull out the ingredient data so we can update the relations.
        ingredients_data = validated_data.pop('cocktailingredient_set')
        ingredients = (instance.cocktailingredient_set).all()
        ingredients = list(ingredients)

        # Update cocktail specific data
        instance.name = validated_data.get('name', instance.name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()

        for ingredient_data in ingredients_data:
            try:
                cocktail_ingredient = ingredients.pop(0)
                cocktail_ingredient.sort_order = ingredient_data.get('sort_order', cocktail_ingredient.sort_order)
                cocktail_ingredient.amount = ingredient_data.get('amount', cocktail_ingredient.amount)
                cocktail_ingredient.unit = ingredient_data.get('unit', cocktail_ingredient.unit)
                for key, value in ingredient_data.items():
                    if key is "ingredient":
                        for ing_key, ing_value in value.items():
                            if ing_key is "name":
                                name = ing_value
                            if ing_key is "liquid":
                                liquid = ing_value

                        try:
                            ingredient_entity = Ingredient.objects.get(name=name, liquid=liquid)
                        except Ingredient.DoesNotExist:
                            ingredient_entity = Ingredient.objects.create(name=name, liquid=liquid, created_by=instance.created_by)
                cocktail_ingredient.ingredient = ingredient_entity
                cocktail_ingredient.save()

            except IndexError:
                #this is completely new ingredient relation
                cocktail_ingredient = dict()

                for key, value in ingredient_data.items():
                    if key is "ingredient":
                        for ing_key, ing_value in value.items():
                            if ing_key is "name":
                                name = ing_value
                            if ing_key is "liquid":
                                liquid = ing_value

                        try:
                            ingredient_entity = Ingredient.objects.get(name=name, liquid=liquid)
                        except Ingredient.DoesNotExist:
                            ingredient_entity = Ingredient.objects.create(name=name, liquid=liquid, created_by=instance.created_by)
                        cocktail_ingredient['ingredient'] = ingredient_entity
                    else:
                        cocktail_ingredient[key] = value
                CocktailIngredient.objects.create(**cocktail_ingredient, cocktail=instance)
        if len(ingredients) > 0 :
            for cocktail_ingredient in ingredients:
                cocktail_ingredient.delete()
        return instance


    def create(self, validated_data):
        # print("user", user)
        # Pull out the ingredient data so we can create the relations.
        ingredients_data = validated_data.pop('cocktailingredient_set')
        # Create the cocktail
        cocktail = Cocktail.objects.create(**validated_data)

        # Ingredient entitites will be saved here
        ingredients_list = []

        # Loop through ingredients, and find or create an Ingredient in the database.
        # Return the cocktail_ingredient dict with the Ingredient object in it.
        for ingredient_dict in ingredients_data:
            cocktail_ingredient = dict()
            for key, value in ingredient_dict.items():
                if key is "ingredient":
                    for ing_key, ing_value in value.items():
                        # print("name", ing_key, ing_value)
                        if ing_key is "name":
                            name = ing_value
                        if ing_key is "liquid":
                            liquid = ing_value

                    try:
                        ingredient_entity = Ingredient.objects.get(name=name, liquid=liquid)
                    except Ingredient.DoesNotExist:
                        # grab user from newly created cocktail
                        ingredient_entity = Ingredient.objects.create(name=name, liquid=liquid, created_by=cocktail.created_by)
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
    cocktail = CocktailSerializer(read_only=True)
    cocktail_id = serializers.PrimaryKeyRelatedField(
        queryset=Cocktail.objects.all(), source='cocktail'
    )
    class Meta:
        model = UserCocktail
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
                # perhaps add 'read_only': True here too.
            }
        }


class UserTabSerializer(serializers.ModelSerializer):
    cocktail = CocktailSerializer(read_only=True)
    cocktail_id = serializers.PrimaryKeyRelatedField(
        queryset=Cocktail.objects.all(), source='cocktail'
    )

    class Meta:
        model = UserTabCocktail
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
                # perhaps add 'read_only': True here too.
            }
        }


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


class UserHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserHistory
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'default': serializers.CreateOnlyDefault(
                    serializers.CurrentUserDefault()
                ),
            }
        }
