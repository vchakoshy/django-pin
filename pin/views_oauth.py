from hashlib import md5
from random import random

import gdata.contacts.data
from gdata.contacts.client import ContactsClient, ContactsQuery
from gdata.gauth import AuthSubToken

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page, cache_control
from django.template.loader import render_to_string

from user_profile.models import Profile

if settings.DEBUG:
	MAX_RESULT = 25
	PAGING = False
	TEST_PAGE_URL = 'http://127.0.0.1:8000/pin/invite/google'
else:
	MAX_RESULT = 100000
	PAGING = True
	TEST_PAGE_URL = 'http://www.wisgoon.com/pin/invite/google'

def GetAuthSubUrl():
    domain = 'www.wisgoon.com'
    next = TEST_PAGE_URL
    scopes = ['http://www.google.com/m8/feeds/']
    secure = False  # set secure=True to request a secure AuthSub token
    session = True
    return gdata.gauth.generate_auth_sub_url(next, scopes, secure=secure, session=session)

def invite_google(request):

    all_emails = []
    if 'token' in request.GET:

        token = request.GET['token']
        token_auth_login = AuthSubToken(token)
        
        query = ContactsQuery()
        query.max_results = MAX_RESULT

        client = ContactsClient(auth_token=token_auth_login)
        client.upgrade_token(token=token_auth_login)

        try:
            feed = client.GetContacts(q=query)
            while feed:
                next = feed.GetNextLink()

                for entry in feed.entry:
                    try:
                        email_address = entry.email[0].address
                        #print email_address
                        all_emails.append(email_address)
                    except:
                        pass

                feed = None
                if PAGING and next:
                    feed = client.GetContacts(next.href, auth_token=token_auth_login, q=query)
        except:
            pass

    return render(request , 'pin/invite_google.html', {'login': GetAuthSubUrl(), 'all_emails':all_emails})


@login_required
def activation_email(request):

    user = request.user
    profile = user.profile
    if profile.activation_key == str(0):
        salt = md5(str(random())).hexdigest()[:5]
        profile.activation_key = md5(salt+user.username).hexdigest()
        
        profile.save()

    ctx_dict = {'activation_key': profile.activation_key}

    subject = render_to_string('registration/activation_email_subject.txt',
                               ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('registration/activation_email.txt',
                               ctx_dict)
    
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            
    return render(request, 'pin/activation.html')

def activation_email_key(request):
    pass
