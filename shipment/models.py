from django.db import models
from cedis.models import Cedi 
from django.contrib.auth import get_user_model

User = get_user_model()


class Ship(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cedi = models.ForeignKey(Cedi,on_delete=models.CASCADE,null=True, blank=True)
    delivery_distance = models.FloatField(blank=True,null=True)
    delivery_time = models.FloatField(blank=True,null=True)


