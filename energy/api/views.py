from django.http import JsonResponse
from energy.sockets.models import Sockets
import json 
from energy.tasks import find_new_sockets_task, update_socket_status_task, update_sockets_task

def api_sockets_view(request):
    """
    API endpoint that shows all sockets information
    """
    data = Sockets.objects.filter(type='HWE-SKT').values()
    return JsonResponse(list(data), safe=False)

def api_find_new_sockets(request):
    """
    API endpoint that refreshes all sockets information
    """
    try:
        find_new_sockets_task.delay()
        return JsonResponse({'status': 'ok'}, safe=False)
    except:
        return JsonResponse({'status': 'error', 'message': 'Error refreshing sockets'}, safe=False)

def api_update_sockets(request):
    """
    API endpoint that refreshes all sockets information
    """
    try:
        update_sockets_task.delay()
        return JsonResponse({'status': 'ok'}, safe=False)
    except:
        return JsonResponse({'status': 'error', 'message': 'Error refreshing sockets'}, safe=False)

def api_socket_status(request, id, status):
    """
    API endpoint that enables to change the power_on status of a socket
    """
    socket = Sockets.objects.get(pk=id)
    if isinstance(socket, Sockets):
        if status == 'on':
            socket.power_on = True
            socket.save()
            update_socket_status_task.delay(socket.id, 'on')
            return JsonResponse({'status': 'ok'}, safe=False)
        elif status == 'off':
            socket.power_on = False
            socket.save()
            update_socket_status_task.delay(socket.id, 'off')
            return JsonResponse({'status': 'ok'}, safe=False)
        else:
            return JsonResponse({'status': 'failed', 'error': 'Socket not found'})
        
    return JsonResponse({'status': 'failed', 'error': 'Socket not found'})
