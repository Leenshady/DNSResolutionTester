# DNSperf
- [English](README.md) | [中文](README_ZH.md)  

DNSperf is a tool for testing the performance of DNS servers in resolving A records, which can help you choose the most suitable DNS for your local network.

## Develop Environment
- Python 3.12.3  

Yon can download from https://www.python.org/.
## Dependent Libraries
- dnspython
- numpy
- pandas
- requests

Run the this code in bash (Linux) or cmd (Windows) to install dependency libraries.
```cmd
pip install dnspython
pip install numpy
pip install pandas
pip install requests
```
## Configure
You can add domain name that you want to test the DNS in domain_names.json.
```json
[
    "www.github.com",
    "www.baidu.com"
]
```
You can add DNS server that you want to test in dns_server.json.
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

## Run
Run the source code.
```cmd
python DNSperf.py
```
Run the source code and output the test results to result.log.
```cmd
python DNSperf.py --log result
```
Run DNSperf on the Windows system and output the test results to result.log.
```cmd
DNSperf.exe --log result
```

## DNS Support
- [x] Support DNS（IP Address）
- [x] Support DNS over HTTPS (RFC 8484, supports GET and POST)
- [ ] Support DNS over HTTPS (JSON API, supports GET)
- [ ] Support DNS over TLS
- [ ] Add circuit breaker function, end the DNS test directly if there is no response after multiple resolutions, to avoid waiting for too long
- [ ] Optimize DNS testing algorithm to avoid triggering QoS

## Reminder
Due to some public DNS adopting QoS policies, the test results may be inaccurate.