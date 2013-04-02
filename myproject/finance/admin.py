from django.contrib import admin
from finance.models import *


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'value', 'date']
    date_hierarchy = 'date'
    list_filter = ['category']
    
admin.site.register(MacroCategory)
admin.site.register(MicroCategory)
admin.site.register(Expense, ExpenseAdmin)
