***** 光達YDLiDAR連接 *****
1. 執行python3 usb_tool.py查找使用中的usb埠 (正常是"/dev/ttyUSBx" x = port)
2. 打開cmd並執行命令 -> sudo chmod 777 /dev/ttyUSBx
3. 若有不同請更改scan.py中YDLiDAR的port和address

***** Arduino和自轉馬達連接 *****
1. 打開Arduino.exe並將file->example->Firmata->StandardFirmata.ino上傳至Arduino中
2. 執行python3 usb_tool.py查找使用中的usb埠 (正常是"/dev/ttyACMx" x = port)
3. 打開cmd並執行命令 -> sudo chmod 777 /dev/ttyACMx
4. 將自轉馬達以彩虹線連至Arduino: 5V->紅線, GND->灰線, port 9(可更改)->橘線
5. 若有不同請更改scan.py中Arduino的port和address

***** Host <-> Client設定 *****
1. server.py和scan.py內包含聯絡host<->client的socket以及其使用的ip和port
2. ip若是在同一個網域內就改成127.0.0.1 並把port改8888
3. 若不是則要把ip改成server端的ip，port則要先輸入指令>$ netstat -lat查找空閒的port執行
4. 找一個tcp且Listen的可用port並在scan.py中更改

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
***** 程式執行 *****
1. iesl workstation執行server.py
>$ python server.py(要先執行)

2. 接著在Jetson Nano上執行
>$ python3 scan.py

