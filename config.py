mail_from_usr = "***REMOVED***"
mail_from_pw = "***REMOVED***"

disk_home_warning_to_mails = ["***REMOVED***", "***REMOVED***"]

# 磁盘使用率到达多少时体系
warning_disk_home_rate = [80, 90, 95, 98]

# 每隔多少小时提醒
warning_disk_home_time = [24 * 30, 7 * 24, 6 * 24, 24]
# 提醒内容
warning_disk_home_title = [
    "磁盘占用已经到达警戒值", "磁盘占用过高，影响性能！", "磁盘占用极高！严重影响性能！", "磁盘占用危险！有崩盘风险！"
]
warning_disk_home_msg = [
    "磁盘占用已经到达警戒值，请提醒清理各自空间", "磁盘占用过高！影响服务器性能！，请提醒用户清理各自空间",
    "磁盘占用极高！严重影响服务器性能！，请提醒占用过多的同学，立刻清理、转移数据", "磁盘占用危险！有崩盘风险！，请管理员立刻清理空间"
]