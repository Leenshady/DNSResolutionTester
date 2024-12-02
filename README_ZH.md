# DNSperf
- [English](README.md) | [中文](README_ZH.md)  

DNSperf是一个测试DNS服务器解析A记录性能的工具，可以帮助您为本地网络选择最合适的DNS。

## 开发环境
- Python 3.12.3  

您可以从 https://www.python.org/ 下载。

## 依赖库
- dnspython
- numpy
- pandas
- requests

在 bash（Linux）或者cmd（Windows）中运行以下代码安装依赖库。
```cmd
pip install dnspython
pip install numpy
pip install pandas
pip install requests
```

## 配置
您可以在 domain_names.json 中添加要用来测试DNS的域名。
```json
[
    "www.github.com",
    "www.baidu.com"
]
```
您可以在 dns_server.json 中添加要测试的DNS服务器。
```json
{
    "DNS": [
        {
            "name": "Alibaba DNS",
            "addr": "223.5.5.5"
        },
        {
            "name": "Google DNS",
            "addr": "8.8.8.8"
        }
    ],
    "DoH": [
        {
            "name": "Alibaba DoH",
            "addr": "https://dns.alidns.com:443/dns-query"
        },
        {
            "name": "Google DoH",
            "addr": "https://dns.google/dns-query"
        }
    ]
}
```

## 运行
运行源代码。
```cmd
python DNSperf.py
```
运行源代码，并将测试结果输出到result.log文件。
```cmd
python DNSperf.py --log result
```
在Windows系统中运行DNSperf，并将测试结果输出到result.log文件。
```cmd
DNSperf.exe --log result
```

## DNS支持
- [x] 支持DNS（IP Address）
- [x] 支持DNS over HTTPS(RFC 8484，支持GET和POST)
- [ ] 支持DNS over HTTPS(JSON API，支持GET)
- [ ] 支持DNS over TLS
- [ ] 增加熔断功能，多次解析无应答直接结束该DNS测试，避免等待时间过长
- [ ] 优化DNS测试算法，避免触发QoS

## 提醒
因部分公共DNS采用了QoS策略，测试结果有可能不准确。
