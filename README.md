# linux_tools

`.gitlab-ci.yml` 自动部署

```bash
# 创建单独环境
conda create --name gr python=3.11
# 权限问题
chown -R gitlab-runner:http /usr/local/anaconda3/envs/gr
```


## 其他

详见 [ylt/bin/ylt](ylt/bin/ylt)

```bash
* * * * * source /usr/local/anaconda3/bin/activate gr && ylt
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
0 02 * * * source /usr/local/anaconda3/bin/activate gr && ylt_ref_disk
```

## 软连接

让所有人可以使用

```bash
ln -s /usr/local/anaconda3/envs/gr/bin/topn /usr/bin
ln -s /usr/local/anaconda3/envs/gr/bin/sinfo-s /usr/bin
```