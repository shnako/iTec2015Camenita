from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    user = models.ForeignKey(User)
    status_code = models.PositiveIntegerField(default=200)
    delay = models.PositiveIntegerField(default=0, null=True, blank=True)
    response = models.TextField()
    dynamic_code = models.TextField()


class PageAccessLog(models.Model):
    HTTP_METHODS = ['get', 'put', 'post', 'delete', 'options', 'head']
    HTTP_METHODS_CHOICES = ((method, method.upper()) for method in HTTP_METHODS)

    page = models.ForeignKey(Page)
    timestamp = models.DateTimeField()
    request_type = models.CharField(max_length=20, choices=HTTP_METHODS_CHOICES)
    request_body = models.TextField()
    response_body = models.TextField()
