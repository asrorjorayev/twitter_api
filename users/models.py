from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add='now')
    updated_add=models.DateTimeField(auto_now='now')



class User(AbstractUser):
    phone_number=models.CharField(max_length=13,unique=True,null=True,blank=True),
    image=models.ImageField(upload_to='image/',null=True,blank=True,validators=[
        FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])
    ])


    def __str__(self):
        return self.username
    
class Followers(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')
    is_accepted=models.BooleanField(default=False)

    def __str__(self):
        return self.from_user.username

    