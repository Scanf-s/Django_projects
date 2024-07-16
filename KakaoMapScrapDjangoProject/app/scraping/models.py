from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100, null=False, verbose_name="식당 이름")
    restaurant_address = models.CharField(max_length=100, null=True, verbose_name="식당 주소")
    review_count = models.PositiveIntegerField(verbose_name="리뷰 개수")
    category = models.CharField(max_length=100, verbose_name="카테고리")
    star_rate = models.DecimalField(max_digits=3, decimal_places=2, null=True, verbose_name="별점")
    thumbnail_image = models.URLField(max_length=500, null=True, verbose_name="썸네일")
    current_state = models.CharField(max_length=100, null=True, verbose_name="영업 상태")
    phone_number = models.CharField(max_length=15, null=True, verbose_name="전화번호")

    def __str__(self):
        return self.restaurant_name

    class Meta:
        db_table = "restaurant"
