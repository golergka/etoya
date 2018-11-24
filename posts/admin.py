from django.contrib import admin
from solo.admin import SingletonModelAdmin
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from .models import Post, Block, HighlightBlock, TextBlock, IndexConfiguration


class BlockInline(StackedPolymorphicInline):
    class HighlightBlockInline(StackedPolymorphicInline.Child):
        model = HighlightBlock

    class TextBlockInline(StackedPolymorphicInline.Child):
        model = TextBlock

    model = Block
    child_inlines = (
        HighlightBlockInline,
        TextBlockInline
    )


@admin.register(Post)
class PostAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']})
    ]
    inlines = (BlockInline, )


admin.site.register(IndexConfiguration, SingletonModelAdmin)
