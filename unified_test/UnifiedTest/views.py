from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext


def Login(request):
    context = RequestContext(request)
    context_dict = {
    }

    # Render the response and send it back!
    return render_to_response('registration/login.html', context_dict, context)