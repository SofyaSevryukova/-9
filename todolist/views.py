from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework import generics
from .serializers import TaskSerializer, TasklistSerializer, TagSerializer, UserRegistrationSerializer
from .models import Task, Tasklist, Tag
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework import permissions


class ProhibitionRegistration(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated()


class TasklistCreateView(generics.ListCreateAPIView):
    serializer_class = TasklistSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Tasklist.objects.all()
        try:
            queryset = queryset.filter(owner=self.request.user.id)
        except:
            pass
        return queryset


class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TasklistSerializer

    def get_queryset(self):
        queryset = Tasklist.objects.all()
        try:
            queryset = queryset.filter(owner=self.request.user.id)
        except:
            pass
        return queryset


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id).filter(tasklist__owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.filter(owner=self.request.user).get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id).filter(tasklist__owner=self.request.user)
        return queryset

class TagCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class UserCreateView(generics.CreateAPIView):
    permission_classes = (ProhibitionRegistration, )
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
