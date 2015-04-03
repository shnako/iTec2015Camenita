from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from unified_test.decorators import unified_test_api_request
from unified_test.exceptions import UnifiedTestRequestException
from unified_test.parameters import MIN_PASSWORD_LENGTH
from rest_framework import status

__author__ = 'Vlad Iulian Schnakovszki'

# Logs in a new user.
@unified_test_api_request
def login_email_website(request):
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