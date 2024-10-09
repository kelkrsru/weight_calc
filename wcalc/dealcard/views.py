import logging

from django.conf import settings as app_settings
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

import core.methods as core_methods
import dealcard.methods as dealcard_methods
from core.bitrix24.bitrix24 import DealB24, create_portal
from core.models import Package, ProductRow
from settings.models import SettingsPortal

logger = logging.getLogger(__name__)
SEPARATOR = '*' * 40
NEW_STR = '\n    '


@xframe_options_exempt
@csrf_exempt
def index(request):
    """Метод страницы Карточка сделки."""
    template = 'dealcard/index.html'
    title = 'Страница карточки сделки'
    title_app = app_settings.TITLE_APP

    logger.info(f'{SEPARATOR}')
    logger.info(f'{NEW_STR}{request.method=}  {request.build_absolute_uri()}')

    try:
        member_id, deal_id, auth_id = core_methods.initial_check(request)
        logger.debug(f'{NEW_STR}{member_id=}  {deal_id=}  {auth_id=}')
    except BadRequest:
        logger.error(f'{NEW_STR}Неизвестный тип запроса')
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })
    portal = create_portal(member_id)
    logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')
    user_info = core_methods.get_current_user(request, auth_id, portal)
    logger.info(f'{NEW_STR}{user_info=}')

    productrows_bx = dealcard_methods.get_all_products_deal(request, portal, deal_id)
    logger.debug(f'{NEW_STR}{productrows_bx=}')

    productrows_db, log_msg = dealcard_methods.create_productrows_in_db(portal, deal_id, productrows_bx)
    logger.info(f'{log_msg}')
    logger.debug(f'{NEW_STR}{productrows_db=}')

    packages = Package.objects.filter(ACTIVE=True)
    logger.debug(f'{NEW_STR}{packages=}')

    context = {
        'title': title,
        'title_app': title_app,
        'member_id': member_id,
        'deal_id': deal_id,
        'user': user_info,
        'productrows': productrows_db,
        'packages': packages
    }

    response = render(request, template, context)
    if auth_id:
        response.set_cookie(key='user_id', value=user_info.get('user_id'), samesite='None', secure=True)
    return response


@xframe_options_exempt
@csrf_exempt
def calculate(request):
    """Метод для сохранения изменений в таблице."""

    logger.info(f'{SEPARATOR}')
    logger.info(f'{NEW_STR}{request.method=}  {request.build_absolute_uri()}')

    productrow_id = int(request.POST.get('productrow_id'))
    package_id = int(request.POST.get('package_id'))
    logger.info(f'{NEW_STR}{productrow_id=}  {package_id=}')

    try:
        productrow = ProductRow.objects.get(id=productrow_id)
        logger.info(f'{NEW_STR}{productrow=}')
    except ObjectDoesNotExist:
        logger.error(f'{NEW_STR}productrow ObjectDoesNotExist')
        return JsonResponse({'error': 'ProductRowObjectDoesNotExist'})
    except Exception as ex:
        logger.error(f'{NEW_STR}productrow {ex.args[0] - ex.args[1]}')
        return JsonResponse({'error': f'{ex.args[0] - ex.args[1]}'})

    if not package_id:
        productrow.PACKAGE = None
        productrow.QUANTITY_PACKAGES = 0
        productrow.QUANTITY_PALLETS = 0
        productrow.TONNAGE = 0
        productrow.save()
        logger.info(f'{NEW_STR}Упаковка не задана, обнуляем все значения')
        return JsonResponse({'result': 'ok', 'quantity_packages': 0, 'quantity_pallet': 0, 'tonnage': 0})

    try:
        package = Package.objects.get(id=package_id)
        logger.info(f'{NEW_STR}{package=}')
    except ObjectDoesNotExist:
        logger.error(f'{NEW_STR}package ObjectDoesNotExist')
        return JsonResponse({'error': 'PackageObjectDoesNotExist'})
    except Exception as ex:
        logger.error(f'{NEW_STR}package {ex.args[0] - ex.args[1]}')
        return JsonResponse({'error': f'{ex.args[0] - ex.args[1]}'})

    quantity_packages, quantity_pallet, tonnage = dealcard_methods.calculate_values_productrows(productrow)
    logger.info(f'{NEW_STR}{quantity_packages=}  {quantity_pallet=}  {tonnage=}')
    logger.info(f'{NEW_STR}Сохранили значения в БД')

    return JsonResponse({'result': 'ok', 'quantity_packages': quantity_packages, 'quantity_pallet': quantity_pallet,
                         'tonnage': tonnage})


@xframe_options_exempt
@csrf_exempt
def send_deal(request):
    """Метод для отправки значений в сделку."""

    logger.info(f'{SEPARATOR}')
    logger.info(f'{NEW_STR}{request.method=}  {request.build_absolute_uri()}')

    member_id = request.POST.get('member_id')
    deal_id = int(request.POST.get('deal_id'))
    quantity_pallet = request.POST.get('quantity_pallet')
    tonnage = request.POST.get('tonnage')
    logger.info(f'{NEW_STR}{member_id=}  {deal_id=}  {quantity_pallet=}  {tonnage=}')

    portal = create_portal(member_id)
    logger.debug(f'{NEW_STR}{portal.id=}  {portal.name=}')
    settings_portal = get_object_or_404(SettingsPortal, portal=portal)
    logger.debug(f'{NEW_STR}{settings_portal.id=}')

    deal_bx = DealB24(portal, deal_id)
    logger.debug(f'{NEW_STR}{deal_bx=}')
    fields = {settings_portal.quantity_pallet_code: quantity_pallet, settings_portal.tonnage_code: tonnage}
    logger.debug(f'{NEW_STR}{fields=}')
    result = deal_bx.update(fields)
    logger.info(f'{NEW_STR}{result=}')

    return JsonResponse({'result': result})
