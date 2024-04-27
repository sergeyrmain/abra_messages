from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import RegistrationForm
from .models import Message
from .serializer import MessageSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list(request):
    if request.method == 'GET':
        # Optionally filter for unread messages only
        unread_only = request.query_params.get('unread', None) == 'true'
        if unread_only:
            messages = Message.objects.filter(receiver=request.user, is_read=False)
        else:
            messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Set the sender to the current user automatically
        request.data['sender'] = request.user.id
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_detail(request, pk):
    # Get the message, ensure user is sender or receiver
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'GET':
        # Mark the message as read if the receiver is reading it
        if message.receiver == request.user:
            message.is_read = True
            message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        # Allow deletion only if the user is the sender or the receiver
        if message.sender == request.user or message.receiver == request.user:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_message_list(request):
    # Filter for unread messages for the authenticated user
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False)
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)
