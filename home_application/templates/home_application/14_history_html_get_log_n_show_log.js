function get_log(celery_id) {
    console.log(celery_id)
    var url = '{{ SITE_URL }}' + 'api/get_log/' + celery_id + '/';
    $.get(url, {}, function (res) {
        if (res.result) {
            show_log(res.data);
        } else {
            alert(res.message);
        }
    })
}

function show_log(log_content) {
    var d = dialog({
        width: 800,
        height: 500,
        padding: 0,
        //quickClose: true,
        title: '日志详情',
        content: log_content,
    });
    d.showModal();
}


<link href="https://magicbox.bk.tencent.com/static_api/v3/assets/artDialog-6.0.4/css/ui-dialog.css" rel="stylesheet">
<script src="https://magicbox.bk.tencent.com/static_api/v3/assets/artDialog-6.0.4/dist/dialog-min.js"></script>