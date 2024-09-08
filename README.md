# nasu-check-alerter
アラート用スクリプト  
influxdbで最新値から180秒以上、600秒以下の場合にdiscordにアラートを送信する  

pyを/usr/local/bin/にコピー  
configを/usr/local/etc/にコピー  
.serviceを/usr/lib/systemd/system/　に配置  
```
systemctl daemon-reload  
systemctl enable health_check_alerter.service
```
