def get_log(request, operation_id):
    """查询日志"""

    operation = Operation.objects.get(id=operation_id)

    try:
        logs = json.loads(operation.log)
    except TypeError as e:
        logs = []

    log_content = '<div class="log-content">'
    for log_item in logs:
        job_log_content = log_item.get('log_content')
        log_content += '<div class="ip-start"><prev>IP: {}</prev></div>'.format(log_item.get('ip', ''))
        log_content += ''.join(
            map(lambda x: '<prev>{}</prev><br>'.format(x), job_log_content.split('\n'))
        )
        log_content += '<div class="ip-end"></div>'
    log_content += '</div>'

    return JsonResponse({
        'result': True,
        'data': log_content
    })