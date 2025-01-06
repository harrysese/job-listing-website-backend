from rest_framework import serializers
from joblistingapp.models import Job
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs={'password':{'write_only':True}}
    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({'error':'Username already exists'})
        elif User.objects.filter(username=validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
        return user
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    def validate(self, data):
        from django.contrib.auth import authenticate
        print(f"Data received for authentication: {data}")
        user=authenticate(**data)
        if user is not None:
            access_token=AccessToken.for_user(user)
            return {'access': str(access_token)}
        else:
            raise serializers.ValidationError('Ínvalid Credentials')