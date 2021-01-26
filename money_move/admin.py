from django.contrib import admin

# Register your models here.

from .models import Income, Spendings, MoneySource, SpendingKind, Cash, CashKind



admin.site.register(MoneySource)
admin.site.register(SpendingKind)
admin.site.register(CashKind)

class IncomeAdmin(admin.ModelAdmin):
	list_display = ('date_field', 'ammount', 'source', 'comment')


admin.site.register(Income, IncomeAdmin)

class SpendingsAdmin(admin.ModelAdmin):
	list_display = ('date_field', 'ammount', 'kind', 'comment')


admin.site.register(Spendings, SpendingsAdmin)

class CashAdmin(admin.ModelAdmin):
	list_display = ('date_field', 'ammount', 'cash_kind', 'comment')


admin.site.register(Cash, CashAdmin)