from django.contrib import admin
from .models import Restaurant, Dish

# Register your models here.

# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location')
#     search_fields = ('name', 'location', 'menu')

admin.site.register(Restaurant)
admin.site.register(Dish)
