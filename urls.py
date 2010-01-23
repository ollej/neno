from django.conf.urls.defaults import *

# Activate admin interface
from django.contrib import admin
admin.autodiscover()

# REST API
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import XMLResponder
from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from django.utils.feedgenerator import Atom1Feed
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

class DiscussionAtomFeed(Feed):
    feed_type = Atom1Feed

    def set_object(self, obj):
        self.obj = obj

    def get_object(self, bits):
        # If there already is an object set, just return that.
        if self.obj:
            return self.obj
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Discussion.objects.get(id__exact=bits[0])

    def items(self, obj):
        return obj.posts

    def title(self, obj):
        return obj.subject

    def subtitle(self, obj):
        return "Posts in the Discussion about: " + obj.subject

    def author_name(self, obj):
        return obj.posts[0].author.name

    def author_email(self, obj):
        return obj.posts[0].author.email

    def author_link(self, obj):
        return obj.posts[0].author.homepage

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "discussion/" + obj.id

    def item_author_name(self, item):
        return item.author.name

    def item_author_email(self, item):
        return item.author.email

    def item_author_link(self, item):
        return item.author.homepage

    def item_pubdate(self, item):
        return item.updated

class AtomDiscussionResponder(XMLResponder):
    def render(self, object_list):
        """
        Serializes the first Discussion object in object_list into an Atom feed.
        """
        obj = object_list[0]
        f = feedgenerator.Atom1Feed(
            title=obj.subject,
            link='',
            description='',
            subtitle='Discussion about: ' + obj.subject,
            feed_url='http://localhost:8000/api/discussion/' + str(obj.id),
            id='http://localhost:8000/api/discussion/' + str(obj.id),
            guid='http://localhost:8000/api/discussion/' + str(obj.id),
            author_name=obj.posts[0].author.name,
            author_email=obj.posts[0].author.email,
            author_link=obj.posts[0].author.homepage,
        )
        for p in obj.posts:
            f.add_item(
                title=p.subject,
                link='http://localhost:8000/api/posts/' + str(p.id),
                description=p.display_body,
                author_email=p.author.email,
                author_name=p.author.name,
                author_link=p.author.homepage,
                pubdate=p.created
            )
        response = f.writeString("UTF-8")
        #obj = object_list[0]
        #atom = AtomFeed(atom_id, obj.subject, obj.updated, obj.posts[0].icon.name, '', '', '', obj.posts[0].author.name)
        #for p in object_list.posts:
        #    atom.add_item(atom_id, p.subject, p.updated, p.display_body, '', '', '', '', p.author.name)
        #response = atom.get_feed()
        return response

class DiscussionFeed(Collection):
    def get_entry(self, did):
        d = Discussion.objects.get(id=int(did))
        posts = d.posts
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
        for p in Post.objects.filter(discussion=self.model):
            p.delete()
        self.model.delete()
        return HttpResponse(_("Object successfully deleted."), self.collection.responder.mimetype)
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
    url(r'^api/discussion/(.+?)/?$', xml_discussion_feed),
    url(r'^api/posts/(.*?)/?$', xml_post_collection),
    url(r'^api/profiles/(.*?)/?$', xml_profile_resource),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # django-openid
)

