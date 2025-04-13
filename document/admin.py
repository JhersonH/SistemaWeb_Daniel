from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'class_assignment', 'upload_date')
    search_fields = ('title', 'class_assignment__course__name', 'class_assignment__teacher__user__first_name')
    list_filter = ('document_type', 'upload_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_assignment__teacher__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'class_assignment' and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(teacher__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Document, DocumentAdmin)
