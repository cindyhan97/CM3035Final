from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return "{0}/{1}/{2}".format(instance.user.id, "avatar", filename)


def user_post_path(instance, filename):
    return "{0}/{1}/{2}".format(instance.poster.nickname, "posts", filename)

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=256, null=True, blank=True)
    photo = models.FileField(null = True, blank = True, upload_to=user_directory_path)
    chat_code = models.CharField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return self.user.username

class friends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user")
    friend= models.ManyToManyField(User, blank=True, related_name="friends")


class publicChat(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="publicChat_user", unique= False)
    comment = models.TextField(max_length=800, null = True, blank = True)


class userPost(models.Model):
    poster = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="poster",unique= False)
    text = models.TextField(max_length=800, null = True, blank = True)
    mediaFile1 = models.FileField(null = True, blank = True, upload_to=user_post_path)
    mediaFile2 = models.FileField(null = True, blank = True, upload_to=user_post_path)
    mediaFile3 = models.FileField(null = True, blank = True, upload_to=user_post_path)
    posttime = models.TimeField(auto_now=True)

class friendReq(models.Model):
    FromUser = models.ForeignKey(User,on_delete=models.CASCADE, related_name='FromUser', db_constraint=False)
    ToUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ToUser',db_constraint=False)

