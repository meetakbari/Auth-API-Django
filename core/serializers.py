from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if raw_password is not None:
            instance.set_password(raw_password) #set_password method is inbuilt, it generates hashed password of raw_password
        instance.save()

        return instance

