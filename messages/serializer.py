from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'subject', 'message', 'creation_date', 'is_read']
        read_only_fields = ['sender']

    def create(self, validated_data):
        # Set sender to the current user from the request context
        validated_data['sender'] = self.context['request'].user
        return super(MessageSerializer, self).create(validated_data)
