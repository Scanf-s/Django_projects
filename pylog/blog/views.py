from django.shortcuts import render, redirect
from blog.models import Post, Comment


def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "post_list.html", context=context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method=="POST":
        new_comment = request.POST["comment"]
        Comment.objects.create(
            post=post,
            content=new_comment
        )
    context = {
        "post": post
    }
    return render(request, "post_detail.html", context=context)


def post_add(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        thumbnail = request.FILES.get("thumbnail")

        new_post = Post.objects.create(
            title=title,
            content=content,
            thumbnail=thumbnail
        )
        return redirect(f"/posts/{new_post.id}")

    return render(request, "post_add.html")
