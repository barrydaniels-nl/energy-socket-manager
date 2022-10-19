from django.db import models
# Create your models here.

class Sockets(models.Model):
    network_name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    power_on = models.BooleanField(default=False)
    switch_lock = models.BooleanField(default=False)
    serial = models.CharField(max_length=100, blank=True, null=True)
    ip = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)

    def __str__(self):
        return self.friendly_name

    def turn_on(self):
        """
        Set power_on to True, signal update_socket_status() will be called
        to turn on socket via the API
        """
        self.power_on = True
        self.save()

    def turn_off(self):
        """
        Set power_on to False, signal update_socket_status() will be called
        to turn off socket via the API
        """
        self.power_on = False
        self.save()
    
    class Meta:
        verbose_name_plural = 'Sockets'
