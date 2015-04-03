from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices

HTTP_METHODS = Choices('GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'HEAD')


class Page(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    ref = models.CharField(max_length=64)
    url = models.CharField(max_length=200)
    status_code = models.PositiveIntegerField(default=200)
    delay = models.PositiveIntegerField(default=0, null=True, blank=True)
    response = models.TextField()
    dynamic_code = models.TextField(blank=True)

    def __unicode__(self):
        return '{url}'.format(url=self.url)


class PageAccessLog(models.Model):
    page = models.ForeignKey(Page)
    timestamp = models.DateTimeField()
    request_type = models.CharField(max_length=20, choices=HTTP_METHODS)
    request_body = models.TextField()
    response_body = models.TextField()

    def __unicode__(self):
        return '{page} - {ts}'.format(page=self.page, ts=self.timestamp)
