from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Message
from .serializers import MessageListSerializer, MessageDetailSerializer, MessageCreateSerializer

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
def create_message(request):
    if request.method == 'POST':
        # Automatically add the sender to the request data
        request.data['sender'] = request.user.id
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def all_messages(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # If the user is a superuser, return all messages
        messages = Message.objects.all()
    else:
        # If the user is not a superuser, retrieve messages where the sender or receiver is the current user
        messages = Message.objects.filter(receiver=request.user) | Message.objects.filter(sender=request.user)

    serializer = MessageListSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def unread_messages(request):
    # Retrieve all unread messages for the current user
    unread_messages = Message.objects.filter(receiver=request.user, unread=True)
    serializer = MessageListSerializer(unread_messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def message_details(request, pk):
    # Retrieve details of a specific message for the current user
    message = get_object_or_404(Message, pk=pk)
    
    if request.user.is_superuser or message.receiver == request.user:
        # Check if the request user is the receiver of the message
        if request.user == message.receiver:
            # Update the status of the message to "read"
            message.unread = False
            message.save()
    else:
        return Response({"details": f"no permissions to {request.user} for this message"}, status=status.HTTP_401_UNAUTHORIZED)
 
    # Serialize the message details along with the receiver's username
    serializer = MessageDetailSerializer(instance=message)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def delete_message(request, pk):
    # Delete a specific message for the current user
    if not request.user.is_superuser:
        message = get_object_or_404(Message, pk=pk, receiver=request.user)
    else:
        message = get_object_or_404(Message, pk=pk)
    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
