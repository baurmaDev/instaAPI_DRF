from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount, Post



class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['id', 'nickname', 'bio',  'phone_number']


class UserSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password','user_account']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_account_data = validated_data.pop('user_account')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        if user_account_data:
            UserAccount.objects.create(user=user, **user_account_data)
        return user


class PostSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user_account',  'caption', 'created_at', 'updated_at']

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        # instance.image = validated_data.get('image', instance.image)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('A username is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials. Please try again.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {'user': user}