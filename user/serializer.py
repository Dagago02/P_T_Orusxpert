from rest_framework import serializers
from .models import User 



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email','password', 'cellphone']
    def validate_username(self, attrs):
        if attrs == "Daniel":
            raise serializers.ValidationError('no te llamas daniel')
        return attrs
    def validate_cellphone(self, attrs):
        if not len(attrs)==10:
            raise serializers.ValidationError('los telefonos tienen 10 numeros')
        return super().validate(attrs)