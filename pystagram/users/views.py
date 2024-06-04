from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignupForm
from users.models import User
from posts.models import Post
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")

    if request.method == "POST":
        # LoginForm 인스턴스 생성
        form = LoginForm(data=request.POST)

        # 폼이 유효한지 검증 (반드시 호출해줘야 폼 데이터를 가져올 수 있음)
        print("form.is_valid()", form.is_valid())
        if form.is_valid():
            # 폼에서 데이터를 가져옴
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # username, password에 해당하는 사용자가 존재하는지 검증
            # 사용자 모델로 저장된 username과 password를 통해 검증하게 된다.
            user = authenticate(username=username, password=password)

            if user:
                login(request, user) # 로그인
                # redirect 함수에 /posts/feeds/ URL을 전달해줘도 되고,
                # reverse 함수에 전달하는 인자처럼 APPNAME:URLNAME을 전달해줘도 된다.
                # urls.py를 참고해보자.
                return redirect("posts:feeds")
            else:
                form.add_error(None, "invalid username or password")

        # 로그인을 어떤 이유던지간에 실패한 경우 다시 로그인 페이지 렌더링
        context = {"form" : form}
        return render(request, "users/login.html", context=context)

    else: # GET method
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "users/login.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("users:login")


def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save() # 자동으로 users/form의 signup class의 save()함수가 호출된다.
            login(request, user)
            return redirect("posts:feeds")
    else:  # GET method
        form = SignupForm()

    """
    GET 또는 form 에러 발생 시 signup.html을 렌더링해준다.
    이때, POST에서 에러가 발생하면 signup.html에는 에러메세지가 포함되고,
    GET 요청만 되면 그냥 signup.html이 보이게 된다.
    """
    context = {"form": form}
    return render(request, "users/signup.html", context=context)


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context={"user": user}
    return render(request, "users/profile.html", context=context)


def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/followers.html", context=context)

def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/following.html", context=context)


def follow(request, user_id):
    # 로그인한 유저
    user = request.user

    # 팔로우하려는 유저
    target_user = get_object_or_404(User, id=user_id)

    # 팔로우 하려는 유저가 이미 팔로우 된 상태라면, (Unfollow 기능)
    if target_user in user.following.all():
        # 팔로우 목록에서 제거
        user.following.remove(target_user)
    else: # Follow
        user.following.add(target_user)

    url_next = request.GET.get("next") or reverse("users:profile", args=[user_id])
    return HttpResponseRedirect(url_next)