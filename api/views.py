from django.shortcuts import render
from django_filters import rest_framework as django_filters
from rest_framework import viewsets, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import *
from .models import *


class CustomAuth(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })

class CocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows cocktails to be viewed or edited. """
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer
    search_fields = ('name', 'ingredients__name')
    filter_fields = ('name', 'notes', 'ingredients__name')

    # assign user from token in request header
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # allow partial update with PATCH
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class IngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows ingredients to be viewed or edited. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name',)
    filter_fields = ('name',)


class CocktailIngredientFilterSet(django_filters.FilterSet):
    ingredient_name = django_filters.CharFilter(field_name="ingredient__name", lookup_expr='icontains')
    class Meta:
        model = CocktailIngredient
        fields = ('ingredient__name', 'cocktail')

class CocktailIngredientViewSet(viewsets.ModelViewSet):
    """ API endpoint for the CocktailIngredient join table. """
    queryset = CocktailIngredient.objects.all()
    serializer_class = CocktailIngredientSerializer
    filterset_class = CocktailIngredientFilterSet

class ProductViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows products to be viewed or edited. """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ('size', 'unit', 'ingredient', 'name')
    search_fields = ('name', 'ingredient')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserCocktailViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the cocktails saved by the current user. """
    def get_queryset(self):
        return UserCocktail.objects.filter(user=self.request.user)

    serializer_class = UserCocktailSerializer
    filter_fields = ('cocktail', 'cocktail_id', 'is_saved', 'user', 'make_count')
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

    # allow partial update with PATCH
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class UserShoppingViewSet(viewsets.ModelViewSet):
    """ API endpoint that retrieves the products/ingredients in the current user's shopping list."""
    def get_queryset(self):
        return UserShopping.objects.filter(user=self.request.user)
    serializer_class = UserShoppingSerializer
    filter_fields = ('product', 'ingredient', 'product__name', 'ingredient__name', 'user')
    search_fields = ('product__name', 'ingredient__name')
