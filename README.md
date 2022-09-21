# RFID Website for Granting and Logging Access
This python project is used in combination with a microprocessor connected to an RFID scanner, creating a website that will provide an interface for users with two functionalities:
- Logging which RFID cards were scanned on the RFID scanner, which time it was done, and whether access was granted.
- Insert the names and RFID of users that can be granted access when scanning their cards on the RFID scanner. 
 
## Installation and Execution
This python program was created through Windows 10 Visual Studio Code using __Python 3.10.7 64-bit__ from the Microsoft Store and the __Python__ extension from Microsoft.

Installing the code was done using PowerShell and the command:
```powershell
git clone https://github.com/cmmira/RFID_Web.git
```

A virtual environment was created for this python project along with the required packages using the Command Prompt:
```commandprompt
> cd <RFID_Web File Location> 
> py -3 -m venv venvRFID
> venvRFID\Scripts\activate.bat
(venvRFID) > pip install -r requirements.txt
```

Running the code first required the creation of the database and then execution using Command Prompt:
```commandprompt
> python3
>>> from RFID_Web import db
>>> db.create_all()
>>> exit()
> python3 RFID.py
```

## Webpages
This program uses application routing with each one generating an HTTP template and changing according to the button pressed for an interactive website. There is also one web page route meant to only serve the microprocessor.

### Home Page Route  _‘/’_
This web page divides the functionality of the program using two buttons which each one redirects the website to the desired functionality.
- The left button redirects the webpage to modify the names and RFID that will be granted access when scanning their cards on the RFID scanner.
- The right button redirects the webpage to look at the logs of RFID cards that were scanned on the RFID scanner.

### Route  _‘/users’_
On this web page a table will show which RFIDs have authorized access and the name connected to the RFID. There are also buttons on the table that can update or delete the names and RFIDs. Below the table are text boxes of which new RFIDs can be given authorized access and which name will be connected to that RFID. There is also a button below to return to the home page.  

### Route  _‘/log’_
On this web page the logs are shown in the structure of a table with a button to go back to the main home page. 
- The first column shows the name connected to the RFID scanned but if it is unknown then “Unknown” is shown.
- The second column shows the RFID scanned on the RFID scanner.
- The third column shows the time that the RFID card was scanned on the RFID scanner.
- The fourth column shows whether the RFID scanned was granted access or if it was denied access.

### Route  _‘/check’_
This application routing section of the python code is meant to be used with the microprocessor connected to an RFID scanner. Taking in a JSON object from the microprocessor and using the RFID number given to log whether the RFID was granted access or denied and the time it was swiped on the RFID scanner.
- This project was a collaborative effort, in which another group member handled the assembly of the microprocessor and the setup with the JSON object needed for logging activities.
- The initial setup for this section of the application routing was first tested by inserting the RFID through the URL such as, “/check/<int:i>”.

### Route  _‘/delete/<int:id>’_
This application routing section of the python code does not have its own web page and instead uses the information from the authorized access table to select which RFID and name will be deleted from the corresponding database. Since the authorized access table is ordered by rows, each row has a corresponding row ID number in the database which is used with the application routing alongside _’/delete/<Row ID>’_ as shown. 

### Route  _‘/update/<int:id>’_
On this web page the application routing uses the row on the authorized access table of which the update button was pressed since each row on the table has its own update button. The update web page itself provides an interface in which the user can change the name and RFID, committing the changes into the database using the button next to the rightmost text box.

