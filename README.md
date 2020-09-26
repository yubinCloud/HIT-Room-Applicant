# HIT-Room-Applicant 教室申请系统
哈尔滨工业大学（威海）教室申请系统。
后端由Flask搭建

## 路由表

### 管理员端相关路由函数
|API |url|请求方式|文件名|负责人|
|:----|:----|:----|:----|:---|
|管理员登录|http://xx.com/api/admin/login|POST|adm_login|zyq|
|管理员登出|http://xx.com/api/admin/logout|POST|adm_logout|zyq|
|获取用户信息|http://xx.com/api/admin/user|GET|
|查看账号列表|http://xx.com/api/admin/logout|GET|account_about|xql|
|新增管理员账号|http://xx.com/api/admin/account|POST|account_about|xql|
|获取账号总数|http://xx.com/api/admin/account/num|GET|account_about|yb|
|修改管理员账号|http://xx.com/api/admin/account/id|POST|admin_modify|xql|
|查看公告列表|http://xx.com/api/admin/notice|GET|adm_notice_bp|yb|
|获取公告数量|http://xx.com/api/admin/notice/num|GET|adm_notice_bp|yb|
|获取教室列表|http://xx.com/api/admin/room|GET|adm_room|yb|
|新增教室|http://xx.com/api/admin/room|POST|adm_room|yb|
|获取教室总数量|http://xx.com/api/admin/room/num|GET|adm_room|yb|
|获取无管理员的教室|http://xx.com/api/admin/room/noadmin|GET|adm_room|yb|
|获取无管理员教室数量|http://xx.com/api/admin/room/noadmin/num|GET|adm_room|yb|
|移入/移出教室|http://xx.com/api/admin/myroom|POST|adm_myroom|yb|


### 学生端相关路由函数
|API |url|请求方式|文件名|负责人|
|:----|:----|:----|:----|:---|
|查看公告列表|http://xx.com/api/stu/notice|GET|notice.py|wz|
|查看公告详情|http://xx.com/api/stu/notice/id|GET|notice.py|wz|
|获取全部楼号|http://xx.com/api/stu/building|GET|room.py|xql|
|教室使用说明|http://xx.com/api/stu/room/use/id|GET|room.py|zyq|
|查看教室介绍|http://xx.com/api/stu/room/id|GET|room.py|zyq|
|教室使用情况|http://xx.com/api/stu/room/use|GET|room.py|yb|
|我的申请列表|http://xx.com/api/stu/apply|GET|stu_apply.py|yb|
|我的申请详细内容|http://xx.com/api/stu/apply/id|GET|stu_apply_info.py|yb|
|修改申请内容|http://xx.com/api/stu/apply/id|POST|stu_apply_info.py|xql|
|学生提交教室申请|http://xx.com/api/stu/apply|POST|stu_apply.py|wz|
|上传教室申请材料图片|http://xx.com/api/stu/apply/image|POST|||
|获取时间表|http://xx.com/api/stu/timetable|GET|time_get.py|xql|
