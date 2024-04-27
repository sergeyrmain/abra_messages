from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Message

class MessageAPITests(APITestCase):
    def setUp(self):
        # Set up users
        self.user1 = User.objects.create_user(username='user1', password='user1password')
        self.user2 = User.objects.create_user(username='user2', password='user2password')

        # Set up messages
        self.message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject="Hi There",
            message="Hello, how are you doing?",
            is_read=False
        )
        self.message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            subject="Re: Hi There",
            message="I'm good, thanks for asking!",
            is_read=True  # One message read for diversity
        )

        # Initialize the APIClient
        self.client = APIClient()

    def test_get_all_messages(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one message received by user2

    def test_get_unread_messages_only(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('message_list') + '?unread=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(msg['is_read'] == False for msg in response.data))  # Check all messages are unread

    def test_write_message(self):
        self.client.force_authenticate(user=self.user1)
        data = {'receiver': self.user2.id, 'subject': 'Test Message', 'message': 'This is a test message.'}
        response = self.client.post(reverse('message_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sender'], self.user1.id)

    def test_read_specific_message(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('message_detail', args=[self.message1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message1.refresh_from_db()
        self.assertTrue(self.message1.is_read)

    def test_delete_message(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('message_detail', args=[self.message1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(id=self.message1.id).exists())

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
