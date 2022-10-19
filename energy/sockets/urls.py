"""energy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from energy.sockets.views import sockets_view, find_new_sockets, update_sockets, SocketsUpdateView, change_status

app_name = 'sockets'

urlpatterns = [
    path('', sockets_view, name='sockets'),
    path('new', find_new_sockets, name='sockets-new'),
    path('status_update', update_sockets, name='socket-status-update'),
    path('update/<int:pk>/', SocketsUpdateView.as_view(), name='sockets-update'),
    path('change-status/<int:id>/<str:status>', change_status, name='socket-status-change'),
]
