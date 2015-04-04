import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import status

from UnifiedTest.models import Page, PageAccessLog
from UnifiedTest.forms import PageForm, PageAuthenticationForm
from user_management.views import login_user


def index(request):
    if request.user.is_authenticated():
        return redirect(pages)
    else:
        return redirect(login_user)


@login_required
def pages(request):
    if request.method == "POST":
        search_query = request.POST.get("SEARCH-QUERY")
        if search_query is not None:
            user_pages = Page.objects.filter(
                Q(ref__icontains=search_query)
                | Q(status_code__icontains=search_query)
                | Q(delay__icontains=search_query)
                | Q(response__icontains=search_query)
                | Q(dynamic_code__icontains=search_query)
                | Q(default_response__icontains=search_query),
                user=request.user
            )
    else:
        user_pages = Page.objects.filter(user=request.user)

    return render_to_response('app/pages.html', {
        'pages': user_pages,
    }, RequestContext(request))


@login_required
def requests(request):
    if request.method == "POST":
        search_query = request.POST.get("SEARCH-QUERY")
        if search_query is not None:
            user_requests = PageAccessLog.objects.filter(
                Q(page__ref__icontains=search_query)
                | Q(timestamp__icontains=search_query)
                | Q(request_method__icontains=search_query)
                | Q(request_body__icontains=search_query)
                | Q(response_body__icontains=search_query),
                user=request.user
            )
    else:
        user_requests = PageAccessLog.objects.filter(page__user=request.user)

    return render_to_response('app/requests.html', {
        'requests': user_requests
    }, RequestContext(request))


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
        page_authentication_form = PageAuthenticationForm(request.POST)
        if page_form.is_valid() and page_authentication_form.is_valid():
            page = page_form.save(commit=False)
            page.user = request.user
            page.save()

            page_authentication = page_authentication_form.save(commit=False)
            page_authentication.page = page
            page_authentication.value = request.POST.get('value')
            page_authentication.save()

            messages.success(request, 'Page details saved.')
            return HttpResponseRedirect(reverse('edit-page',
                                                kwargs={'page_ref': page.ref}))
    return render_to_response('app/page-details.html', context={
        'mode': 'create',
        'page_form': page_form,
        'page_authentication_form': page_authentication_form
    }, context_instance=RequestContext(request))


@login_required
def edit_page(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)

    # Ensure user is page owner.
    if request.user != page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        url = use_page_absolute_url(request, page.ref)
        page_form = PageForm(initial={'url': url}, instance=page)
        auth_form_initial = {
            'type': page.authentication.type,
            'value': page.authentication.value
        }
        page_authentication_form = PageAuthenticationForm(initial=auth_form_initial,
                                                          instance=page.authentication)
    elif request.method == 'POST':
        page_form = PageForm(request.POST, instance=page)
        page_authentication_form = PageAuthenticationForm(request.POST,
                                                          instance=page.authentication)
        if page_form.is_valid() and page_authentication_form.is_valid():
            page_form.save()

            page_authentication = page_authentication_form.save(commit=False)
            page_authentication.value = request.POST.get('value')
            page_authentication.save()
        else:
            print page_form.errors
    return render_to_response('app/page-details.html', context={
        'mode': 'edit',
        'page_form': page_form,
        'page_authentication_form': page_authentication_form
    }, context_instance=RequestContext(request))


@login_required
def view_page_response(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)
    # Ensure user is page owner.
    if request.user != page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return render_to_response('app/text-wrapper.html', context={'text_content': page.response})


@login_required
def view_page_code(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)
    # Ensure user is page owner.
    if request.user != page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return render_to_response('app/text-wrapper.html', context={'text_content': page.dynamic_code})


@login_required
def view_request_details(request, request_id):
    page_access_log = get_object_or_404(PageAccessLog, id=request_id)
    # Ensure user is page owner.
    if request.user != page_access_log.page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return render_to_response('app/text-wrapper.html', context={'text_content': page_access_log.request_body})


@login_required
def view_response_details(request, request_id):
    page_access_log = get_object_or_404(PageAccessLog, id=request_id)
    # Ensure user is page owner.
    if request.user != page_access_log.page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    return render_to_response('app/text-wrapper.html', context={'text_content': page_access_log.response_body})


@login_required
def delete_page(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)

    # Ensure user is page owner.
    if request.user != page.user:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

    try:
        page.access_logs.all().delete()
    except:
        # No access logs, no worries.
        pass

    page.authentication.delete()
    page.delete()

    messages.success(request, 'The page has been deleted.')

    return HttpResponseRedirect(reverse('pages'))
