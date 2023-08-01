'''文件入口'''
from ylt import temps
from ylt import disk
from ylt import nodes
from ylt import ns_state


# 监控master温度
to_mail_users_temp=["***REMOVED***", "***REMOVED***"]
temps.main(to_mail_users_temp)

# 监控master磁盘
to_mail_users_disk=["***REMOVED***", "***REMOVED***", "***REMOVED***"]
disk.main(to_mail_users_disk)

# 监控节点在线状态
to_mail_users_nodes=["***REMOVED***"]
nodes.main(to_mail_users_nodes)

# 显示独立服务器状态
ns_state.main(["ns1", "ns2", "ns3", "ns4"])
