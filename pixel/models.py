from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Pixel_W(models.Model):
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    z1 = models.CharField(max_length = 22,default='4294967295')
    z2 = models.CharField(max_length = 22,default='4294967295')
    z3 = models.CharField(max_length = 22,default='4294967295')
    u1 = models.CharField(max_length = 25)
    u2 = models.CharField(max_length = 25)
    u3 = models.CharField(max_length = 25)
    lable1 = models.CharField(max_length=255, default='')
    lable2 = models.CharField(max_length=255, default='')
    lable3 = models.CharField(max_length=255, default='')
    update_time1 = models.DateTimeField(auto_now_add=True)
    update_time2 = models.DateTimeField(auto_now_add=True)
    update_time3 = models.DateTimeField(auto_now_add=True)
    del_time1 = models.BigIntegerField(default=300)
    del_time2 = models.BigIntegerField(default=300)
    del_time3 = models.BigIntegerField(default=300)
    update_time = models.DateTimeField(auto_now=True)


class Pixel_C(models.Model):
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    z1 = models.CharField(max_length = 22,default='4294967295')
    z2 = models.CharField(max_length = 22,default='4294967295')
    z3 = models.CharField(max_length = 22,default='4294967295')
    u1 = models.CharField(max_length = 25)
    u2 = models.CharField(max_length = 25)
    u3 = models.CharField(max_length = 25)
    lable1 = models.CharField(max_length=255, default='')
    lable2 = models.CharField(max_length=255, default='')
    lable3 = models.CharField(max_length=255, default='')
    update_time1 = models.DateTimeField(auto_now_add=True)
    update_time2 = models.DateTimeField(auto_now_add=True)
    update_time3 = models.DateTimeField(auto_now_add=True)
    del_time1 = models.BigIntegerField(default=300)
    del_time2 = models.BigIntegerField(default=300)
    del_time3 = models.BigIntegerField(default=300)
    update_time = models.DateTimeField(auto_now=True)


class Pixel_B(models.Model):
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    z1 = models.CharField(max_length = 22,default='4294967295')
    z2 = models.CharField(max_length = 22,default='4294967295')
    z3 = models.CharField(max_length = 22,default='4294967295')
    u1 = models.CharField(max_length = 25)
    u2 = models.CharField(max_length = 25)
    u3 = models.CharField(max_length = 25)
    lable1 = models.CharField(max_length=255, default='')
    lable2 = models.CharField(max_length=255, default='')
    lable3 = models.CharField(max_length=255, default='')
    update_time1 = models.DateTimeField(auto_now_add=True)
    update_time2 = models.DateTimeField(auto_now_add=True)
    update_time3 = models.DateTimeField(auto_now_add=True)
    del_time1 = models.BigIntegerField(default=300)
    del_time2 = models.BigIntegerField(default=300)
    del_time3 = models.BigIntegerField(default=300)
    update_time = models.DateTimeField(auto_now=True)


class Pixel_A(models.Model):
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    z1 = models.CharField(max_length = 22,default='4294967295')
    z2 = models.CharField(max_length = 22,default='4294967295')
    z3 = models.CharField(max_length = 22,default='4294967295')
    u1 = models.CharField(max_length = 25)
    u2 = models.CharField(max_length = 25)
    u3 = models.CharField(max_length = 25)
    lable1 = models.CharField(max_length=255, default='')
    lable2 = models.CharField(max_length=255, default='')
    lable3 = models.CharField(max_length=255, default='')
    update_time1 = models.DateTimeField(auto_now_add=True)
    update_time2 = models.DateTimeField(auto_now_add=True)
    update_time3 = models.DateTimeField(auto_now_add=True)
    del_time1 = models.BigIntegerField(default=300)
    del_time2 = models.BigIntegerField(default=300)
    del_time3 = models.BigIntegerField(default=300)
    update_time = models.DateTimeField(auto_now=True)



class lable(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lable_user')
    pixel_id = models.IntegerField(null=False)
    index_abc = models.CharField(max_length = 22)
    z = models.CharField(max_length = 22,default='4294967295')
    lable_text = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    del_time = models.IntegerField()
    lable_url = models.CharField(max_length=255)

    add_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='lable_add_user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    def get_level(self):
        if self.points < 100:
            return 1
        elif 100 <= self.points < 1000:
            return 2
        else:
            return 3

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'followed')
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    user_level = models.IntegerField(default=1)
    user_experience = models.IntegerField(default=0)
    user_points = models.IntegerField(default=0)
    is_realname_authenticated = models.BooleanField(default=False)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    signature = models.TextField(blank=True)

    # user_level：用户等级，通常是一个整数。
    # user_experience：用户经验，通常是一个整数。
    # user_points：用户积分，通常是一个整数。
    # is_realname_authenticated：是否实名认证的标识，是一个布尔值。
    # id_number：用户身份证号码，使用CharField，可以为空。
    # mobile_number：用户手机号，使用CharField，可以为空。
    # avatar_url：用户头像的URL地址，使用URLField，可以为空。
    # signature：用户签名，使用TextField，可以为空。
    def __str__(self):
        return self.user.username
