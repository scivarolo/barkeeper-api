from django.conf.urls import include, url
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from .models import *
from . import views

router = routers.DefaultRouter()
router.register(r'cocktails', views.CocktailViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'cocktailingredients', views.CocktailIngredientViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]