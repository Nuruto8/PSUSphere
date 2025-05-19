from django.db import models

class FireStation(models.Model):
    name = models.CharField(max_length=100)
<<<<<<< HEAD
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    city = models.CharField(max_length=100, default='Puerto Princesa')  # Added default
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.city})"
=======
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.name
>>>>>>> 6d9f211cbaf99d243be40ee4aeec0678e7b05933
