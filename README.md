# linux_tools

如果集群设置了`gitlab`和`gitlab-runner`，这里支持`.gitlab-ci.yml` 自动部署

下面使用 `anaconda3` 环境

```bash
# 创建单独环境
sudo /usr/local/anaconda3/bin/conda create --prefix /usr/local/anaconda3/envs/gr python=3.11
# 权限问题
chown -R gitlab-runner:root /usr/local/anaconda3/envs/gr
conda install jinja2
```

## 使用方法

需要设置，在本项目搜索 `***REMOVED***`，里面对应的内容要修改

- [ylt/bin/ylt](ylt/bin/ylt) 这里面，需要设置接受各种信息的人的邮箱
- [ylt/utils/send_mail.py](ylt/utils/send_mail.py) 设置发邮件的人和密码


crontab参考

```bash
SHELL=/bin/zsh
PATH=/usr/bin:/bin:/usr/local/anaconda3/bin

# 登录节点 温度、磁盘、在线状态 监控
*/5 * * * * source activate gr && ylt
# 登录节点磁盘详情输出
0 00 * * 6 source activate gr && ylt_ref_disk
# 刷新节点的top等数据
*/5 * * * * source activate gr && ylt_ref_2s

```

## 其他

crontab

```bash
SHELL=/bin/zsh
PATH=/usr/bin:/bin:/usr/local/anaconda3/bin
```


详见 [ylt/bin/ylt](ylt/bin/ylt)

```bash
mkdir -p /opt/ylt//cache/
```

```bash
* * * * * source activate gr && ylt
* * * * * source activate gr && ylt_ref_2s
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
0 02 * * * source activate gr && ylt_ref_disk
```

## 软连接

让所有人可以使用

```bash
ln -s /usr/local/anaconda3/envs/gr/bin/topn /usr/local/bin
ln -s /usr/local/anaconda3/envs/gr/bin/sinfo-s /usr/local/bin
```