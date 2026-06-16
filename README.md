# **ATC Advisor**



**A VATSIM ATC proximity notification tool for Microsoft Flight Simulator.**

**Reads your real position via SimConnect, finds the nearest active controller and alerts you on PC and mobile via ntfy.**



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **Features:**



* **Reads your real position from MSFS via SimConnect;;**



* **Fetches live ATC data from VATSIM;**



* **Calculates distance to the nearest active controller (in nautical miles);**



* **Alerts via Windows notification and ntfy (PC and mobile);**



* Configurable alert distance (10–200 NM);



* Auto-refresh (30s, 60s, 120s or Off);



* Supports 14 languages (Arabic, Chinese, Dutch, English, French, German, Hindi, Italian, Japanese, Korean, Portuguese, Russian, Spanish and Turkish);



* Light and Dark theme.





\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **Requirements:**



* Windows 10/11 (64-bit);



* Microsoft Flight Simulator 2020/2024;



* Python 3.11+ (only if you choose to use the .py files instead of the .exe.)



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **Installation:**



###### **From github.com:**





1. Go to https://github.com/JohnnyRochaSoares/ATC-Advisor/releases;
2. Download the latest .exe ZIP;
3. Extract the ZIP folder;
4. Run it.





###### **From Git:**



1. Open CMD on your PC;
2. Type the following commands:



```bash
git clone https://github.com/JohnnyRochaSoares/ATC-Advisor.git
cd ATC-Advisor
pip install -r requirements.txt
cd src
python main.py
```



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **Project Structure:**



```
ATC Advisor/

├── LICENSE

├── README.md

├── requirements.txt

├── assets/

│   └── ATC Advisor.ico

└── src/

   └── main.py

   ├── core/

   │   ├── distance.py
       ├── logic.py
   │   ├── position.py
       └── settings.py
   │

   ├── integrations/

   │   ├── airports.py

   │   └── vatsim.py

   └── ui/


&#x20;      ├── app.py



&#x20;      └── languages.py

```

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **License:**



##### **Copyright (c) 2026 João Rocha Soares**



##### **All rights reserved.**



This code and all its contents are the intellectual property of João Rocha Soares.

Users may run, use and modify this code exclusively for personal purposes.

It is strictly prohibited to distribute, sell or publish this code, or any modified

version, without prior written permission from the author.



To request permission, contact the author via Email, GitHub or Instagram.



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_





### **Contacts:**

######  		│

######           	├─ Email: \[joao.rocha.soares.13.pt@gmail.com]

######  	  	│

######         	├─ GitHub: \[JohnnyRochaSoares]

######  		│

######         	├─ Instagram: \[@johnny\_rocha\_soares]

######  	  	│

