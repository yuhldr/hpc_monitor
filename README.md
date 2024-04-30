# linux_tools

`.gitlab-ci.yml` 自动部署

```bash
# 创建单独环境
sudo /usr/local/anaconda3/bin/conda create --prefix /usr/local/anaconda3/envs/gr python=3.11
# 权限问题
chown -R gitlab-runner:root /usr/local/anaconda3/envs/gr
conda install jinja2
```


## 其他

详见 [ylt/bin/ylt](ylt/bin/ylt)

```bash
mkdir -p /opt/ylt//cache/
```

```bash
* * * * * source /usr/local/anaconda3/bin/activate /usr/local/anaconda3/envs/gr && ylt
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
0 02 * * * source /usr/local/anaconda3/bin/activate /usr/local/anaconda3/envs/gr && ylt_ref_disk
```

## 软连接

让所有人可以使用

```bash
ln -s /usr/local/anaconda3/envs/gr/bin/topn /usr/local/bin
ln -s /usr/local/anaconda3/envs/gr/bin/sinfo-s /usr/local/bin
```