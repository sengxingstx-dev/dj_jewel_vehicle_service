from django.contrib import admin

from .models import Customer, RentalAgent, Category, Car, Rental, Payment


class RentalAgentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'email',
        'phone',
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'email',
        'phone',
        'address',
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category_name',
        'created_at',
        'updated_at',
    )
    search_fields = ('category_name',)


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'model',
        'make',
        'price',
        'get_category_name',
        'available',
    )
    search_fields = ('model', 'make', 'available')

    def get_category_name(self, obj):
        return obj.category.category_name

    get_category_name.short_description = 'Category Name'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(RentalAgent, RentalAgentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Rental)
admin.site.register(Payment)
