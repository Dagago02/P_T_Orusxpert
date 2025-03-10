from rest_framework import serializers
from .models import Cedi 



class CediSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cedi
        fields = ['name', 'lat','long']
    