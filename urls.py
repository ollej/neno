from django.conf.urls.defaults import *
from django.conf import settings

# Activate admin interface
from django.contrib import admin
admin.autodiscover()

# REST API
#from neno.forum import rest_api

urlpatterns = patterns('',
    # Example:
    # (r'^neno/', include('neno.foo.urls')),
    (r'^api/', include('neno.forum.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # django-openid
)

# Serve media files locally
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)/$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
