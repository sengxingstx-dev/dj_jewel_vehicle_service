from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
    )  # Fields to display in the list view
    search_fields = ('username',)  # Fields to search for in the admin interface


admin.site.register(Account, AccountAdmin)
