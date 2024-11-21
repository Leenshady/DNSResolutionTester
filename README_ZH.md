# DNSperf
- [English](README.md) | [中文](README_ZH.md)  

DNSperf是一个DNS服务器性能测试工具，可以帮助您为本地网络选择最合适的DNS。
# 如何使用
您可以在 domain_names.json 中添加要用来测试DNS的域名。
```json
["www.github.com","www.baidu.com"]
```
您可以在 dns_server.json 中添加要测试的DNS服务器。
```json
["8.8.8.8","223.5.5.5"]
```
# 开发环境
- Python 3.12.3  

您可以从 https://www.python.org/ 下载。
# 依赖库
- dnspython 2.7.0
- numpy 2.1.3
- pandas 2.2.3  

在 bash（Linux）或者cmd（Windows）中运行以下代码安装依赖库。
```cmd
pip install dnspython
pip install numpy
pip install pandas
```
在DNSperf路径下运行。
```cmd
python DNSperf.py
```