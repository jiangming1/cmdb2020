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