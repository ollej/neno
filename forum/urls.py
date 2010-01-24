# REST API
from neno.forum.rest_api import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^discussions/?$', xml_discussion_collection, name='discussions'),
    url(r'^discussion/(.+?)/?$', xml_discussion_feed, name='discussion'),
    url(r'^posts/(.*?)/?$', xml_post_collection, name='posts'),
    url(r'^profiles/(.*?)/?$', xml_profile_resource, name='profile'),
)

