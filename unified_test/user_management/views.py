from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import re
from rest_framework import status
from unified_test.decorators import unified_test_api_request
from unified_test.exceptions import UnifiedTestRequestException
from unified_test.parameters import MIN_PASSWORD_LENGTH


@unified_test_api_request
def login_user(request):
    if request.method == "GET":
        context = RequestContext(request)
        context_dict = {
            'MIN_PASSWORD_LENGTH': MIN_PASSWORD_LENGTH
        }
        # Render the response and send it back!
        return render_to_response('registration/login.html', context_dict, context)
    elif request.method == "POST":
        _login_user(request)
        return HttpResponse(status=status.HTTP_200_OK)


# Logs a user in if valid credentials. Will propagate exceptions.
def _login_user(request):
    # Django's ORM protects against SQL Injection attacks.
    # Ensure email address is not null.
    email = request.POST.get('EMAIL')
    if email is None:
        raise UnifiedTestRequestException('Missing email address!')
    # Ensure email address is valid.
    try:
        validate_email(email)
    except ValidationError:
        raise UnifiedTestRequestException('Invalid email address!')

    # Validate password.
    password = request.POST.get('PASSWORD')
    if password is None:
        raise UnifiedTestRequestException('Missing password!')
    if len(password) < MIN_PASSWORD_LENGTH:
        raise UnifiedTestRequestException("Password must contain at least " + str(MIN_PASSWORD_LENGTH) + " characters!")

    # Login the user for this session. Will generate.
    user = authenticate(username=email, password=password)
    if user is None:
        raise UnifiedTestRequestException('Invalid credentials!')
    login(request, user)


# Creates a new user from the website.
@unified_test_api_request
def register(request):
    # Will propagate all exceptions.
    _validate_create_user_parameters(request)
    _create_user(request)
    return HttpResponse(status=status.HTTP_200_OK)


def _validate_create_user_parameters(request):
    # Django's ORM protects against SQL Injection attacks.
    # Ensure email address is not null.
    email = request.POST.get('EMAIL')
    if request.POST.get('EMAIL') is None:
        raise UnifiedTestRequestException('Missing email address!')
    # Ensure email address is valid.
    try:
        validate_email(email)
    except ValidationError:
        raise UnifiedTestRequestException('Invalid email address!')
    # Ensure email is unique. Will generate an exception if not.
    try:
        User.objects.get(email=email)
        raise UnifiedTestRequestException('There is already a registered user with this email address! Please log in!')
    except User.DoesNotExist:
        # All good, move along.
        pass

    # Ensure first name is not null.
    first_name = request.POST.get('FIRST-NAME')
    if first_name is None:
        raise UnifiedTestRequestException('Missing first name!')
    # Ensure first name is valid.
    if not is_valid_name(first_name):
        raise UnifiedTestRequestException('Invalid first name!')

    # Ensure last name is not null.
    last_name = request.POST.get('LAST-NAME')
    if last_name is None:
        raise UnifiedTestRequestException('Missing last name!')
    # Ensure last name is valid.
    if not is_valid_name(last_name):
        raise UnifiedTestRequestException('Invalid last name!')

    # Validate password.
    password = request.POST.get('PASSWORD')
    if password is None:
        raise UnifiedTestRequestException('Missing password!')
    if len(password) < MIN_PASSWORD_LENGTH:
        raise UnifiedTestRequestException("Password must contain at least " + str(MIN_PASSWORD_LENGTH) + " characters!")


def _create_user(request):
    # Create the user object.
    User.objects.create_user(username=request.POST.get('EMAIL'),
                             email=request.POST.get('EMAIL'),
                             password=request.POST.get('PASSWORD'),
                             first_name=request.POST.get('FIRST-NAME'),
                             last_name=request.POST.get('LAST-NAME'))

    # Login the user for this session
    user = authenticate(username=request.POST.get('EMAIL'), password=request.POST.get('PASSWORD'))
    login(request, user)


# Validates a string as a full name.
def is_valid_name(name):
    # Ensure not null.
    if name is None:
        return False
    # Validate with a regex.
    regex = re.compile("[a-zA-Z-' ]+")
    return regex.match(name)