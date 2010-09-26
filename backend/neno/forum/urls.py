# REST API
from neno.forum.rest_api import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^discussions/?$', atom_discussions_feed, name='discussions'),
    url(r'^discussion/(.+?)/?$', atom_discussion_resource, name='discussion'),
    url(r'^post/(.*?)/?$', atom_post_resource, name='post'),
    url(r'^profiles/?$', atom_profile_collection, name='profiles'),
    # FIXME: profile viewing doesn't seem to work in djang 1.1.1
    #url(r'^profile/(.*?)/?$', atom_profile_resource, name='profile'),
)

