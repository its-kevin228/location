from django.contrib import admin
from .models import Category, PropertyType, Equipment, Property, PropertyPhoto, Sale


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'owner', 'listing_type', 'status', 'rent_price', 'sale_price', 'is_active')
    list_filter = ('listing_type', 'status', 'is_active', 'property_type__category')
    search_fields = ('title', 'address', 'city', 'owner__username')
    filter_horizontal = ('equipments',)
    inlines = [PropertyPhotoInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer_name', 'sale_price', 'sale_date', 'status')
    list_filter = ('status',)
    search_fields = ('buyer_name', 'buyer_email', 'property__title')
    readonly_fields = ('created_at',)
