# Project Bongo

## Requirements
 - You must be on windows 10 or 11
 - You must have Google Chrome
 - It is highly recommended that you have an intel processor newer than or equal to the haswell series. (Ignore this if your computer was made within the past decade)
 - Set the sleep timer to Never sleep on your computer.
 - Only connect 1 monitor. (If you have multiple, it still works but requires additional setup.)


If this is your first time setup, please skip to 
- [Setup](#setup)

## Instructions
1. Expand the cache folder. Click on siteListTodo.json (this file can be opened with notepad). 
2. Change the numbers to the times you wish to collect from a site. the abbreviation key is listed in the file keys.md in the same folder (cache).
3. Save and close siteListTodo.json.
4. Run client.exe as admin. (Right mouse click, run as admin. If you get a prompt saying windows does not recognize this file, __more info__, then click run anyway. Then Click yes to the administrator prompt)
5. Wait for the prompt to say OCR Server started. Press enter until chrome opens. 

This should run until complete. 
If any errors occur, please contact me and record the error log either through a screenshot or a copy paste of the message. 

## FAQ
- Why does my program enter the chrome welcome page so much?
 - When the program is running and is idle (waiting for the next time to collect code) chrome will default back to the chrome welcome page. This is expected behavior.
- How do I stop the program?
 - Wait for the program to stop running and you return to the chrome welcome page. You have at least 20 seconds to close the program during this time. 
 Press the windows key. Click on the window where the exe is running in your taskbar. (it should be a window with white text on a black background.)
 Click into the window. Press Ctrl + c. 
 - If you need to stop it mid solve, try using alt+tab. When you are on the correct window, press Ctrl + c


## Accessing collected data
1. Open the folder labeled "codes"
2. The latest session's data should be in the most recent folder. 



## Setup

1. Click 'Releases' on the right side. Download the latest version release's 'Source Code' as a .zip (NOT TO YOUR DESKTOP) and extract the contents.   
1. Run setup.exe as administrator type your usename and API Key that is provided by myself. (Right mouse click, run as admin. If you get a prompt saying windows does not recognize this file, __more info__, then click run anyway. Then Click yes to the administrator prompt) 
2. Run setup.exe again as administrator AGAIN. Wait for the screen to clear and prompts you to enter your Username and API key. 
3. Create accounts for each site you wish. **DO NOT USE THE GOOGLE OPTION**. Use the native log in when signing up. Using a gmail is okay for this. 
4. (Optional but highly recommended) Create a burner Google account. This will be used to store your passwords on chrome. 
5. Run the startChrome.exe as admininstrator by right clicking and selecting "run as administrator" and clicking Yes to the prompt. Log into Chrome with your burner Google account from the prior step. 
6. Log into each website you have created an account for and **SAVE THE PASSWORDS TO CHROME**. The program will try to use these to log in when you are logged out for any reason.
7. Close the chrome window. Reopen startChrome.exe and see if your passwords have been saved. 
8. Navigate to [https://clickspeedtest.com/scroll-test.html](https://clickspeedtest.com/scroll-test.html). Use your scroll wheel and scroll down ONCE. Record the number into the file ./settings/mainSettings.json (the file can be opened with notepad). replace the value 133 with your recorded value (it may be 133 in which case leave it alone). 
9. Save and close the file.
10. Close all chrome instances opened through this app.


Your setup is now complete. Return to [instructions](#instructions).

## How to make your computer never sleep
