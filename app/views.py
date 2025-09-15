from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app import models
from app import serializers
from app.tasks import send_daily_summary

# Create your views here.


class UserRegisterView(GenericViewSet, mixins.CreateModelMixin):
    queryset=models.User.objects.none()
    serializer_class=serializers.UserRegisterSerializer
    permission_classes = []
    http_method_names = ['post']



class UserEditView(
                    GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin
                   ):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserEditSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return self.queryset.filter(is_deleted=False)
        else:
            return self.queryset.filter(id=self.request.user.id, is_deleted=False)
    
    def destroy(self, request, *args, **kwargs):
        
        if request.user.role == 'admin':
           instance = self.get_object()
        else:
            instance = request.user

        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TasksViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return self.queryset.filter(is_deleted=False)
        else:
            return self.queryset.filter(user=self.request.user, is_deleted=False)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()