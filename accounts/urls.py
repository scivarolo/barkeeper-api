from django.urls import path

from . import views


urlpatterns = [
    # path("signup/", views.SignUp.as_view(), name="signup"),
    path("register/", views.register_user)
]