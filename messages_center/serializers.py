from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = ['sender', 'receiver', 'subject', 'content']
        
class MessageListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = ['sender', 'receiver', 'creation_date', 'subject', 'unred']
        
class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = ['sender', 'receiver', 'creation_date', 'subject', 'content']        