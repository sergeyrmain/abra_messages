from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializer import MessageSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list(request):
    if request.method == 'GET':
        # cases for only unread messages or all messages
        unread_only = request.query_params.get('unread', 'false').lower() == 'true'
        if unread_only:
            messages = Message.objects.filter(receiver=request.user, is_read=False)
        else:
            messages = Message.objects.filter(receiver=request.user)

        message_serializer = MessageSerializer(messages, many=True)
        return Response(message_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # create new message sender is automatically set to the current user.
        message_serializer = MessageSerializer(data=request.data, context={'request': request})
        if message_serializer.is_valid():
            message_serializer.save()
            return Response(message_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.method == 'GET':
        # mark the message as read if the receiver is the current user.
        if message.receiver == request.user:
            message.is_read = True
            message.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # only the sender or receiver can delete the message.
        if message.sender == request.user or message.receiver == request.user:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Permission denied to delete this message.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Validate username and password.
    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Prevent registration with a duplicate username.
    if User.objects.filter(username=username).exists():
        return Response({'error': 'This username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user_id = user.id
    return Response({'message': f'Registration successful.ID: {user_id}'}, status=status.HTTP_201_CREATED)
