from django.contrib import admin
from .models import UserProfile,Product,Cart,Order

class OrderAdmin(admin.ModelAdmin):
	list_display=["order_product","order_price","order_payment_status","order_cart","order_txn_id","order_description"]

class cart(admin.TabularInline):
	model = Cart
	extra = 2

class user_cart(admin.ModelAdmin):
	inlines = [cart,]

admin.site.register(Product)
admin.site.register(UserProfile,user_cart)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)