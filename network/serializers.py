from django.conf import settings 
from rest_framework import serializers
from .models import Tweet, User, Like, Follower

class UserSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['username', 'display_name', 'date_of_birth', 'address1', 'city', 'country', 'email', 'mobile_phone', 'photo', 'follower', 'following']

class TweetSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    datetime = serializers.DateTimeField(format='%b. %d, %Y, %I:%M')
    class Meta:
        model = Tweet
        fields = ['pk','user', 'username', 'content', 'datetime', 'likes']
        ordering = ['datetime']

        def create(self, validated_data):
            return Tweet.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.name = validated_data.get("user", instance.user)
            instance.content = validated_data.get("content", instance.content)
            instance.datetime = validated_data.get("datetime", instance.datetime)
            instance.username = validated_data.get("username", instance.username)
            instance.likes = validated_data.get("likes", instance.likes)
            instance.save()
            return instance

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'tweet']

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['follower', 'following']
    def create(self, validated_data):
            return Follower.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.follower = validated_data.get("follower", instance.follower)
        instance.following = validated_data.get("following", instance.following)
        instance.save()
        return instance