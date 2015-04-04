from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices

HTTP_METHODS = Choices('GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'OPTIONS',
                       'HEAD')


class Page(models.Model):
    DEFAULT_RESPONSES = Choices('Static', 'Dynamic')
    user = models.ForeignKey(User, null=True, blank=True)
    ref = models.CharField(max_length=64, unique=True)
    status_code = models.PositiveIntegerField(default=200)
    delay = models.PositiveIntegerField(default=0, null=True, blank=True)
    response = models.TextField(blank=True)
    dynamic_code = models.TextField(blank=True)
    default_response = models.CharField(max_length=50, choices=DEFAULT_RESPONSES,
                                        default=DEFAULT_RESPONSES.Static)

    def __unicode__(self):
        return '{ref}'.format(ref=self.ref)


class PageAccessLog(models.Model):
    page = models.ForeignKey(Page, related_name="access_logs")
    timestamp = models.DateTimeField()
    request_method = models.CharField(max_length=20, choices=HTTP_METHODS)
    request_body = models.TextField()
    response_body = models.TextField(blank=True)

    def __unicode__(self):
        return '{page} - {ts}'.format(page=self.page, ts=self.timestamp)


class PageAuthentication(models.Model):
    AUTH_CHOICES = Choices('None', 'Basic', 'Headers', 'OAuth')
    page = models.OneToOneField(Page, related_name='authentication')
    type = models.CharField(choices=AUTH_CHOICES, default=AUTH_CHOICES.None, max_length=10)
    value = models.CharField(max_length=1024, blank=True)
