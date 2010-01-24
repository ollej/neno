from django.conf.urls.defaults import *
from django.conf import settings

# Activate admin interface
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('neno.forum.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Serve media files locally
if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)/$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
