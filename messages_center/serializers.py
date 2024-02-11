from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = ['sender', 'receiver', 'subject', 'content']
    
    def get_sender(self, obj):
        return obj.sender.username

    def get_receiver(self, obj):
        return obj.receiver.username

        
class MessageListSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    
    class Meta(object):
        model = Message
        fields = ['id' ,'sender', 'receiver', 'creation_date', 'subject', 'unread']
    
    def get_sender(self, obj):
        return obj.sender.username

    def get_receiver(self, obj):
        return obj.receiver.username

        
class MessageDetailSerializer(serializers.ModelSerializer):
    
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'creation_date', 'subject', 'content', 'unread']

    def get_sender(self, obj):
        return obj.sender.username

    def get_receiver(self, obj):
        return obj.receiver.username
    
class MessageCreateSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField()
    sender_username = serializers.SerializerMethodField(read_only=True)  # Added field for sender's username

    class Meta:
        model = Message
        fields = ['sender', 'sender_username', 'receiver', 'subject', 'content']

    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None

    def create(self, validated_data):
        receiver_username = validated_data.pop('receiver')
        receiver = User.objects.get(username=receiver_username)
        validated_data['receiver'] = receiver
        message = Message.objects.create(**validated_data)
        return message
