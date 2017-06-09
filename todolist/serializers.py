from rest_framework import serializers
from .models import Task, Tasklist, Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    tasks = serializers.SlugRelatedField(many=True, queryset=Task.objects.all(), slug_field='name')

    class Meta:
        model = Tag
        fields = ('tag', 'tasks')
        read_only_fields = ('tasks',)


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='tag')
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority', 'tags')
        read_only_fields = ('date_created', 'date_modified', 'tags')


class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tasklist
        fields = ('id', 'name', 'tasks', 'owner')
        read_only_fields = ('tasks','owner', )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password', )
        read_only_fields = ('id', )


    def create(self, user_data):
        user = User.objects.create(username=user_data['username'],)
        user.set_password(user_data['password'])
        user.save()
        return user