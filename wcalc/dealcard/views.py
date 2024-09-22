import core.methods as core_methods

from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from core.bitrix24.bitrix24 import create_portal


@xframe_options_exempt
@csrf_exempt
def index(request):
    """Метод страницы Карточка сделки."""
    template = 'dealcard/index.html'
    title = 'Страница карточки сделки'

    try:
        member_id, deal_id, auth_id = core_methods.initial_check(request)
    except BadRequest:
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })
    portal = create_portal(member_id)
    user_info = core_methods.get_current_user(request, auth_id, portal)

    context = {
        'title': title,
        'member_id': member_id,
        'deal_id': deal_id,
        'user': user_info
    }

    response = render(request, template, context)
    if auth_id:
        response.set_cookie(key='user_id', value=user_info.get('user_id'))
    return response
