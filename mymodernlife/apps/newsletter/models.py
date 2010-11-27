from django.db import models

class EmailSubscription(models.Model):
    email = models.EmailField()
