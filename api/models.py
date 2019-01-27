from django.db import models

# Create your models here.

class ApiUser(models.Model):
    """Defines a user the same way used in json-server version of database."""
    email = models.EmailField()
    password = models.CharField('')