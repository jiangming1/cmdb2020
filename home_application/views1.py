# -*- coding: utf-8 -*-
from django.shortcuts import render
from blueking.component.shortcuts import get_client_by_request


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    result, biz_list, message = get_biz_list(request)
    return render(request, 'home_application/execute.html',{'biz_list': biz_list})

def show_history(request):
    """
    联系我们
    """
    return render(request, 'home_application/history.html')

def contact(request):
    """
    联系我们
    """
    return render(request, 'home_application/contact.html')

def get_biz_list(request):
    biz_list = []
    client = get_client_by_request(request)
    kwargs = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    resp = client.cc.search_business(**kwargs)

    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            biz_list.append({
                'name': _d.get('bk_biz_name'),
                'id': _d.get('bk_biz_id'),
            })
    return resp.get('result'), biz_list, resp.get('message')
