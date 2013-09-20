from BeautifulSoup import BeautifulStoneSoup
from httplib import HTTPSConnection

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import resolve
from django.shortcuts import render


def html_decorator(func):
    def _decorated(*args, ** kwargs):
        response = func(*args, **kwargs)

        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")

        return HttpResponse(wrapped)

    return _decorated


@html_decorator
def test(request):

    view = resolve("http://127.0.0.1:8000/pin/api/post/?format=json")

    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept
    res = view.func(request, **view.kwargs)

    return HttpResponse(res._container)


TOKEN_VAR = 'contact_token'
TOKEN_IN_GET = 'token'


def gdata_required(f):
    """
    Authenticate against Google GData service
    """
    def wrap(request, *args, **kwargs):
        if TOKEN_IN_GET not in request.GET and TOKEN_VAR not in request.session:
            # no token at all, request one-time-token
            # next: where to redirect
            # scope: what service you want to get access to
            return HttpResponseRedirect("https://www.google.com/accounts/AuthSubRequest?next=http://127.0.0.1:8000/pin/test_page&scope=https://www.google.com/m8/feeds&session=1")
        elif TOKEN_VAR not in request.session and TOKEN_IN_GET in request.GET:
            # request session token using one-time-token
            conn = HTTPSConnection("www.google.com")
            conn.putrequest('GET', '/accounts/AuthSubSessionToken')
            conn.putheader('Authorization', 'AuthSub token="%s"' % request.GET[TOKEN_IN_GET])
            conn.endheaders()
            conn.send(' ')
            r = conn.getresponse()
            if str(r.status) == '200':
                token = r.read()
                token = token.split('=')[1]
                token = token.replace('', '')
                request.session[TOKEN_VAR] = token
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


@gdata_required
def test_page1(request):
    """
    Simple example - list google docs documents
    """
    if TOKEN_VAR in request.session:
        con = HTTPSConnection("www.google.com")
        con.putrequest('GET', '/m8/feeds/contacts/vchakoshy@gmail.com/full')
        con.putheader('Authorization', 'AuthSub token="%s"' % request.session[TOKEN_VAR])
        con.endheaders()
        con.send('')
        r2 = con.getresponse()
        dane = r2.read()
        soup = BeautifulStoneSoup(dane)
        dane = soup.prettify()
        return render(request, 'pin/a.html', {'dane': dane})
    else:
        return render(request, 'pin/a.html', {'dane': 'bad bad'})


def send_mail(request):
    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = 'hello', 'info@wisgoon.com', 'vchakoshy@gmail.com'
    text_content = 'shoma yek payame jadid darid.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse('done')
