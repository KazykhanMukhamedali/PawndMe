from django.contrib import admin
from .models import Animal, AnimalPhoto, Favorite


class AnimalPhotoInline(admin.TabularInline):
    model = AnimalPhoto
    extra = 0


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'age', 'size', 'location', 'status', 'shelter')
    list_filter = ('type', 'size', 'status')
    search_fields = ('name',)
    inlines = [AnimalPhotoInline]


admin.site.register(Favorite)