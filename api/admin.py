from django.contrib import admin
from .models import Region, City, Area

class CityInline(admin.TabularInline):
    model = City
    extra = 0
    fields = ('id', 'name')
    readonly_fields = ('id',)

class AreaInline(admin.TabularInline):
    model = Area
    extra = 0
    fields = ('id', 'name')
    readonly_fields = ('id',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ('id',)
    inlines = [CityInline]

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_filter = ('region',)
    search_fields = ('id', 'name', 'region__name')
    ordering = ('id',)
    inlines = [AreaInline]
    list_per_page = 130

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'get_region')
    list_filter = ('city__region', 'city')
    search_fields = ('id', 'name', 'city__name', 'city__region__name')
    ordering = ('id',)
    list_per_page = 130

    def get_region(self, obj):
        return obj.city.region.name
    get_region.short_description = 'Region'
