import json
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

from .forms import BarkeeperUserCreationForm
from .models import BarkeeperUser
# Create your views here.

class SignUp(generic.CreateView):
    form_class = BarkeeperUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@csrf_exempt
def register_user(request):
    """Handles the creation of a new user for authentication

    Method arguments:
        request -- The full HTTP request object
    """

    request_body = json.loads(request.body.decode())

    new_user = BarkeeperUser.objects.create_user(
        username=request_body['username'],
        password=request_body['password'],
        email=request_body['email'],
        first_name=request_body['first_name'],
        last_name=request_body['last_name'],
    )

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token":token.key})
    return HttpResponse(data, content_type="application/json")