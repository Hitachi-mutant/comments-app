from django.shortcuts import render

from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.decorators import api_view
from rest_framework.response import Response

# List and Create Comments
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer

# Replies for a specific comment
class CommentRepliesView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        parent_id = self.kwargs['pk']
        return Comment.objects.filter(parent_id=parent_id).order_by('created_at')

@api_view(["GET"])
def get_captcha(request):
    new_captcha = CaptchaStore.generate_key()
    captcha = CaptchaStore.objects.get(hashkey=new_captcha)
    image_url = captcha_image_url(captcha.hashkey)
    return Response({
        "key": captcha.hashkey,
        "image_url": request.build_absolute_uri(image_url)
    })

# send comment via Channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment

class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            data = CommentSerializer(comment).data

            # Broadcast to WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "comments",
                {
                    "type": "new_comment",
                    "comment": data,
                }
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
