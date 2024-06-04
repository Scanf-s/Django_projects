from django.db import models


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="writer",
        on_delete=models.CASCADE,
    )
    content = models.TextField("Content")
    hashtags = models.ManyToManyField("posts.HashTag", verbose_name="hashtag list", blank=True)
    created_at = models.DateTimeField("Created_at", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Post(id:{self.id})"

class PostImage(models.Model):
    post = models.ForeignKey(
        "posts.Post",
        verbose_name="post",
        on_delete=models.CASCADE,
    )
    photo = models.ImageField("Photo", upload_to="post")


class Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="writer",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "posts.Post",
        verbose_name="post",
        on_delete=models.CASCADE,
    )
    content = models.TextField("Content")
    created_at = models.DateTimeField("Created_at", auto_now_add=True)


class HashTag(models.Model):
    name = models.CharField("Tagname", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hashtag"
        verbose_name_plural = "Hashtags"