from django.contrib import admin
from django.urls import path
from energy.api.views import api_sockets_view, api_find_new_sockets, api_socket_status, api_update_sockets

app_name = 'api'

urlpatterns = [
    path('', api_sockets_view, name='api-root'),
    path('sockets', api_sockets_view, name='api-sockets'),
    path('sockets/update', api_update_sockets, name='api-sockets-update'),
    path('sockets/new', api_find_new_sockets, name='api-sockets-new'),
    path('sockets/status/<int:id>/<str:status>', api_socket_status, name='api-socket-status-update'),
]