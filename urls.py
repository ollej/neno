from django.conf.urls.defaults import *

# Activate admin interface
from django.contrib import admin
admin.autodiscover()

# REST API
from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder
from neno.forum.models import Discussion, Post, Profile

"""
Discussion Collection
Display a feed with all available Discussions.
URL = api/discussions
GET = List all Discussions
POST = Create new Discussion
"""
xml_discussion_collection = Collection(
    queryset = Discussion.objects.all(),
    permitted_methods = ('GET', 'POST'),
    responder = XMLResponder(paginate_by = 10)
)


"""
Discussion Entry
Display one Discussion and all containing Posts as a feed.
URL = api/discussion/{id}
GET = Feed for Discussion with all Posts as entries.
PUT = Update the main information of the Discussion.
DELETE = Delete this Discussion and all containing Posts.
TODO: Should be custom class getting all posts connected to Discussion.
"""
xml_discussion_entry = Entry(
    queryset = Discussion.objects.all(),
    permitted_methods = ('GET', 'PUT', 'DELETE'),
    responder = XMLResponder(paginate_by = 10)
)

"""
Post Entry
Display information about one Post.
URL = api/posts
GET = Information about the Post.
PUT = Update the data for this Post.
DELETE = Delete this Post.
TODO: Should be custom class for a single entry.
"""
xml_post_entry = Entry(
    queryset = Post.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = XMLResponder(paginate_by = 10)
)

""""
Profile Collection
Display a feed with all Profiles in the system.
URL = api/profiles
GET = List all Profiles.
POST = Create a new Profile.
PUT = Update a profile.
DELETE = Delete a profile.
"""
xml_profile_resource = Collection(
    queryset = Profile.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = XMLResponder(paginate_by = 10)
)

urlpatterns = patterns('',
    # Example:
    # (r'^neno/', include('neno.foo.urls')),
    url(r'^api/discussions/?$', xml_discussion_collection),
    url(r'^api/discussion/(.+?)/?$', xml_discussion_entry),
    url(r'^api/posts/(.*?)/?$', xml_post_entry),
    url(r'^api/profiles/(.*?)/?$', xml_profile_resource),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # django-openid
)
