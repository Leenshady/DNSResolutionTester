@ECHO
set version="v0.1.1"
pyinstaller -F --upx-dir ..\..\upx-4.2.4-win64\ --add-data ..\dns_servers.json;. --add-data ..\domain_names.json;. -n DNSperf_%version%_win64 ..\DNSperf.py
pause