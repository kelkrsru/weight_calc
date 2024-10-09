import decimal

from django.shortcuts import render

from core.bitrix24.bitrix24 import DealB24
from core.models import ProductRow


def get_all_products_deal(request, portal, deal_id):
    """Метод получения всех продуктов из сделки."""
    try:
        deal_bx = DealB24(portal, deal_id)
        deal_bx.get_all_products()
    except RuntimeError as ex:
        return render(request, 'error.html', {
            'error_name': ex.args[0],
            'error_description': ex.args[1]
        })
    except Exception as ex:
        return render(request, 'error.html', {
            'error_name': ex.args[0],
            'error_description': ex.args[0]
        })
    return deal_bx.products


def create_productrows_in_db(portal, deal_id, productrows):
    """Метод для создания или обновления товарных позиций в БД приложения, а также удаление старых из БД приложения."""
    returning_log_msg = '\n'
    actual_ids = []
    for productrow in productrows:
        productrow['PORTAL'] = portal
        productrow_id = productrow.pop('ID')
        productrow_db, created = ProductRow.objects.update_or_create(PRODUCTROW_ID=productrow_id, defaults=productrow)
        if created:
            returning_log_msg += (f'    Создана товарная позиция ID {productrow_db.id}, PRODUCTROW_ID '
                                  f'{productrow_db.PRODUCTROW_ID}, PORTAL {productrow_db.PORTAL}'
                                  f' DEAL_ID {productrow_db.OWNER_ID}\n')
        else:
            if productrow_db.PACKAGE:
                quantity_packages = decimal.Decimal(
                    round(productrow_db.QUANTITY / productrow_db.PACKAGE.QUANTITY_JARS, 2))
                quantity_pallet = decimal.Decimal(
                    round(productrow_db.QUANTITY / productrow_db.PACKAGE.QUANTITY_ON_PALLET, 2))
                tonnage = decimal.Decimal(round(productrow_db.PACKAGE.WEIGHT_BRUTTO * quantity_pallet))

                productrow.QUANTITY_PACKAGES = quantity_packages
                productrow.QUANTITY_PALLETS = quantity_pallet
                productrow.TONNAGE = tonnage
                productrow.save()
            returning_log_msg += (f'    Обновлена товарная позиция ID {productrow_db.id}, PRODUCTROW_ID '
                                  f'{productrow_db.PRODUCTROW_ID}, PORTAL {productrow_db.PORTAL}'
                                  f' DEAL_ID {productrow_db.OWNER_ID}\n')
        actual_ids.append(int(productrow_id))

    productrows_db = ProductRow.objects.filter(PORTAL=portal, OWNER_TYPE='D', OWNER_ID=deal_id)
    for productrow in productrows_db:
        if productrow.PRODUCTROW_ID not in actual_ids:
            returning_log_msg += (f'    Удалена товарная позиция ID {productrow.id}, PRODUCTROW_ID '
                                  f'{productrow.PRODUCTROW_ID}, PORTAL {productrow.PORTAL},'
                                  f' DEAL_ID {productrow.OWNER_ID}\n')
            productrow.delete()
    productrows_db = ProductRow.objects.filter(PORTAL=portal, OWNER_TYPE='D', OWNER_ID=deal_id)

    return productrows_db, returning_log_msg
