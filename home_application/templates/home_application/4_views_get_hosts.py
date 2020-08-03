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