from django.contrib.auth.models import User, update_last_login
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import authenticate

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterStaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attr):
        if attr["password"] != attr["password2"]:
            raise serializers.ValidationError({"password": "Passwords didn't match."})

        return attr

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            # create a staff user
            is_staff=True,
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def validate(self, attr):
        username = attr["username"]
        password = attr["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                "User with given username and password does not exists."
            )

        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)

        return {"token": token}
