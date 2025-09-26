from app import models
from rest_framework import serializers
from django.contrib.auth import get_user_model


User=get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=models.User
        fields=[
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'confirm_password',
            'role',
            'is_deleted'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields=[
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'role',
            'is_deleted'
        ]
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Task
        fields='__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }