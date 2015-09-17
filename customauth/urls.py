from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    url(r'^register$', 'customauth.views.register', name='res'),
    url(r'^registerme$', 'customauth.views.registerme', name='reg'),
    url(r'^loginme$', 'customauth.views.loginme', name='log'),
    url(r'^checklogin$', 'customauth.views.checklogin', name='chklogin'),
    url(r'^simpleregister$', 'customauth.views.simple_registerme', name='simpleregister'),
    url(r'^logoutme$', 'customauth.views.logout', name='logout'),

)

