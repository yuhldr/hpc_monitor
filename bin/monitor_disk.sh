#/bin/sh

du -h --max-depth=1  /home |sort -hr > "/home/data/disk_home/home_`date +%Y-%m-%d`.txt"

rm -f /home/data/disk_home/home_today.txt
cp "/home/data/disk_home/home_`date +%Y-%m-%d`.txt" /home/data/disk_home/home_today.txt

rm -f "/home/data/disk_home/home_`date -d '-365 days' +%Y-%m-%d`.txt"
