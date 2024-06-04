from django.contrib import admin
from posts.models import Post, Comment, PostImage, HashTag
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

# 직접 admin page에서 썸네일 이미지를 보려면
# from django.contrib.admin.widgets import AdminFileWidget
# from django.db import models
# from django.utils.safestring import mark_safe


# class InlineImageWidget(AdminFileWidget):
#     """
#     AdminFileWidget은 관리자 페이지에서 "파일선택" 버튼을 보여주는 부분인데,
#     이 Widget을 커스텀해서 <img> 태그를 추가해준다.
#     """
#     def render(self, name, value, attrs=None, renderer=None):
#         html = super().render(name, value, attrs, renderer)
#         if value and getattr(value, "url", None):
#             html = mark_safe(f'<img src="{value.url}" height="150">') + html
#         return html

# admin page에서 썸네일 이미지를 보는 또다른 방법은, 라이브러리를 사용하는 것이다.
# poetry add django-admin-thumbnails
import admin_thumbnails


class CommentInline(admin.TabularInline):
    """
    Post에서 Foreign key로 연결된 comment를 보기 위해
    admin.TabularInline를 사용하고, 이 클래스를 Post에서 사용해주면 된다.
    """
    model = Comment
    extra = 1


@admin_thumbnails.thumbnail("photo")
class PostImageInline(admin.TabularInline):
    """
    ImageField를 표시할 때, AdminFileWidget을 Override한 InlineImageWidget을 사용한다.
    """
    model = PostImage
    extra = 1

    # formfield_overrides = {
    #     models.ImageField: {
    #         "widget": InlineImageWidget,
    #     }
    # }


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
    ]

    inlines = [
        CommentInline,
        PostImageInline,
    ]

    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "content",
    ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "photo",
    ]

@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass
