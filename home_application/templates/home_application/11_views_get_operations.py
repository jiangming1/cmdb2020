def get_operations(request):
    """
    Ajax加载操作记录
    """
    biz = request.GET.get('biz')
    script = request.GET.get('script')
    operator = request.GET.get('operator')
    time_range = request.GET.get('timerange')

    operations = Operation.objects.all()
    if biz and biz != 'all':
        operations = operations.filter(biz=int(biz))
    if script and script != 'all':
        operations = operations.filter(script_id=int(script))
    if operator and operator != 'all':
        operations = operations.filter(user=operator)
    if time_range:
        start_time, end_time = time_range.split('~')
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        operations = operations.filter(start_time__range=(start_time, end_time))

    data = [opt.to_dict() for opt in operations]
    return JsonResponse({
        'result': True,
        'data': data,
        'message': "success"
    })