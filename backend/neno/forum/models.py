from django.db import models
from django.db.models import permalink
from django.core.urlresolvers import reverse

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    homepage = models.URLField(max_length=255, verify_exists=True)
    avatar = models.ImageField(upload_to='avatar')
    title = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    openid = models.CharField(max_length=255)
    signature = models.CharField(max_length=1024)
    registration_ip = models.IPAddressField()
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    last_online = models.DateTimeField('date last online')

    @models.permalink
    def get_absolute_url(self):
        return ('profile', [str(self.id)])

    def get_atom(self):
        atom = dict(
            title = self.name,
            description = self.signature,
            link = self.get_absolute_url(),
            author_name = self.name,
            author_email = self.email,
            author_link = self.homepage,
            pubdate = self.created,
        )
        return atom
    atom = property(get_atom)

    def __unicode__(self):
        return self.name + "(" + self.email + ")"

class Icon(models.Model):
    image = models.ImageField(upload_to='icon')
    name = models.CharField(max_length=50)
    updated = models.DateTimeField('date updated')
    created = models.DateTimeField('date created')

    def image_html(self):
        if not self.image:
            return '<img src="" alt="" />'
        return u'<img src="%s" alt="%s" width="%d" height="%d" />' % \
                ((self.image.url), (self.name), (self.image.width), (self.image.height))
    image_html.short_description = 'Icon'
    image_html.allow_tags = True

    def __unicode__(self):
        return self.name

class Post(models.Model):
    discussion = models.ForeignKey('Discussion', blank=False)
    author = models.ForeignKey(Profile, blank=False)
    subject = models.CharField(max_length=255, blank=False)
    icon = models.ForeignKey(Icon)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    #parent = models.ForeignKey('self', blank=True)
    hits = models.IntegerField()
    original_body = models.TextField()
    display_body = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('post', [str(self.id)])

    def get_url(self):
        return 'api/post/' + str(self.id)

    def get_atom(self):
        atom = dict(
            title = self.subject,
            description = self.display_body,
            link = self.get_absolute_url(),
            author_name = self.author.name,
            author_email = self.author.email,
            author_link = self.author.homepage,
            pubdate = self.created,
        )
        return atom
    atom = property(get_atom)

    def __unicode__(self):
        return self.subject

class Discussion(models.Model):
    subject = models.CharField(max_length=255, blank=False)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    slug = models.SlugField(max_length=255)
    main_post = models.ForeignKey('Post', related_name='main_post', blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('discussion', [str(self.id)])

    def get_url(self):
        return 'discussion/' + str(id)
    url = property(get_url)

    def get_author(self):
        if self.main_post:
            return self.main_post.author
        return Author()
    author = property(get_author)

    def get_atom(self):
        atom = dict(
            title = self.subject,
            description = self.slug,
            link = self.get_absolute_url(),
            author_name = self.author.name,
            author_email = self.author.email,
            author_link = self.author.homepage,
            pubdate = self.created,
        )
        return atom
    atom = property(get_atom)

    def __unicode__(self):
        return self.subject

class Emote(models.Model):
    image = models.ImageField(upload_to='emote')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    updated = models.DateTimeField('date updated')
    created = models.DateTimeField('date created')

    def image_html(self):
        if not self.image:
            return '<img src="" alt="" />'
        return u'<img src="%s" alt="%s" width="%d" height="%d" />' % \
                ((self.image.url), (self.name), (self.image.width), (self.image.height))
    image_html.short_description = 'Icon'
    image_html.allow_tags = True

    def __unicode__(self):
        return self.name

