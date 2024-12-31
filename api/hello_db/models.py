from django.db import models

class Hello(models.Model):
    world = models.CharField(max_length=100)

    class Meta:
        db_table = "helllo"
        