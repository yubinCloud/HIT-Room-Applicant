# 学生端相关路由函数
|API |url|请求方式|文件名|负责人|
|:----|:----|:----|:----|:---|
|查看公告列表|http://xx.com/api/stu/notice|GET|notice_list.py|王政|
|查看公告详情|http://xx.com/api/stu/notice/id|GET|notice_info.py|王政|
|获取全部楼号|http://xx.com/api/stu/building|GET|room_floor_get.py|向乾龙|
|获取时间表|http://xx.com/api/stu/timetable|GET|time_get.py|向乾龙|
|教室使用情况|http://xx.com/api/stu/room/use|GET|stu_room_use.py|俞斌|
|教室使用说明|http://xx.com/api/stu/room/use/id|GET|room_use_info.py|钟亦奇|
|查看教室介绍|http://xx.com/api/stu/room/id|GET|room_info.py|钟亦奇|
|我的申请列表|http://xx.com/api/stu/apply|GET|stu_apply.py|俞斌|
|我的申请详细内容|http://xx.com/api/stu/apply/id|GET|stu_apply_info.py|俞斌|
|修改申请内容|http://xx.com/api/stu/apply/id|POST|stu_apply_info.py|向乾龙|
|学生提交教室申请|http://xx.com/api/stu/apply|POST|stu_apply.py|王政|
|上传教室申请材料图片|http://xx.com/api/stu/apply/image|POST|||

# 管理员端相关路由函数
|API |url|请求方式|文件名|负责人|
|:----|:----|:----|:----|:---|
|管理员登录|http://xx.com/api/admin/login|POST|adm_login|钟亦奇|
|管理员登出|http://xx.com/api/admin/logout|POST|adm_logout|钟亦奇|
|查看账号列表|http://xx.com/api/admin/logout|GET|account_about|向乾龙|
|新增管理员账号|http://xx.com/api/admin/account|POST|account_about|向乾龙|
|获取账号总数|http://xx.com/api/admin/account/num|GET|account_about|俞斌|
|修改管理员账号|http://xx.com/api/admin/account/id|POST|admin_modify|向乾龙|
|查看公告列表|http://xx.com/api/admin/notice|GET|adm_notice_bp|俞斌|
|获取教室列表|http://xx.com/api/admin/room|GET|adm_room|俞斌|
|新增教室|http://xx.com/api/admin/room|POST|adm_room|俞斌|
|获取教室总数量|http://xx.com/api/admin/room/num|GET|adm_room|俞斌|
|获取无管理员的教室|http://xx.com/api/admin/room/noadmin|GET|adm_room|俞斌|
|获取无管理员教室数量|http://xx.com/api/admin/room/noadmin/num|GET|adm_room|俞斌|
|移入/移出教室|http://xx.com/api/admin/myroom|POST|adm_myroom|俞斌|