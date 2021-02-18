import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Comment
from django.contrib.auth.models import User

@database_sync_to_async
def save_comment(**data):
    user = data['user']
    text = data['text']
    post = data['post']
    try:
        comment = Comment.objects.create(user_comment=user,post_comment_id=int(post),body=text)
        return comment
        
    except Exception as e:
        print(e)
        return False

        
    
@database_sync_to_async
def get_user(**data):
    return User.objects.get(id=data['id'])










class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id= self.scope['url_route']['kwargs']['id']
        self.group_name = "post_%s" % self.post_id
        user = self.scope['user']
        if user.is_authenticated == False:
            await self.disconnect()
        print(self.channel_name)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
                

        await self.accept()
 

    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(self.group_name,self.channel_name)




    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['text'] != "":
            user =await get_user(id=data['user'])
            text = data['text']
            post = self.post_id
            comment =  await save_comment(user=user,text=text,post=post)
            if comment:
                await self.channel_layer.group_send(self.group_name,
                {
                    'type':'save_comment',
                    'user':user.username,
                    'text':text,
                    'date':str(comment.date.strftime("%d/%m/%Y, %H:%M:%S"))                
                }
                )
            else:
                await self.channel_layer.send(self.channel_name,
                {
                    "type":"error_message",
                    "message":"Xeta bas verdi"

                }
                )
        else:
            await self.channel_layer.send(self.channel_name,
            {
                'type':"error_message",
                'message':'Comment bos ola bilmez'

            }
            )


        
        
        

    async def save_comment(self,event):
        data = {'type':'success','user':event['user'],"text":event['text'],"date":event['date']}
        print(data)
        await self.send(json.dumps(data))




        



    async def error_message(self,event):
        message = event['message']
        await self.send(json.dumps({'type':'error','message':message}))




