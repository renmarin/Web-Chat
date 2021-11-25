from django.db import models
from datetime import datetime


class Chat(models.Model):
    room = models.CharField(max_length=255, default='dev_room')
    name = models.CharField(max_length=70)
    date = models.DateTimeField(default=datetime.now())
    message = models.CharField(max_length=1500)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.name} {self.date} {self.message}'
