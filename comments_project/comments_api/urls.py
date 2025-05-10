from django.urls import path
from .views import CommentListCreateView, CommentRepliesView, get_captcha

urlpatterns = [
    path("captcha/", get_captcha, name="get_captcha"),
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    path('comments/<int:pk>/replies/', CommentRepliesView.as_view(), name='comment-replies'),
]
