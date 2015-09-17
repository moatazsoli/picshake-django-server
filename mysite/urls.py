from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView
urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="index_constr.html")),
    # url(r'^blog/', include('blog.urls')),
    url(r'^customauth/', include('customauth.urls')),
    (r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
