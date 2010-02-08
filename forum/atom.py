from neno.forum.models import Discussion, Post, Profile
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import XMLResponder
from django.utils import feedgenerator
from django.utils.feedgenerator import Atom1Feed

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
        TODO: Refactor and reuse code from AtomResponder.
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

"""
A Discussion needs special handling, since it also contains Posts.
"""
class DiscussionFeed(Collection):
    def __init__(self, **options):
        super(DiscussionFeed, self).__init__(
            queryset = Discussion.objects.all(),
            permitted_methods = ('GET', 'PUT', 'POST', 'DELETE'),
            responder = AtomDiscussionResponder(paginate_by = 10),
            **options
        )

    def get_entry(self, did, *args, **kwargs):
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
        return request
        # ...

    def update(self, request, *args, **kwargs):
        """
        Update the main information about a Discussion.
        TODO: Not created.
        """
        return HttpResponse(request, self.collection.responder.mimetype)
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

