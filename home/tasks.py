from celery import shared_task
from home.models import *
import datetime




@shared_task(name="delete_post")
def delete_post():
    posts = Post.objects.all()
    for post in posts:
        if post.end_date is None:
            continue
        if post.end_date == datetime.date.today() or post.end_date < datetime.date.today():
            post.delete()
        else:
            print('vaxti kecmeyib')
        
    
