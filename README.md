# linux_tools


## top

查看子节点top（其实直接开放ssh免密ssh其他节点也行）

```cron
*/1 * * * * /home/data/gitFile/linux_tools/bin/tops.sh
```

## 其他

详见 [example/main.py](example/main.py)

```bash
cd /home/data/gitFile/linux_tools/example && /opt/anaconda3/bin/python ./main.py
```

额外设置

### 磁盘

统计太慢，每天凌晨自动统计用户磁盘使用情况

```bash
00 00 * * * /home/data/gitFile/linux_tools/bin/monitor_disk.sh
```

