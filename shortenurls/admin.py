from django.contrib import admin
from .models import URLShortener
# Register your models here.
class URLShortAdmin(admin.ModelAdmin):
	fields=('created_by', 'url', 'end_date', 'users_visible_to')
admin.site.register(URLShortener, URLShortAdmin)