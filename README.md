# linux_tools

`.gitlab-ci.yml` 自动部署

```bash
chown root:http /opt/anaconda3/bin/
chmod 775 /opt/anaconda3/bin/

chown -R root:http /home/data/gitFile/linux_tools
chmod 775 /home/data/gitFile/linux_tools

chown root:http /opt/anaconda3/lib/python3.8/site-packages/
chmod 775 /opt/anaconda3/lib/python3.8/site-packages/
```


## 其他

详见 [ylt/bin/ylt](ylt/bin/ylt)

```bash
* * * * * /opt/anaconda3/bin/ylt
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
0 02 * * * /opt/anaconda3/bin/ylt_ref_disk
```

## 软连接

让所有人可以使用

```bash
ln -s /opt/anaconda3/bin/topn /bin
ln -s /opt/anaconda3/bin/sinfo-s /bin
```