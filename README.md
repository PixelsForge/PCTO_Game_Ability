# PCTO_GameAbility
## Installation BlueMuse
*Requires Windows 10 with Fall 2017 Creators Update - Version 10.0.15063 aka Windows 10 (1703).*

### First Step
Download latest version from this **<a href="https://github.com/kowalej/BlueMuse/releases">link</a>** and unzip, then follow the method below.

### Auto Install (Recommended)
Navigate to the unzipped app folder and run the **.\InstallBlueMuse.ps1** PowerShell command (right click and choose Run with PowerShell or execute from terminal directly)

Follow the prompts: 
Manual Install
    1. Double click BlueMuse_xxx.cer then click "Install Certificate".
    2. Select current user or local machine depending on preference and click "Next".
    3. Select "Place all certificates in the following store".
    4. Press "Browse...".
    5. Select install for Local Machine.
    6. Select "Trusted Root Certification Authorities" and click "OK".
    7. Click "Next" and click "Finish" to install certificate.
    8. Open Dependencies folder and appropriate folder for your machine architecture.
    9. Double click and install Microsoft.NET.Native.Framework.1.7 and Microsoft.NET.Native.Runtime.1.7.
    10. Finally, double click and install BlueMuse_xxx.appxbundle.

## SCRIPTS
If you want to do a script you have to have in the same directory the "muselsl" and import it.

## EXECUTION (only with alphabot)
After connecting the sensor to the PC, run the program through the "Client.py" file. Execution must be done by typing the command "py Client.py" on the terminal of the current folder.

## INSTRUCTION (only with alphabot)
After placing the sensor on the person's head, to control the alphabot it is essential to concentrate so that it can move forward. For lateral movements, simply tilt your head to the right or left to move in the desired direction.
