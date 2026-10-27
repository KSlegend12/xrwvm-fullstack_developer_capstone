from django.contrib import admin
from .models import CarMake, CarModel, Dealership, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name', 'type')
    list_filter = ('type', 'year', 'car_make')


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarModelInline]


class DealershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'city', 'state', 'st', 'zip')
    search_fields = ('full_name', 'city', 'state', 'st')
    list_filter = ('state', 'st')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dealership', 'car_make', 'car_model', 'car_year', 'sentiment', 'purchase')
    search_fields = ('name', 'review', 'car_make', 'car_model')
    list_filter = ('sentiment', 'purchase', 'dealership')


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Dealership, DealershipAdmin)
admin.site.register(Review, ReviewAdmin)
