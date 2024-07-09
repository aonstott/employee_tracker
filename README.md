# Employee Tracker
This program is designed to help automate the process of adding and removing employees from teams.  The following instructions are also on knowledge base in GLPI:

# Categories Explanation:
<b>Confirmed to Delete:</b> The program found these employees exact names in teams, and it confirmed that they have been removed from active directory.  They should be safe to remove from MS teams.

<b>Unconfirmed to Delete:</b> These employees' names were found in teams, but they still have a company listed in active directory.  The program only checks for any company, not neccessarily print and mail.  This is because the company listed is usually a more specific subdivision, and adding every single one would be difficult.  Manually check AD to confirm the employee isn't listed as a PM employee.



# Intro
As of May 2024, I (Aaron) am managing adding and removing employees from Microsoft Teams when they enter or leave the department.  I have created some tools to make the process easier, so hopefully whoever takes this responsibility over next has everything set up to do it efficiently.  

The basic idea is that employees must be removed from Teams when they stop working at the department in order to maintain security.  New employees should be added so they receive announcements from the department.  

 

# Spreadsheets
Every month, Roma sends an email to the comp support inbox with an excel file containing info on the current employees in the department.  This spreadsheet contains lots of info, but the most important fields are Name, ID Number, and Net ID.  In order to find employees that need to be removed or added to teams, we can look at the difference between the current month's spreadsheet and last month's.  

 

# Employee Tracker Program
To make this process mostly automated, I have created a python program that determines which employees need to be removed or added.  

# Installation
The program can be found at: this github repo. The repository contains no employee data, you will have to obtain the files yourselves and add them to the folder when you run the program.  

In order to install the program, open up a terminal and navigate to the directory you would like to install the program in.  Then, at the terminal, run the command:

git clone https://github.com/aonstott/employee_tracker

# Setup
In file explorer, find the employee_tracker folder that should have been created by running the previous command.  Put the excel files for last months employees and this months employees into this folder.  Next, create a new file called "teams.txt" in the same folder.

(note: this next part is a little janky but it works.  I couldn't get access to the Teams API because I don't have the admin permissions required.  If you know how to program in python and want to try to get API access for Microsoft Graphs API, you could make this part a lot better.)

Next, you need to go to the Production Services Team, click the 3 dots in the corner, and select manage team.  From here, highlight all the information for the members as shown in the picture attached to this article.  Paste it into the teams.txt file you created.  It will look weird, but I have set it up to automatically filter the data into a usable form. 

![teamsimg](<Screenshot 2024-05-09 140410.png>)

# Run the Program
To run the program, open a terminal and navigate to the employee_manager folder.  Run the following command:

python3 ./main.py "old_file" "new_file"

replace old_file and new_file with the names of the excel files, making sure to keep them in double quotes.  This command should generate a file named TeamsUpdates.txt that will tell you who to add and remove from teams.  

