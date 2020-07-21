from django.contrib import admin

from .models import Place, PlaceReview, PlaceLike, ReviewComment, Tag, KPopContent, KPopCategory, CelebrityCategory, \
    Celebrity


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'release_date')
    list_display_links = ('name', 'content')
    readonly_fields = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceReview)
class PlaceReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceLike)
class PlaceLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewComment)
class PlaceCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    pass


@admin.register(CelebrityCategory)
class CelebrityCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(KPopCategory)
class KPopCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(KPopContent)
class KPopContentAdmin(admin.ModelAdmin):
    pass
