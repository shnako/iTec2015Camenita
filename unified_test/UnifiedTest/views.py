import uuid
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import status

from UnifiedTest.models import Page, PageAccessLog
from UnifiedTest.forms import PageForm, PageAuthenticationForm
from unified_test.exceptions import UnifiedTestRequestException
from user_management.views import login_user


def index(request):
    if request.user.is_authenticated():
        return redirect(pages)
    else:
        return redirect(login_user)


def build_absolute_urls(request, pages, url_name):
    urls = {}
    for page in pages:
        relative_url = reverse(url_name, kwargs={'page_ref': page.ref})
        absolute_url = request.build_absolute_uri(relative_url)
        urls[page.ref] = absolute_url

    return urls

@login_required
def pages(request):
    user_pages = Page.objects.filter(user=request.user)
    edit_page_absolute_urls = build_absolute_urls(request, user_pages,
                                                  'edit-page')
    use_absolute_urls = build_absolute_urls(request, user_pages, 'use-page')
    view_page_response_absolute_urls = build_absolute_urls(request, user_pages,
                                                           'view-page-response')
    view_page_code_absolute_urls = build_absolute_urls(request, user_pages,
                                                       'view-page-code')
    context = {
        'pages': user_pages,
        'edit_page_absolute_urls': edit_page_absolute_urls,
        'use_absolute_urls': use_absolute_urls,
        'view_page_response_absolute_urls': view_page_response_absolute_urls,
        'view_page_code_absolute_urls': view_page_code_absolute_urls
    }
    return render_to_response('app/pages.html', context, RequestContext(request))


@login_required
def requests(request):
    user_pages = Page.objects.filter(user=request.user)
    user_requests = PageAccessLog.objects.filter(page__in=user_pages)
    context = {'requests': user_requests}
    return render_to_response('app/requests.html', context, RequestContext(request))


def get_unique_page_id():
    generated_uuid = uuid.uuid4().hex
    ok = False
    while not ok:
        if Page.objects.filter(ref__icontains=generated_uuid).count() != 0:
            generated_uuid = uuid.uuid4().hex
        else:
            ok = True

    return generated_uuid

def use_page_absolute_url(request, page_ref):
    relative_url = reverse('use-page', kwargs={'page_ref': page_ref})
    return request.build_absolute_uri(relative_url)


@login_required
def create_page(request):
    if request.method == 'GET':
        generated_uuid = get_unique_page_id()
        url = use_page_absolute_url(request, generated_uuid)
        page_form = PageForm(initial={'url': url, 'ref': generated_uuid})
        page_authentication_form = PageAuthenticationForm()
    elif request.method == 'POST':
        page_form = PageForm(request.POST)
        if page_form.is_valid():
            page = page_form.save(commit=False)
            page.user = request.user
            page.save()
            return HttpResponseRedirect(reverse('edit-page',
                                                kwargs={'page_ref': page.ref}))
    return render_to_response('app/create.html', context={'page_form': page_form, 'page_authentication_form': page_authentication_form},
                              context_instance=RequestContext(request))


@login_required
def edit_page(request, page_ref):
    # TODO Verify user is owner
    if request.method == 'GET':
        page = get_object_or_404(Page, ref=page_ref)
        url = use_page_absolute_url(request, page.ref)
        form = PageForm(initial={'url': url}, instance=page)
    elif request.method == 'POST':
        page = get_object_or_404(Page, ref=page_ref)
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    return render_to_response('app/edit-page.html', {'form': form},
                                RequestContext(request))

@login_required
def view_page_response(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)
    return HttpResponse(page.response)


@login_required
def view_page_code(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)
    return HttpResponse(page.dynamic_code)

@login_required
def view_request_details(request, request_id):
    try:
        request_object = PageAccessLog.objects.get(id=request_id)
        if request.user != request_object.page.user:
            raise PermissionDenied
    except:
        # Not going into details to avoid leaking information.
        raise UnifiedTestRequestException("Invalid request id!")

    return HttpResponse(request_object.request_body, status=status.HTTP_200_OK)

@login_required
def view_response_details(request, request_id):
    try:
        response_object = PageAccessLog.objects.get(id=request_id)
        if request.user != response_object.page.user:
            raise PermissionDenied
    except:
        # Not going into details to avoid leaking information.
        raise UnifiedTestRequestException("Invalid request id!")

    return HttpResponse(response_object.response_body, status=status.HTTP_200_OK)
