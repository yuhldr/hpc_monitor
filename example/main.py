'''文件入口'''
from ylt import temps
from ylt import disk
from ylt import nodes
from ylt import ns_state


to_mail_users_disk=["***REMOVED***", "***REMOVED***", "***REMOVED***"]
to_mail_users_temp=["***REMOVED***", "***REMOVED***"]
to_mail_users_nodes=["***REMOVED***"]

temps.main(to_mail_users_temp)
disk.main(to_mail_users_disk)
nodes.main(to_mail_users_nodes)
ns_state.main()
