$('#submit').click(function (event) {
    var records = $('#table_demo2>tbody input:checked').closest('tr');
    if (!records.length) {
        alert('请选择要执行的机器！');
        return false;
    }
    var ips = [];
    for (i = 0; i < records.length; i++) {
        let ip = $($(records[i]).find('.ip')).text();
        ips.push(ip)
    }
    // console.log(ips);
    var biz_id = $("#biz_id").val();
    var script_type = $("#script_type").val();
    $.post('{{SITE_URL}}api/execute/', {
        'biz_id': biz_id,
        'ips': ips,
        'script_param': $("#script-param").val(),
        'script_type': script_type
    }, function (data) {
        if (data.result) {
            submitSuccess();
        } else {
            alert("获取失败")
        }
    }, 'json');
});