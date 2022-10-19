import re
from django.core.management.base import BaseCommand, CommandError
from django.http import JsonResponse
from energy.sockets.models import Sockets
from zeroconf import ServiceBrowser, Zeroconf
import socket
import time
import requests
import json

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

    def update_state(self, ip):
        url = f'http://{ip}/api/v1/state'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                Sockets.objects.filter(ip=ip).update(power_on=data.get('power_on', False), switch_lock=data.get('switch_lock', False))
                return {'ip': ip, 'power_on': data.get('power_on', False), 'switch_lock': data.get('switch_lock', False)}
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
                if not Sockets.objects.filter(network_name=info.name).exists():
                    ip = socket.inet_ntoa(info.addresses[0])
                    Sockets.objects.update_or_create(network_name=info.name, ip=ip, friendly_name='Energy Socket')
                    print(f'Successfully added sockets from ip: {ip}')
                    status.append({'name': info.name, 'ip': ip, 'status': 'added'})
                    self.update_basic_info(ip)
                    self.update_state(ip)
                    return json.dumps(status)
                else:
                    update_status = self.update_state(ip)
                    update_status.update({'name': info.name, 'status': 'updated'})
                    status.append(update_status)
                    return json.dumps(status)
            except Exception as e:
                return json.dumps({'status': 'failed', 'error': f'Failed adding socket with error: {e}'})

class Command(BaseCommand):
    help = 'Find and add new Homewizard Energy sockets to the database'

    def handle(self, *args, **options):
        zeroconf = Zeroconf()
        listener = MyListener()
        browser = ServiceBrowser(zeroconf, "_hwenergy._tcp.local.", listener)        
        time.sleep(10)
        zeroconf.close()