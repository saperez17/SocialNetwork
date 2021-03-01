from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os 
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat(timespec='hours')
        return ''

class User(AbstractUser):
    username = models.CharField(max_length=24, unique=True)
    # password = models.CharField(verbose_name=_("Password"), max_length=32, wid)
    display_name = models.CharField(max_length=30, verbose_name=_("Display name"), help_text=_("Will be shown .."), blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    address1 = models.CharField(verbose_name=_("Address 1"), max_length=1024, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=1023, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
    mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="images", default=os.path.join(settings.MEDIA_ROOT, "images","profile_default_image.png"))

    class Meta:
        ordering = ['last_name']
    def __str__ (self):
        return f"{self.username}"

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"Following: {self.following.username}, Follower: {self.follower.username}"


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets", blank=False)
    username = models.CharField(max_length=24, blank=True, null=True )
    content = models.CharField(max_length=250, blank=True)
    updated = models.DateTimeField(auto_now=True)
    datetime = models.DateTimeField(default=datetime.now, blank=True)  #By passing in the function without parenthesis we telling the model to run this every time a new model is created
    likes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return f"user: {self.username}, tweet: {self.content}"
    
    def save(self, *args, **kwargs):
        self.username = self.user.username
        self.likes = len(self.likes_tweet.all())
        super(Tweet, self).save(*args, **kwargs)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_users", blank=False, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes_tweet", blank=True)
    id_liked_tweet = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"user: {self.user} liked post: {self.tweet.content}"
    def save(self, *args, **kwargs):
        self.id_liked_tweet = self.tweet.pk
        super(Like, self).save(*args, **kwargs)