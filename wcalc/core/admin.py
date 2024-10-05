from django.contrib import admin

from core.models import Package, Portals, ProductRow, Responsible

FIELDSETS_FOR_PRODUCTROW = [
    (
        None,
        {
            "fields": ["PORTAL", "PRODUCTROW_ID", "OWNER_ID", "OWNER_TYPE", "PRODUCT_ID", "PRODUCT_NAME",
                       "ORIGINAL_PRODUCT_NAME", "PRODUCT_DESCRIPTION"],
        },
    ),
    (
        'Стоимость, скидки, налоги',
        {
            "fields": ["PRICE", "PRICE_EXCLUSIVE", "PRICE_NETTO", "PRICE_BRUTTO", "PRICE_ACCOUNT", "QUANTITY",
                       "DISCOUNT_TYPE_ID", "DISCOUNT_RATE", "DISCOUNT_SUM", "TAX_RATE", "TAX_INCLUDED", "MEASURE_CODE",
                       "MEASURE_NAME"],
        },
    ),
    (
        'Дополнительные поля',
        {
            "fields": ["CUSTOMIZED", "SORT", "XML_ID", "TYPE"],
        },
    ),
    (
        'Склад',
        {
            "fields": ["STORE_ID", "RESERVE_ID", "DATE_RESERVE_END", "RESERVE_QUANTITY"],
        },
    ),
    (
        'Упаковка',
        {
            "fields": ["PACKAGE", "QUANTITY_PACKAGES", "QUANTITY_PALLETS", "TONNAGE"],
        },
    ),
]


@admin.register(Portals)
class PortalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'member_id',
        'name',
        'auth_id_create_date',
    )


@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('id_b24', 'first_name', 'last_name')


@admin.register(ProductRow)
class ProductRowAdmin(admin.ModelAdmin):
    list_display = ['id', 'PORTAL', 'PRODUCTROW_ID', 'OWNER_ID', 'OWNER_TYPE']
    fieldsets = FIELDSETS_FOR_PRODUCTROW


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['NAME', ]
