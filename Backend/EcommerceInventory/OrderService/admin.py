from django.contrib import admin

# Register your models here.
from .models import PurchaseOrder, PurchaseOrderItems, PurchaseOrderInwardedLog, PurchaseOrderItemInwardedLog, PurchaseOrderLogs, SalesOrder, SalesOrderItemOutwardedLog, SalesOrderOrderItems

admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItems)
admin.site.register(PurchaseOrderInwardedLog)
admin.site.register(PurchaseOrderItemInwardedLog)
admin.site.register(PurchaseOrderLogs)
admin.site.register(SalesOrder)
admin.site.register(SalesOrderItemOutwardedLog)
admin.site.register(SalesOrderOrderItems)
