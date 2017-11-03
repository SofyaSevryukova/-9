from django.conf.urls import url
from . import views

app_name = 'todolist'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.CreateTodolist.as_view(), name='create_todolist'),
    url(r'^(?P<list_id>[0-9]+)/$', views.ListDetail.as_view(), name='list-detail'),
    url(r'^(?P<list_id>[0-9]+)/update/$', views.ListDetailUpdate.as_view(), name='update_todolist'),
    url(r'^(?P<list_id>[0-9]+)/delete/$', views.ListDetailDelete.as_view(), name='list-detail-delete'),
    url(r'^(?P<list_id>[0-9]+)/create/$', views.TaskCreate.as_view(), name='create_task'),
    url(r'^(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view(), name='task-detail'),
    url(r'^(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/update/$', views.TaskUpdate.as_view(), name='task-detail-update'),
    url(r'^(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/delete/$', views.TaskDetailDelete.as_view(), name='task-detail-delete'),
    url(r'^shared/$', views.shared_tasks, name='shared-tasks'),
]

