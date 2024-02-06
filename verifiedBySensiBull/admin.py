from django.contrib import admin
from .models import verifiedUser
from django.utils.html import format_html
# Register your models here.
class verifiedUsersSensiBull(admin.ModelAdmin):
    list_display = (
        "name",
        "x_username",
        "totalPL",
        "ROI",
        "total_capital",
        "date",
        "verification_url"
    )
    search_fields =[
        "verification_url",
        "name",
        "x_username"
    ]
    ordering = ('-date',)
    def verification__url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.verification_url)
admin.site.register(verifiedUser, verifiedUsersSensiBull)