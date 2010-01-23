from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    homepage = models.URLField(max_length=255, verify_exists=True)
    #avatar = models.ImageField(upload_to='avatar')
    title = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    openid = models.CharField(max_length=255)
    signature = models.CharField(max_length=1024)
    registration_ip = models.IPAddressField(editable=False)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    last_online = models.DateTimeField('date last online')

    def __unicode__(self):
        return self.name + "(" + self.email + ")"

class Icon(models.Model):
    #image = models.ImageField(upload_to='icon')
    name = models.CharField(max_length=50)
    updated = models.DateTimeField('date updated')
    created = models.DateTimeField('date created')

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
    hits = models.IntegerField(editable=False)
    original_body = models.TextField(editable=False)
    display_body = models.TextField()

    def __unicode__(self):
        return self.subject

class Discussion(models.Model):
    subject = models.CharField(max_length=255, blank=False)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.subject

class Emote(models.Model):
    #image = models.ImageField(upload_to='emote')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    updated = models.DateTimeField('date updated')
    created = models.DateTimeField('date created')

    def __unicode__(self):
        return self.name

