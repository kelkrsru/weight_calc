from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from core.bitrix24.bitrix24 import create_portal
from core.methods import get_current_user
from core.models import Portals


@xframe_options_exempt
@csrf_exempt
def index(request):

    template = 'settings/index.html'
    auth_id = ''

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        if 'AUTH_ID' in request.POST:
            auth_id: str = request.POST.get('AUTH_ID')
    elif request.method == 'GET':
        member_id = request.GET.get('member_id')
    else:
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })

    portal: Portals = create_portal(member_id)
    user_info = get_current_user(request, auth_id, portal)

    context = {
        'member_id': member_id,
        'user': user_info,
    }
    response = render(request, template, context)
    if auth_id:
        response.set_cookie(key='user_id', value=user_info.get('user_id'))
    return response
