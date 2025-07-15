from django.contrib import admin

# Register your models here.
from .models import Inventory, InventoryLog, Warehouse, RackAndShelvesAndFloor

admin.site.register(Warehouse)
admin.site.register(RackAndShelvesAndFloor)
admin.site.register(Inventory)
admin.site.register(InventoryLog)