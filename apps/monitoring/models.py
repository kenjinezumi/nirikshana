from django.db import models
from apps.articles.utils import detect_language

import time

class Events(models.Model):
    VALIDATION_STAGES = (
        ('Approved', 'approved'),
        ('To be reviewed', 'to_be_reviewed'),
        ('Rejected', 'rejected'),
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.TextField(null=False, blank=False, default=str(time.time()))
    validation_stage = models.CharField(max_length=50, choices=VALIDATION_STAGES)

    def __str__(self):
        return self.title

    @property
    def article_language(self):
        return detect_language(self.article_content)





