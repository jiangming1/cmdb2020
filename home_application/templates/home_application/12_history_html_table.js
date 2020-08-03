var table = $('#table2_demo1').DataTable({
                autoWidth: true,
                processing: true,
                paging: true, //隐藏分页
                ordering: false, //关闭排序
                info: true, //隐藏左下角分页信息
                searching: false, //关闭搜索
                pageLength: 5, //每页显示几条数据
                lengthChange: false, //不允许用户改变表格每页显示的记录数
                columns: [
                    {data: "biz"},
                    {data: "user"},
                    {data: "script"},
                    {data: "start_time"},
                    {data: "machine_numbers"},
                    {
                        data: "status",
                        render: function (data, type, row, meta) {
                            // http://magicbox.bk.tencent.com/#detail/show?id=list1&isPro=0
                            var color = {
                                'successed': 'king-success',
                                'running': 'king-warning',
                                'failed': 'king-danger',
                                'queue': 'king-info',
                                'finished': 'king-primary',
                            }[data];
                            return '<span class="badge ' + color + '">' + data + '</span>'
                        }
                    },
                    {data: "argument"},
                    {
                        data: null,
                        orderable: false,
                        render: function (data, type, row, meta) {
                            return '<a class="king-btn king-default del" href="javascript: get_log(' + data.id + ');">详情</a>';
                        }
                    }
                ],
                ajax: {
                    url: "{{ SITE_URL }}api/get_operations/",
                    dataSrc: "data",
                    data: function (d) {
                        return $.extend({}, d, {
                            "biz": $("#biz_list").val(),
                            "operator": $("#operators").val(),
                            "script": $("#scripts").val(),
                            "timerange": $("#daterangepicker_demo3").val()
                        });
                    }
                },

                language: {
                    search: '搜索：',
                    processing: '加载中',
                    lengthMenu: "每页显示 _MENU_ 记录",
                    zeroRecords: "没找到相应的数据！",
                    info: "分页 _PAGE_ / _PAGES_",
                    infoEmpty: "暂无数据！",
                    infoFiltered: "(从 _MAX_ 条数据中搜索)",
                    paginate: {
                        first: '首页',
                        last: '尾页',
                        previous: '上一页',
                        next: '下一页',
                    }
                }
            });