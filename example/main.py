'''文件入口'''
from ylt import temps
from ylt import disk
from ylt import nodes
from ylt import ns_state


to_mail_users_disk=["yuhldr@qq.com", "wys@lzu.edu.cn", "dongjq@lzu.edu.cn"]
to_mail_users_temp=["yuhldr@qq.com", "1264171820@qq.com"]
to_mail_users_nodes=["yuhldr@qq.com"]

temps.main(to_mail_users_temp)
disk.main(to_mail_users_disk)
nodes.main(to_mail_users_nodes)
ns_state.main()
