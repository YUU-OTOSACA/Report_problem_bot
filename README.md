Report Problem NC

A telegram bot for collecting data about equipment problems.
The bot sends user requests to the bot administrator, and saves them to the Google table.


The bot token, the bot administrator id, the name of the Google table where the requests are saved, the path to the json file are in the file: ...\Report_problem_bot\config\bot.ini


To launch the bot , you need to launch the Report_problem_bot shortcut on the desktop or file ...\Report_problem_bot\bot.exe .*
An internet connection is required for the bot to work


To create the bot, the python programming language and libraries were used: aiogramm, pandas, gspread, google-api-python-client, oauth2client.


Instructions for using the bot:

1. Launch the bot and do not close the window that opens.*

2. Log into Telegram to chat with the bot.

3. Enter the command "/start".

4. Use the "Report a problem" button.

5. Write your full name.

6. Describe your problem.

7. Check your message, if everything is fine, click the "Everything is fine" button, if something is wrong, click the "Change" button and repeat steps 5-7.

8. Your request has been sent to the bot administrator and saved in Google tables, if new problems occur, repeat steps 4-7.


"*" - for the computer that is the server.

Attention! To enter data about problems in the table, you need to create a service account and give him the opportunity to edit the table. More details can be found here: https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami / (section "Configuring connection in Google Api Console")
