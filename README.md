# sliver-webhook 

官方推荐上线通知功能使用第三方项目（ https://github.com/BishopFox/sliver/issues/870 ），过于麻烦。
脚本实现实时上线通知功能，无需修改 sliver 代码，后台运行程序即可。

## 使用说明

1.修改 webhook_url 为自己的钉钉机器人链接

2.上传到 sliver server 的机器，执行以下命令即可

```
tmux new -s sliver-webhook
python3 sliver-webhook.py
```
