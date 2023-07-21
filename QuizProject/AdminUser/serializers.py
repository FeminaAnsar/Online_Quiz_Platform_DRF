from rest_framework import serializers
from AdminUser.models import User
from QuizApp.models import Quiz


class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['id','title']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','username','email']


class RegisterSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=["name","username","email","password","password2"]
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm Password does not match")
        return attrs

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
