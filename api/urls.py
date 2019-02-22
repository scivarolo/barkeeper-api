from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .models import *
from . import views

router = routers.DefaultRouter()
router.register('cocktails', views.CocktailViewSet, 'cocktails')
router.register('ingredients', views.IngredientViewSet, 'ingredients')
router.register('cocktailingredients', views.CocktailIngredientViewSet, 'cocktailingredients')
router.register('products', views.ProductViewSet, 'products')
router.register('user_cocktails', views.UserCocktailViewSet, 'user_cocktails')
router.register('user_tab', views.UserTabViewSet, 'user_tab')
router.register('user_products', views.UserProductViewSet, 'user_products')
router.register('user_shopping', views.UserShoppingViewSet, 'user_shopping')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.CustomAuth.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Barkeeper API'))
]