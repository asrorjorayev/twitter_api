from django.db import models
from users.models import User,BaseModel

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_user',db_index=True)
    content=models.ImageField(upload_to='media/')
    discription=models.TextField(max_length=255,null=True,blank=True)

    creted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post {self.user.username} "

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment_post',db_index=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_user')
    comment_text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user.username} comment {self.comment_text}"
    

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like_post',db_index=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='like_user')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" liked by {self.user.username}"
    
