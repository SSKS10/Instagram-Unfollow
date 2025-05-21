# Instagram-Unsend-Follow-Request-Using-Python
Unsend follow request sent on Instagram from downloaded meta data in the form of JSON.

If you are worried and not sure how many follow request you have sent to instagram user. There can be hundreds or thousand of such requests and unsending them is a tedious and time taking job. Here is a simple python code which you can utilise to unsend them using web scrapping.

**Pre-Requisite** -
1. Python
2. Selenium

**Steps** - 
1. Download the JSON file with follow request sent information from the user.
2. Use this link for help - https://www.wikihow.com/View-the-List-of-People-You-Have-Requested-to-Follow-on-Instagram
3. Convert zip file and download 'pending_follow_requests.json'.
4. Add username, password and downloaded file path in config file.
5. Run main.py to start the project - This will run the web scrapping to unsend all the follow request.
