from django.shortcuts import render, redirect, reverse
from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, "posts/feeds.html", context=context)

@require_POST
def comment_add(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # db에 반영하지 않고, 메모리에만 생성
        comment = form.save(commit=False)

        # comment를 생성한 사용자 = 요청을 보낸 사용자
        comment.user = request.user

        comment.save()

        print(comment.id)
        print(comment.content)
        print(comment.user)

        # 생성한 comment에서 연결된 post 정보를 가져와서 id값에 해당하는 링크로 redirect
        # HTTPResponseRedirect 함수는 Appname:URLname 형태로 사용할 수 없는데, reverse 함수를 사용해서
        # Appname:URLname을 실제 URL로 변경해서 넣어주어야 한다.
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)


@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("You are not allowed to delete this comment.")


def post_add(request):
    if request.method=="POST":
        # post 요청 시 content 데이터는 PostForm으로 처리해주고,
        # image 데이터는 PostImageForm으로 처리해줘야함
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            # post의 user를 요청한 user로 생성
            post.user = request.user
            post.save()

            # post_add의 input multiple attribute로 인해, request.FILES대신, request.FILES.getlist("images")로 받아야한다.
            # getlist로 받아오면 여러개의 이미지 파일이 list형태로 전달된다.
            for image_file in request.FILES.getlist("images"):
                # PostImage 모델에 이미지 전달
                # for loop을 돌면서, 동일한 post에 대해 이미지를 계속 전달해준다.
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            # hashtags로 전달된 문자열을 쉼표로 분리해서 hashtag 생성
            hashtag_string = request.POST.get("hashtags")
            if hashtag_string:
                hashtag_names = [hashtag_name.strip() for hashtag_name in hashtag_string.split(",")]
                for hashtag_name in hashtag_names:
                    hashtag, _ = HashTag.objects.get_or_create(name=hashtag_name)
                    # get_or_create함수는 반환값으로 2개의 아이템이 담긴 tuple이 반환되는데,
                    # 첫번째 요소는 DB에서 가져오거나 새로 만든 Hashtag 객체이고,
                    # 두번째 요소는 생성 여부에 대한 flag이다.
                    # 이때, 두번째 요소는 굳이 필요하지 않으므로 '_'로 받아준다.
                    post.hashtags.add(hashtag)

            # post의 id값에 해당하는 링크로 redirect
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    else: # Get request시에는 빈 PostForm을 보여준다.
        form = PostForm()

    context = {"form": form}
    return render(request, "posts/post_add.html", context=context)


def hashtags(request, hashtag_name):
    try:
        hashtag = HashTag.objects.get(name=hashtag_name)
    except ObjectDoesNotExist: # Hashtag에 해당하는 포스트를 찾을 수 없는 경우
        hashtag = "invalid_hashtag"
        posts = Post.objects.none() # Empty QuerySet return
    else:
        posts = Post.objects.filter(hashtags=hashtag)

    context = {
        "hashtag_name": hashtag,
        "posts": posts,
    }
    return render(request, "posts/hashtags.html", context=context)
