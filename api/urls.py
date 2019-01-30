from django.conf.urls import include, url
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from .models import *

class CocktailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cocktail
        fields = ('name', 'instructions', 'notes')

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer

router = routers.DefaultRouter()
router.register(r'cocktails', CocktailViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]