from django.contrib import admin
from scraping.models import Restaurant
from django.contrib.admin import SimpleListFilter


class StarRateCustomFilter(SimpleListFilter):
    title = '별점'
    parameter_name = 'star_rate'

    def lookups(self, request, model_admin):
        return (
            ('1', '1점대'),
            ('2', '2점대'),
            ('3', '3점대'),
            ('4', '4점대'),
            ('5', '5점대'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(star_rate__gte=1, star_rate__lt=2)
        elif self.value() == '2':
            return queryset.filter(star_rate__gte=2, star_rate__lt=3)
        elif self.value() == '3':
            return queryset.filter(star_rate__gte=3, star_rate__lt=4)
        elif self.value() == '4':
            return queryset.filter(star_rate__gte=4, star_rate__lt=5)
        elif self.value() == '5':
            return queryset.filter(star_rate=5)
        else:
            return queryset


class ReviewCountCustomFilter(SimpleListFilter):
    title = '리뷰 개수'
    parameter_name = 'review_count'

    def lookups(self, request, model_admin):
        return (
            ('1', '1개 ~ 10개'),
            ('10', '10개 ~ 100개'),
            ('100', '100개 ~ 1000개'),
            ('1000', '1000개이상'),
        )

    def queryset(self, request, queryset):
        if self.value() == '10':
            return queryset.filter(star_rate__gte=1, star_rate__lt=10)
        elif self.value() == '10':
            return queryset.filter(star_rate__gte=10, star_rate__lt=100)
        elif self.value() == '100':
            return queryset.filter(star_rate__gte=100, star_rate__lt=1000)
        elif self.value() == '1000':
            return queryset.filter(review_count__gte=1000)
        else:
            return queryset


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant_name",
        "restaurant_address",
        "review_count",
        "category",
        "star_rate",
        "thumbnail_image",
        "current_state",
        "phone_number",
    )
    ordering = ("-star_rate", "-review_count")
    search_fields = ("restaurant_name", "restaurant_address")
    list_filter = (StarRateCustomFilter, ReviewCountCustomFilter, "current_state", "category")
    list_per_page = 30
