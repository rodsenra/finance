from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    url(r'^pie_macro/(?P<year>\d{4})/(?P<month>\d{2})/$', 'myproject.views.pie_macro'),
    url(r'^pie_micro/(?P<year>\d{4})/(?P<month>\d{2})/$', 'myproject.views.pie_micro'),                       
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
