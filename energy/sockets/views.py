from django.shortcuts import render
from energy.sockets.forms import SocketsForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from energy.sockets.models import Sockets
from django.core.management import call_command
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.core import serializers
from energy.tasks import find_new_sockets_task, update_socket_status_task, update_sockets_task
import json

def sockets_view(request):
    sockets = Sockets.objects.all()
    context = {'sockets': sockets}
    return render(request, 'sockets/sockets_list.html', context)

class SocketsUpdateView(UpdateView):
    model = Sockets
    form_class = SocketsForm
    template_name = 'sockets/sockets_form.html'
    success_url = reverse_lazy('sockets:sockets')

def update_sockets(request):
    try:
        update_sockets_task.delay()
        return redirect('sockets:sockets')
    except Exception as e:
        return JsonResponse({'status': 'failed', 'error': f'Failed updating sockets with error: {e}'})


def find_new_sockets(self):
    try:
        find_new_sockets_task.delay()
        return redirect('sockets:sockets')
    except:
        return redirect('sockets:sockets')

def change_status(request, id, status):
    """
    Change the power_on status of a socket, after save the signal will be
    called to turn on/off the socket 
    """
    socket = Sockets.objects.get(pk=id)
    if isinstance(socket, Sockets):
        if status == 'on':
            socket.power_on = True
            update_socket_status_task.delay(socket.id, 'on')
        elif status == 'off':
            socket.power_on = False
            update_socket_status_task.delay(socket.id, 'off')
        else:
            return redirect('sockets:sockets')
        socket.save()
    else:
        return JsonResponse({'status': 'failed', 'error': 'Socket not found'})
        #return json.dumps({'status': 'failed', 'error': 'Socket not found'})

    return redirect('sockets:sockets')
