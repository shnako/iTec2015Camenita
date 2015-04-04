import uuid
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from UnifiedTest.models import Page
from UnifiedTest.forms import PageForm
from user_management.views import login_user


def index(request):
    if request.user.is_authenticated():
        return redirect(pages)
    else:
        return redirect(login_user)


@login_required
def pages(request):
    user_pages = Page.objects.filter(user=request.user)
    context = {'pages': user_pages}
    return render_to_response('app/pages.html', context, RequestContext(request))


def get_unique_page_id():
    generated_uuid = uuid.uuid4().hex
    ok = False
    while not ok:
        if Page.objects.filter(url__icontains=generated_uuid).count() != 0:
            generated_uuid = uuid.uuid4().hex
        else:
            ok = True

    return generated_uuid


@login_required
def create_page(request):
    if request.method == 'GET':
        generated_uuid = get_unique_page_id()
        relative_url = reverse('use-page', kwargs={'page_ref': generated_uuid})
        url = request.build_absolute_uri(relative_url)
        form = PageForm(initial={'url': url, 'ref': generated_uuid})
    elif request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            # page.user = request.user
            page.save()
            return HttpResponseRedirect(reverse('view-page',
                                                kwargs={'page_ref': page.ref}))
    return render_to_response('app/create.html', context={'form': form},
                              context_instance=RequestContext(request))


@login_required
def view_page_details(request, page_ref):
    # TODO Verify user is owner
    page = get_object_or_404(Page, ref=page_ref)
    form = PageForm(instance=page)
    return render_to_response('app/view.html', {'form': form},
                              RequestContext(request))
