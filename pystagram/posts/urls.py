from django.urls import path
from posts.views import feeds, comment_add, comment_delete, post_add, hashtags

app_name = "posts"
urlpatterns = [
    path("feeds/", feeds, name="feeds"),
    path("comment_add/", comment_add, name="comment_add"),
    path("comment_delete/<int:comment_id>", comment_delete, name="comment_delete"),
    path("post_add/", post_add, name="post_add"),
    path("hashtags/<str:hashtag_name>/", hashtags, name="hashtags"),
]
