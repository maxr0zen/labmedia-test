from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = 'clients'
        indexes = [
            models.Index(fields=['country'], name='client_country_idx'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
