# REST API
from neno.forum.models import Discussion, Post, Profile
from neno.forum.atom import *;
from django_restapi.model_resource import Collection, Entry
#from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

"""
Discussions Collection
Display a feed with all available Discussions.
URL = api/discussions
GET = List all Discussions
"""
atom_discussions_feed = Collection(
    queryset = Discussion.objects.all(),
    permitted_methods = ('GET', 'POST'),
    responder = AtomResponder(paginate_by = 10)
)

"""
Discussion Feed
Display one Discussion and all containing Posts as a feed.
URL = api/discussion/{id}
GET = Feed for Discussion with all Posts as entries.
PUT = Update the main information of the Discussion.
POST = Create new Discussion
DELETE = Delete this Discussion and all containing Posts.
"""
atom_discussion_resource = DiscussionFeed()

"""
Post Collection
Display information about one Post.
URL = api/post
GET = Information about the Post.
POST = Create a new Post.
PUT = Update the data for this Post.
DELETE = Delete this Post.
TODO: Should be custom class for a single entry.
"""
atom_post_resource = Collection(
    queryset = Post.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = AtomResponder(paginate_by = 10)
)

""""
Profile Collection
Display a feed with all Profiles in the system.
URL = api/profile
GET = List all Profiles.
POST = Create a new Profile.
PUT = Update a profile.
DELETE = Delete a profile.
"""
atom_profile_collection = Collection(
    queryset = Profile.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = AtomResponder(paginate_by = 10)
)
atom_profile_resource = Entry(atom_profile_collection, Profile)

