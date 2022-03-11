from django_summernote.admin import SummernoteModelAdmin
from product.models import Description_Middle
from django.contrib import admin

# Register your models here.
class Description_MiddleAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
admin.site.register(Description_Middle,Description_MiddleAdmin)