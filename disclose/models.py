from django.db import models
from django.contrib.auth.models import User

class Breed(models.Model):
    breed = models.CharField(max_length=50)

    def __str__(self):
        return self.breed

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    petname = models.CharField(max_length=50)
    description = models.TextField()
    state = models.CharField(msa_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)

    def __str__(self):
        return self.pet
