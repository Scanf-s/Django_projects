from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자명 (3자리 이상)"}
        ),
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 (4자리 이상)"}
        ),
    )


class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput)  # 비밀번호 입력 시 ****로 표시

    profile_image = forms.ImageField()
    short_description = forms.CharField()

    # https://docs.djangoproject.com/en/dev/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_username(self):
        """
        username에 대한 유효성 검사를 해주는 메서드
        clean_{필드명}처럼 검증 메서드를 추가해주면, views에서 따로 검증을 하지 않아도 된다.
        (장고가 알아서 해줌)
        :return:
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken")
        return username

    def clean(self):
        """
        password랑 check_password가 동일한지 검증하는 메서드
        두개의 필드명에 대해서 검증하려면 clean 메서드를 추가해준다.
        (마찬가지로 장고가 알아서 검증해줌)
        :return:
        """
        password = self.cleaned_data.get("password")
        check_password = self.cleaned_data.get("check_password")
        if password != check_password:
            self.add_error("check_password", "passwords are not same")  # forms.add_error랑 같은 역할

        # clean method는 마지막에 값을 리턴하지 않아도 된다.

    def save(self):  # 회원가입 기능
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        profile_image = self.cleaned_data.get("profile_image")
        short_description = self.cleaned_data.get("short_description")
        user = User.objects.create_user(
            username=username,
            password=password,
            profile_image=profile_image,
            short_description=short_description
        )
        return user
