from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from .models import (
    Section, CategoryNews, News, Subscriber, Service,
    # гостиница
    RoomCategory, RoomAmenity, Room, RoomBooking
)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CategoryNews)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'get_photo', 'time_create', 'time_update', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50' style='border-radius:6px;'/>")
        return "—"
    get_photo.short_description = 'Фото'


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    # ✅ исправлено: get_photo был, но не выводился
    list_display = ('id', 'title', 'get_photo', 'time_create', 'time_update', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50' style='border-radius:6px;'/>")
        return "—"
    get_photo.short_description = 'Фото'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'subscribed_at')
    list_display_links = ('id', 'email')
    search_fields = ('email',)
    list_filter = ('is_active', 'subscribed_at')


# ============================================================
# ГОСТИНИЦА / НОМЕРА
# ============================================================

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'default_capacity', 'is_published', 'order')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_published', 'order')
    list_filter = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'icon', 'is_published', 'order')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'icon')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'number', 'title', 'category',
        'get_photo', 'capacity', 'floor',
        'price', 'currency', 'status', 'is_published', 'time_update'
    )
    list_display_links = ('id', 'number', 'title')
    search_fields = ('number', 'title', 'content')
    list_filter = ('is_published', 'status', 'category', 'currency')
    list_editable = ('is_published', 'status', 'price')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('amenities',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50' style='border-radius:6px;'/>")
        return "—"
    get_photo.short_description = 'Фото'


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'room', 'guest_name', 'guest_phone',
        'date_from', 'date_to', 'status',
        'total_price', 'currency', 'created_at'
    )
    list_display_links = ('id', 'room', 'guest_name')
    search_fields = ('guest_name', 'guest_phone', 'guest_email', 'room__number', 'room__title')
    list_filter = ('status', 'currency', 'created_at', 'date_from', 'date_to')
    list_editable = ('status',)
    date_hierarchy = 'created_at'


# Настройки интерфейса админки
admin.site.site_title = 'Администрирование сайта'
admin.site.site_header = 'Администрирование сайта'
