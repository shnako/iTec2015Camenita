import uuid
import urlparse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from annoying.decorators import render_to

from UnifiedTest.models import Page
from UnifiedTest.forms import CreatePageForm


def login(request):
    context = RequestContext(request)
    context_dict = {
    }

    # Render the response and send it back!
    return render_to_response('registration/login.html', context_dict, context)


def index(request):
    create_url = request.build_absolute_uri(reverse('create-page'))
    context = {'create_url': create_url}
    return render_to_response('app/index.html', context,
                              RequestContext(request))

def get_unique_page_id():
    generated_uuid = uuid.uuid4().hex
    ok = False
    while not ok:
        if Page.objects.filter(url__icontains=generated_uuid).count() != 0:
            generated_uuid = uuid.uuid4().hex
        else:
            ok = True

    return generated_uuid

def create_page(request):
    if request.method == 'GET':
        generated_uuid = get_unique_page_id()
        relative_url = reverse('use-page', kwargs={'page_uuid': generated_uuid})
        url = request.build_absolute_uri(relative_url)
        form = CreatePageForm(initial={'url': url, 'user': request.user})
    elif request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: save the user
            #page = form.save(commit=False)
            #page.user = request.user
            #page.save()
            # TODO: redirect to view page
            return HttpResponseRedirect(reverse(create_page))
    return render_to_response('app/create.html', context={'form': form},
                              context_instance=RequestContext(request))

def use_page(request, page_uuid):
    pass
