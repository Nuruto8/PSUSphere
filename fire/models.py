from django.db import models

class FireStation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    city = models.CharField(max_length=100, default='Puerto Princesa')  # Added default
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.city})"