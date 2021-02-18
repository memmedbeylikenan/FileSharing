from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import indexes

from django.db.models.indexes import Index
# Create your models here.
Permission_field = (
    ("show", "show"),
    ("comment", "comment"),
    
)

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file_field = models.FileField(upload_to='uploads/')
    desc = models.TextField()
    created_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if self.created_date:
            self.end_date = self.created_date + datetime.timedelta(days=7)

        super(Post,self).save(*args,**kwargs)
    
    class Meta:
        indexes = [
            models.Index(fields=['user','title'])
        ]


class Comment(models.Model):
    post_comment = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments', blank=True, null=True)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_comment','post_comment'])
        ]


class Permission(models.Model):
    userpermission = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    permission_field = models.CharField(max_length=50, choices=Permission_field)
    
    def __str__(self):
        return 'post_title - %s, userpermission-%s' %(self.post.title, self.userpermission.username)
    