from django.contrib import admin
from .models import (
    
    Product,
    SellerProfile,
    ProductVariant,
    ProductImage,
)

admin.site.register(Product)
admin.site.register(SellerProfile)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
