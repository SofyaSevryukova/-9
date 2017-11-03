from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
import requests
from django.http import HttpResponseRedirect
from .forms import TodolistCreateForm, LoginForm, TodolistUpdateForm, TaskCreateForm
from todolist.services import create_auth_header, convert_from_json_to_obj
from todolist.services import generate_confirmation_token
# Create your views here.

def index(request):
    headers = create_auth_header(request.session)
    r = requests.get('http://127.0.0.1:8080/todolists/', headers=headers)
    todolists = r.json()
    return render(request, 'index.html', {'todolists': todolists, 'session': request.session})

class CreateTodolist(View):
    def get(self, request, *args, **kwargs):
        form = TodolistCreateForm()
        return render(request, 'create_todolist.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TodolistCreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name']}
            headers = create_auth_header(request.session)
            response = requests.post('http://127.0.0.1:8080/todolists/', data=post_data, headers=headers)
            return HttpResponseRedirect('/todolists/')

class ListDetail(View):
    def get(self, request, list_id, *args, **kwargs):
        # return HttpResponse('{} hah'.format(list_id))
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers)
        list_details = r.json()
        return render(request, 'list_detail.html', {'list_details': list_details})

class ListDetailDelete(View):
    def get(self, request, list_id, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.delete('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers)
        return redirect('todolist:index')

class ListDetailUpdate(View):
    def get(self, request, list_id, *args, **kwargs):
        form = TodolistUpdateForm()
        return render(request, 'update_todolist.html', {'form': form, 'list_id': list_id})
    def post(self, request, list_id, *args, **kwargs):
        form = TodolistUpdateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name']}
            headers = create_auth_header(request.session)
            r = requests.put('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers, data=post_data)
            return redirect('todolist:index')

class TaskCreate(View):
    def get(self, request, list_id, *args, **kwargs):
        form = TaskCreateForm()
        return render(request, 'create_task.html', {'form': form, 'list_id': list_id})
    def post(self, request, list_id, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            post_data = {}
            for key in form.cleaned_data:
                post_data[key] = form.cleaned_data[key]
            post_data['tags'] = convert_from_json_to_obj(post_data['tags']) if post_data['tags'] else []
            print(post_data)
            headers = create_auth_header(request.session)
            r = requests.post('http://127.0.0.1:8080/todolists/{}/tasks/'.format(list_id), headers=headers, data=post_data)
            if r.status_code == 400:
                print(r.json())
            return redirect('todolist:list-detail', list_id=list_id)
    # дописать post()
    #     {"tags": [], "name": "", "description": "", "completed": false, "due_date": null, "priority": null}

class TaskUpdate(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        form = TaskCreateForm(r.json())
        return render(request, 'update_task.html', {'form': form, 'list_id': list_id, 'pk': pk})
    def post(self, request, list_id, pk, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            post_data = {}
            for key in form.cleaned_data:
                post_data[key] = form.cleaned_data[key]
            print(post_data['tags'])
            post_data['tags'] = convert_from_json_to_obj(post_data['tags'][1:-1]) if post_data['tags'] else [] # НЕ ВСЕГДА КОРРЕКТНО РАБОТАЕТ
            print(post_data['tags']) # убрать квадратые скобки из JSON репрезентации
            print(post_data)
            headers = create_auth_header(request.session)
            r = requests.put('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers, data=post_data)
            if r.status_code == 400:
                print(r.json())
            return redirect('todolist:list-detail', list_id=list_id)


class TaskDetail(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        task_details = r.json()
        return render(request, 'task_detail.html', {'task_details': task_details, 'list_id': list_id})

class TaskDetailDelete(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.delete('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        return redirect('todolist:list-detail', list_id=list_id)

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
            response = requests.post('http://127.0.0.1:8080/api-token-auth/', data=post_data)
            credentials = response.json()
            if credentials.get('token', False):
                request.session['token'] = credentials['token']
                print('token in session')
                print(request.session['token'])
                return HttpResponseRedirect("/todolists/")
            else:
                print('not found token')
                return HttpResponse("You email/password is wrong!", status=403)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect('/todolists/')

def shared_tasks(request):
    headers = create_auth_header(request.session)
    r = requests.get('http://127.0.0.1:8080/shared/', headers=headers)
    shared_tasks = r.json()
    return render(request, 'shared_tasks.html', {'tasks': shared_tasks})