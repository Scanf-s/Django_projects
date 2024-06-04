from django import forms
from posts.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Comment에 넣어줘야 하는 field를 지정해준다.
        # user 정보는 Django가 알아서 처리해주도록 설정하였다.
        fields = [
            "post",
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Add a comment...",
                }
            )
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]