from django.db import models

# Create your models here.


class Payment(models.Model):
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
