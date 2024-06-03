from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignupForm
from users.models import User
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/posts/feeds/")

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
                return redirect("/posts/feeds/")
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
    return redirect("/users/login/")


def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save() # 자동으로 users/form의 signup class의 save()함수가 호출된다.
            login(request, user)
            return redirect("/posts/feeds/")
    else:  # GET method
        form = SignupForm()

    """
    GET 또는 form 에러 발생 시 signup.html을 렌더링해준다.
    이때, POST에서 에러가 발생하면 signup.html에는 에러메세지가 포함되고,
    GET 요청만 되면 그냥 signup.html이 보이게 된다.
    """
    context = {"form": form}
    return render(request, "users/signup.html", context=context)