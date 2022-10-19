from celery import shared_task
from django.http import JsonResponse
from energy.sockets.models import Sockets
from zeroconf import ServiceBrowser, Zeroconf
import socket
import time
import requests
import json
from requests.exceptions import RequestException

@shared_task
def update_sockets_task():
    sockets = Sockets.objects.filter(type='HWE-SKT')
    status_codes = []
    for socket in sockets:
        url = f'http://{socket.ip}/api/v1/state'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                if data.get('power_on') == True:
                    power_on = True
                else:
                    power_on = False

                if data.get('switch_lock') == True:
                    switch_lock = True
                else:
                    switch_lock = False
                Sockets.objects.filter(ip=socket.ip).update(power_on=power_on, switch_lock=switch_lock)
                status_codes.append({'status': 'ok', 'ip': socket.ip, 'power_on': power_on, 'switch_lock': switch_lock})
            except Exception as e:
                return(f'Failed updating socket {socket.ip} with error: {e}')
    return status_codes

class MyListener:
    def update_basic_info(self, ip):
        url = f'http://{ip}/api'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                Sockets.objects.filter(ip=ip).update(type=data.get('product_type', ''), serial=data.get('serial', '')) 
            except Exception as e:
                print(f'Failed updating socket {ip} with error: {e}')

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        status = []
        info = zeroconf.get_service_info(type, name)
        if info: 
            try:
                ip = socket.inet_ntoa(info.addresses[0])
                if not Sockets.objects.filter(network_name=info.name).exists():
                    Sockets.objects.update_or_create(network_name=info.name, ip=ip, friendly_name='Energy Socket')
                    self.update_basic_info(ip)
                    self.update_state(ip)
            except Exception as e:
                return json.dumps({'status': 'failed', 'error': f'Failed adding socket with error: {e}'})

@shared_task
def find_new_sockets_task():
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_hwenergy._tcp.local.", listener)
    time.sleep(10)
    zeroconf.close()

@shared_task
def update_socket_status_task(id, socket_status):
    if socket_status:
        socket = Sockets.objects.get(id=id)
        if socket_status == 'on':
            status = "true"
            socket.power_on = True
            socket.save()
        elif socket_status == 'off':
            status = "false"
            socket.power_on = False
            socket.save()
        else:
            return json.dumps({'status': 'failed', 'error': 'Invalid status'})

    if id:
        url = f"http://{socket.ip}/api/v1/state"
        data = '{"power_on": ' + status + '}'
        try:
            response = requests.put(url, data=data)
            if response.status_code == 200:
                return json.dumps(response.json())
            else:
                return json.dumps({'status': 'failed', 'error': f"Error updating socket status with response {response.json()}"})
        except RequestException as e:
            return json.dumps({'status': 'failed', 'error': f"Request error {e}"})                        
    else:
        return json.dumps({'status': 'failed', 'error': f"No valid ip provided in {socket.ip}"})
