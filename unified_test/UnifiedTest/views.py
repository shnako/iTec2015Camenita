import uuid

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from UnifiedTest.models import Page
from UnifiedTest.forms import PageForm


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
        form = PageForm(initial={'url': url, 'user': request.user})
    elif request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            # TODO: save the user
            # page = form.save(commit=False)
            #page.user = request.user
            #page.save()
            return HttpResponseRedirect(reverse('view-page', kwargs={'page_id': page.id}))
    return render_to_response('app/create.html', context={'form': form},
                              context_instance=RequestContext(request))


def view_page_details(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    form = PageForm(instance=page)
    return render_to_response('app/view.html', {'form': form},
                              RequestContext(request))


def use_page(request, page_uuid):
    pass
