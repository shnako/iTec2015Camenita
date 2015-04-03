from django.shortcuts import render_to_response
from django.template import RequestContext
from unified_test.parameters import MIN_PASSWORD_LENGTH

__author__ = 'VladIulian'


def login(request):
    context = RequestContext(request)

    context_dict = {
        'MIN_PASSWORD_LENGTH': MIN_PASSWORD_LENGTH
    }

    # Render the response and send it back!
    return render_to_response('registration/login.html', context_dict, context)