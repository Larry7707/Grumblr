from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.html import escape

# Create your models here.

class Post(models.Model):
    content = models.CharField(max_length=42)
    user = models.ForeignKey(User, default=None)
    date = models.DateTimeField()
    show_comment = models.BooleanField(default = False)
    last_changed = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        ans = 'id: %d, content: %s, user: %s' % (self.id, self.content, 
                                                    self.user.username)
        return ans

    def get_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_tag_id(self):
        return "post_%d" % self.id

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(last_changed__gt=time).distinct(\
                                    ).order_by('date')

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_posts(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(deleted=False,
                                   last_changed__gt=time).distinct(\
                                   ).order_by('-date')

    # Generates the HTML-representation of a single to-do list post.
    @property
    def html(self):
        # html ="<li id='post_%d'> <button class='delete-btn'>x</button> %s</li>"\
        #  % (self.id, escape(self.content))
        return self.__html

    @html.setter
    def html(self, content):
        self.__html = content
        # return self.html

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('last_changed'))\
        ['last_changed__max'] or "1970-01-01T00:00+00:00"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=420, default = "")
    age = models.IntegerField(default = 0)
    confirmed = models.BooleanField(default = False)
    following = models.ManyToManyField('Profile', related_name = "followed",
                                        symmetrical=False)
    image = models.ImageField(max_length=500,
                              upload_to = 'profile', 
                              default = 'profile/default.png')
    def __unicode__(self):
        ans ="user: %s\n age: %d \n bio: %s" % (self.user, self.age, self.bio)
        return ans

    def get_user(self):
        return self.user

class Comment(models.Model):
    """docstring for Comment"""
    profile = models.ForeignKey(Profile, default=None)
    post = models.ForeignKey(Post, default=None)
    time = models.DateTimeField()
    content = models.CharField(max_length=420)
    last_changed = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Comment.objects.filter(last_changed__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_comments(post, filter_time="1970-01-01T00:00+00:00"):
        return Comment.objects.filter(deleted=False,
                                   last_changed__gt=filter_time,
                                    post=post).distinct().order_by("time")
    @staticmethod
    def get_max_time():
        return Comment.objects.all().aggregate(Max('last_changed'))\
        ['last_changed__max'] or "1970-01-01T00:00+00:00"

    def get_tag_id(self):
        return "comment_%d" % self.id

    def get_name(self):
        name = "%s %s" % (self.profile.user.first_name, 
                        self.profile.user.last_name)
        return name
   
        

