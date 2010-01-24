from django.conf.urls.defaults import *
from django.conf import settings

# Activate admin interface
from django.contrib import admin
admin.autodiscover()

# REST API
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import XMLResponder
from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from neno.forum.models import Discussion, Post, Profile

"""
Discussions Collection
Display a feed with all available Discussions.
URL = api/discussions
GET = List all Discussions
"""
xml_discussion_collection = Collection(
    queryset = Discussion.objects.all(),
    permitted_methods = ('GET', 'POST'),
    responder = XMLResponder(paginate_by = 10)
)

class AtomResponder(XMLResponder):
    def render(self, object_list):
        """
        Serializes the objects in object_list into an Atom feed.
        """
        f = feedgenerator.Atom1Feed(
            title='Post list',
            description='List of posts',
            subtitle='List of posts',
            link='',
            feed_url='',
            id='/posts',
            guid='',
            author_name='',
            author_email='',
            author_link='',
        )
        for o in object_list:
            f.add_item(
                title=o.atom['title'],
                link=o.atom['link'],
                description=o.atom['description'],
                author_email=o.atom['author_email'],
                author_name=o.atom['author_name'],
                author_link=o.atom['author_link'],
                pubdate=o.created
            )
        response = f.writeString("UTF-8")
        return response


class AtomDiscussionResponder(XMLResponder):
    def render(self, object_list):
        """
        Serializes the first Discussion object in object_list into an Atom feed.
        """
        obj = object_list[0]
        f = feedgenerator.Atom1Feed(
            title=obj.subject,
            description='Discussion: ' + obj.subject,
            subtitle='Discussion: ' + obj.subject,
            link=obj.get_absolute_url(),
            feed_url=obj.get_absolute_url(),
            id='api/discussions/' + str(obj.id),
            guid=obj.get_absolute_url(),
            author_name=obj.author.name,
            author_email=obj.author.email,
            author_link=obj.author.homepage,
        )
        for p in obj.post_set.all():
            f.add_item(
                title=p.atom['title'],
                link=p.atom['link'],
                description=p.atom['description'],
                author_email=p.atom['author_email'],
                author_name=p.atom['author_name'],
                author_link=p.atom['author_link'],
                pubdate=p.created
            )
        response = f.writeString("UTF-8")
        return response

class DiscussionFeed(Collection):
    def get_entry(self, did):
        d = Discussion.objects.get(id=int(did))
        entry = self.entry_class(self, d)
        return entry

    def read(self, request, *args, **kwargs):
        """
        Displays a Discussion with all containing Posts.
        """
        did = int(request.path.split("/")[2])
        d = self.get_entry(did)
        return self.responder.list(request, d)
        # ...

    def create(self, request, *args, **kwargs):
        """
        Create a new Discussion and first Post.
        TODO: Not created.
        """
        # ...

    def update(self, request, *args, **kwargs):
        """
        Update the main information about a Discussion.
        TODO: Not created.
        """
        # ...

    def delete(self, request, *args, **kwargs):
        """
        Deletes a discussion and all containing Posts.
        TODO: Needs permission check.
        """
        for p in self.model.post_set.all():
            p.delete()
        self.model.delete()
        return HttpResponse(_("Discussion successfully deleted."), self.collection.responder.mimetype)
        # ...

"""
Discussion Feed
Display one Discussion and all containing Posts as a feed.
URL = api/discussion/{id}
GET = Feed for Discussion with all Posts as entries.
PUT = Update the main information of the Discussion.
POST = Create new Discussion
DELETE = Delete this Discussion and all containing Posts.
TODO: Should be custom class getting all posts connected to Discussion.
"""
xml_discussion_feed = DiscussionFeed(
    queryset = Discussion.objects.all(),
    permitted_methods = ('GET', 'PUT', 'DELETE'),
    responder = AtomDiscussionResponder(paginate_by = 10)
)

"""
Post Entry
Display information about one Post.
URL = api/posts
GET = Information about the Post.
POST = Create a new Post.
PUT = Update the data for this Post.
DELETE = Delete this Post.
TODO: Should be custom class for a single entry.
"""
xml_post_collection = Collection(
    queryset = Post.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = AtomResponder(paginate_by = 10)
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
    responder = AtomResponder(paginate_by = 10)
)

urlpatterns = patterns('',
    # Example:
    # (r'^neno/', include('neno.foo.urls')),
    url(r'^api/discussions/?$', xml_discussion_collection, name='discussions'),
    url(r'^api/discussion/(.+?)/?$', xml_discussion_feed, name='discussion'),
    url(r'^api/posts/(.*?)/?$', xml_post_collection, name='posts'),
    url(r'^api/profiles/(.*?)/?$', xml_profile_resource, name='profile'),

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
