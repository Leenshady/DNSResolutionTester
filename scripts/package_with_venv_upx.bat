@ECHO
set version="v0.1.1"
call ..\myenv\Scripts\activate.bat
pip install pyinstaller
pip install dnspython
pip install pandas
pip install numpy
pip install requests
pyinstaller -F -n DNSperf_%version%_win64 ..\DNSperf.py --upx-dir ..\..\upx-4.2.4-win64\ --add-data "..\*.json;."
pause
deactivate