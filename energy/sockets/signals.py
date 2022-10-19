# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from energy.sockets.models import Sockets
# import requests
# import json

# @receiver(post_save, sender=Sockets)
# def update_socket_status(sender, instance, created, **kwargs):
#     if not created:
#         if instance.ip:
#             url = f"http://{instance.ip}/api/v1/state"
#             data = '{"power_on": ' + str(instance.power_on).lower() + '}'
#             response = requests.put(url, data=data)
#             if response.status_code == 200:
#                 print("Socket status updated")
#             else:
#                 print(f"Error updating socket status with response {response.json()}")
#         else:
#             print(f"No IP address found in signal {instance}")
    