function get_host() {
    $.ajax({
        url: '{{ SITE_URL }}api/get_hosts/',
        type: 'GET',
        data: {"biz_id": $("#biz_id").val(), "script_type": $("#script_type").val()},
        success: function (res) {
            if (res.result) {
                $('#table_demo2 tbody').html(res.data)
            } else {
                alert(res.message);
            }
        }
    });
}