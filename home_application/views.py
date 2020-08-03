# -*- coding: utf-8 -*-
from django.shortcuts import render
from blueking.component.shortcuts import get_client_by_request
from django.http import JsonResponse
from django.template.loader import render_to_string
import base64
import datetime
import json
import time
from celery.task import task
#from common.mymako import render_mako_context,render_mako_tostring,render_json
from home_application.models import Script,Operation

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    result, biz_list, message = get_biz_list(request)
    scripts = Script.objects.all()
    return render(request, 'home_application/execute.html',{'biz_list': biz_list,'scripts':scripts})

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

def get_hosts(request):
    biz_id = request.GET.get("biz_id", 0)
    if biz_id:
        biz_id = int(biz_id)
    else:
        return JsonResponse({
            'result': False,
            'message': "must provide biz_id to get hosts"
        })

    client = get_client_by_request(request)
    resp = client.cc.search_host({
        "page": {"start": 0, "limit": 5, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [
                    # "bk_cloud_id",
                    # "bk_host_id",
                    # "bk_host_name",
                    # "bk_os_name",
                    # "bk_os_type",
                    # "bk_host_innerip",
                ],
                "condition": []
            },
            # {"bk_obj_id": "module", "fields": [], "condition": []},
            # {"bk_obj_id": "set", "fields": [], "condition": []},
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": biz_id
                    }
                ]
            }
        ]
    })
    hosts = [{
        "ip": host['host']['bk_host_innerip'],
        "os": host['host']['bk_os_name'],
        "bk_cloud_id": host['host']['bk_cloud_id'][0]["id"],
    } for host in resp['data']['info']]
    table_data = render_to_string('home_application/execute_tbody.html', {
        'hosts': hosts,
    })
    return JsonResponse({
        'result': True,
        'data': table_data,
        'message': "success"
    })



def execute(request):
    """执行任务"""

    biz_id = request.POST.get("biz_id")
    script_type = request.POST.get("script_type")
    script_param = request.POST.get("script_param", "")
    ips = request.POST.getlist("ips[]")

    if biz_id:
        biz_id = int(biz_id)

    if script_type:
        script_type = int(script_type)

    try:
        script_content = Script.objects.get(id=script_type).script
    except Script.DoesNotExist:
        return JsonResponse({"result": False, "message": "script not exist!"})

    client = get_client_by_request(request)

    task = run_script.delay(client, biz_id, script_content, script_param, ips)

    opt = Operation.objects.create(
        biz=biz_id,
        script=Script.objects.get(id=script_type),
        machine_numbers=len(ips),
        celery_id=task.id,
        argument=script_param,
        user=request.user.username
    )

    return JsonResponse({"result": True, "data": opt.celery_id, "message": "success"})


@task
def run_script(client, biz_id, script_content, script_param, ips):
    """快速执行脚本"""

    # 执行中
    Operation.objects.filter(celery_id=run_script.request.id).update(
        status="running"
    )

    resp = client.job.fast_execute_script(
        bk_biz_id=biz_id,
        account="root",
        script_param=base64.b64encode(script_param.encode()).decode(),
        script_content=base64.b64encode(script_content.encode()).decode(),
        ip_list=[{"bk_cloud_id": 0, "ip": ip} for ip in ips]
    )

    # 启动失败
    if not resp.get('result', False):
        Operation.objects.filter(celery_id=run_script.request.id).update(
            log=json.dumps([resp.get("message")]),
            end_time=datetime.datetime.now(),
            result=False,
            status="start_failed"
        )

    task_id = resp.get('data').get('job_instance_id')
    poll_result = poll_job_task(client, biz_id, task_id)

    # 查询日志
    resp = client.job.get_job_instance_log(job_instance_id=task_id, bk_biz_id=biz_id)
    ip_logs = resp['data'][0]['step_results'][0]['ip_logs']
    status = resp['data'][0]['status']

    result = True if status == 3 else False
    Operation.objects.filter(celery_id=run_script.request.id).update(
        log=json.dumps(ip_logs),
        end_time=datetime.datetime.now(),
        result=result,
        status="successed" if result else "failed"
    )


def poll_job_task(client, biz_id, job_instance_id):
    """true/false/timeout"""

    count = 0

    res = client.job.get_job_instance_status(job_instance_id=job_instance_id, bk_biz_id=biz_id)

    while res.get('data', {}).get('is_finished') is False and count < 30:
        res = client.job.get_job_instance_status(job_instance_id=job_instance_id, bk_biz_id=biz_id)
        count += 1
        time.sleep(3)

    return res
