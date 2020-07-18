from django.contrib import admin

from .models import Place, PlaceReview, PlaceLike, ReviewComment, Tag, KPopContent, KPopCategory, CelebrityCategory, \
    Celebrity


# class PostImageInline(admin.TabularInline):
#     model = PostImage
#     extra = 1

#
# class PlaceCommentInline(admin.TabularInline):
#     model = ReviewComment
#     extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'release_date')
    list_display_links = ('name', 'content')
    # inlines = [
    #     PlaceCommentInline,
    # ]
    readonly_fields = ('tags',)


@admin.register(PlaceReview)
class PlaceReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceLike)
class PlaceLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewComment)
class PlaceCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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
