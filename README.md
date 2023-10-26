# linux_tools


## 其他

详见 [example/main.py](example/main.py)

```bash
/opt/anaconda3/bin/python /opt/anaconda3/bin/ylt
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
00 00 * * * /opt/anaconda3/bin/python /opt/anaconda3/bin/ylt_ref_disk
```

