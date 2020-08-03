function submitSuccess() {
    var d = dialog({
        width: 260,
        title: '操作提示',
        ok: function () {
            location.href = "{{ SITE_URL }}history/"
        },
        okValue: '查看执行结果',
        content: '<div class="king-notice-box king-notice-success"><p class="king-notice-text">任务提交成功！</p></div>',
        cancelValue: '继续执行任务',
        cancel: function () {
            // do something
        }
    });
    d.showModal();
}


<link href="https://magicbox.bk.tencent.com/static_api/v3/assets/artDialog-6.0.4/css/ui-dialog.css" rel="stylesheet">
<script src="https://magicbox.bk.tencent.com/static_api/v3/assets/artDialog-6.0.4/dist/dialog-min.js"></script>