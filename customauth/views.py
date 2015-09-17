from django.shortcuts import render
import json
from django.contrib.gis.geos import Point
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from registration import signals
from registration.models import RegistrationProfile
from django.contrib.auth.models import User





import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.module_loading import import_by_path
from django.middleware.csrf import rotate_token

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
REDIRECT_FIELD_NAME = 'next'





def register(request):
    return render(request, 'custom_form.html')
def printdata(request):
    
    print json.dumps(request.POST['json_data'])


def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
    
        
        
# Create your views here.
@csrf_exempt
def registerme(request):
    """
    Given a username, email address and password, register a new
    user account, which will initially be inactive.

    Along with the new ``User`` object, a new
    ``registration.models.RegistrationProfile`` will be created,
    tied to that ``User``, containing the activation key which
    will be used for this account.

    An email will be sent to the supplied email address; this
    email should contain an activation link. The email will be
    rendered using two templates. See the documentation for
    ``RegistrationProfile.send_activation_email()`` for
    information about these templates and the contexts provided to
    them.

    After the ``User`` and ``RegistrationProfile`` are created and
    the activation email is sent, the signal
    ``registration.signals.user_registered`` will be sent, with
    the new ``User`` as the keyword argument ``user`` and the
    class of this backend as the sender.

    """
    
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        
        if User.objects.filter(username=username).exists():
            return HttpResponse(2001) #username already in use
        if not (validateEmail(email)):
            return HttpResponse(2002) #not a valid email address
        if User.objects.filter(email=email).exists():
            return HttpResponse(2003) #user email
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        return HttpResponse(2000)   # registration successful check ur email

@csrf_exempt
def simple_registerme(request):
    
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        first_name= request.POST['firstname']
        last_name= request.POST['lastname']
        if User.objects.filter(username=username).exists():
            return HttpResponse(2001) #username already in use
        if not (validateEmail(email)):
            return HttpResponse(2002) #not a valid email address
        if User.objects.filter(email=email).exists():
            return HttpResponse(2003) #user email
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        
        return HttpResponse(2000)   # registration successful check ur email

from django.contrib.auth import authenticate, login   
@csrf_exempt   
def loginme(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(3000) # on client, save session ID
        else:
            return HttpResponse(3001)
    else:
        return HttpResponse(3003)
        
        
@csrf_exempt
def checklogin(request):
    if request.user.is_authenticated():
        return HttpResponse("user is authenticated")
    else:
        return HttpResponse("user is NOT authenticated")
@csrf_exempt
def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    #user_logged_out.send(sender=user.__class__, request=request, user=user)

    # remember language choice saved to session
    language = request.session.get('django_language')

    request.session.flush()

    if language is not None:
        request.session['django_language'] = language

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    # Do something for anonymous users.
#         if username and password:
#             self.user_cache = authenticate(username=username, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
#             elif not self.user_cache.is_active:
#                 raise forms.ValidationError(_("This account is inactive."))
#     username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
#     if Site._meta.installed:
#         site = Site.objects.get_current()
#     else:
        
#     signals.user_registered.send(sender=self.__class__,
#                                  user=new_user,
#                                  request=request)
# Create your views here.
