from django.db import models
from django.contrib.auth.models import User

# Create Thread
class ForumThread(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    description=models.TextField()
    tags=models.CharField(max_length=200,default=None)
    views=models.CharField(max_length=100,default=0)
    add_time=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
    
    def tag_as_list(self):
        return self.tags.split(',')

# Thread Replies
class ThreadReply(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    thread_id=models.ForeignKey(ForumThread,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    description=models.TextField()
    reply_time=models.DateTimeField(auto_now_add=True,null=True)

    def get_signature(self):
        return Setting.objects.filter(user_id=self.user_id).first()

# Save Setting
class Setting(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    signature=models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.signature


