# Employee Tracker
This program is designed to help automate the process of adding and removing employees from teams.  The following instructions are also on knowledge base in GLPI:

# Categories Explanation:
<em> This is an explanation of the categories in the output "TeamsUpdates.txt" file.  If you haven't yet installed or used the program skip to intro section.  This part is at the top because I am guessing it will be used a lot for reference. <br>
Note: I am considering changing the program to check emails instead of names in Teams, in which case these will change.</em>
<br><br>
<b>Confirmed to Delete:</b> The program found these employees' exact names in teams, and it confirmed that they have been removed from active directory.  They should be safe to remove from MS teams.

<b>Unconfirmed to Delete:</b> These employees' names were found in teams, but they still have a company listed in active directory.  The program only checks for any company, not neccessarily print and mail.  This is because the company listed is usually a more specific subdivision, and adding every single one would be difficult.  Manually check AD to confirm the employee isn't listed as a PM employee.

<b>Check manually to determine removal:</b> The program did not find these employees' exact names in Teams, but found their last name.  This could mean they are using a nickname in Teams, or that they are not in teams but there is someone else with the same last name.  Check teams manually using netid, and if the departed employee is still in teams, delete them.

<b>Confirmed to Add:</b> The program did not find these employees' names in teams, and it confirmed that they have been added to active directory.  They should be safe to add to MS teams.

<b>Unconfirmed to Add:</b> These employees' names were not found in teams, but they do not have a company listed in active directory.  It's possible they just haven't been added to the AD group yet and will be later.  Check these ones against the spreadsheet just to be sure.

<b>Check manually to determine Addition:</b> The program found these employees' last names in teams, but not an exact match.  This could be because the new employee is in teams but is using a nickname, or they are not in Teams but someone else has the same last name.  Check Teams manually, and if the new employee is not in Teams add them. 



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

```git clone https://github.com/aonstott/employee_tracker```

# Setup
In file explorer, find the employee_tracker folder that should have been created by running the previous command.  Put the excel files for last months employees and this months employees into this folder.  <s>Next, create a new file called "teams.txt" in the same folder.</s>


<em>I found a new way to get names from teams.  I left the documentation for the old method should it ever be needed, but it really doesn't work very well so use it as a last resort.  Stuff for the old method is all struck through.  New method is much easier; only a few commands from the terminal are needed:  </em>

1. Run these commands separately from a powershell with admin privileges:

```
Install-Module -Name PowerShellGet -Force -AllowClobber
Install-Module -Name MicrosoftTeams -Force -AllowClobber
Import-Module MicrosoftTeams
```
2. Check that teams module was installed:

```
Get-Module -ListAvailable
```

3. Run the following and login to Teams:
```
Connect-MicrosoftTeams
```
4. Get the GroupID of the group in Teams.  Easiest way to do this is to open Teams, go to the channel, and click the three dots at the top right and select get link to channel: ![teamsimg](<groupid1.png>) The GroupID is part of the query string, should look like this: ![teamsimg](<groupid2.png>) Make sure to highlight everything between the "=" and "&" characters.  That is the GroupID you will substitute into the next command.



5. Run this command to output a list of all teams members in the group.
```
Get-TeamUser -GroupId <GroupID>
```

Output should look like this:
![teamsimg](<teamsoutput.png>)


<br><s>(note: this next part is a little janky but it works.  I couldn't get access to the Teams API because I don't have the admin permissions required.  If you know how to program in python and want to try to get API access for Microsoft Graphs API, you could make this part a lot better.)

Next, you need to go to the Production Services Team, click the 3 dots in the corner, and select manage team.  From here, highlight all the information for the members as shown in the picture attached to this article.  Paste it into the teams.txt file you created.  It will look weird, but I have set it up to automatically filter the data into a usable form. 

![teamsimg](<Screenshot 2024-05-09 140410.png>)</s>

<em> Note: there is potential for furhter automation here.  The Microsoft Graph API allows you to perform actions on Teams with API calls, which may allow for automatic addition and removal of employees.  Requires admin access, and could potentially go very wrong if not implemented correctly.  But theoretically would save time.</em>  

6. Now that you have your shell set up to get Teams members, use this command to create the file the program will use.  If you create the file outside the employee_tracker directory, you will need to move it afterwards so the program can access it. The command is saving the same output you saw from the last step into a file called teams_members.csv, and converting it into csv format with commas separating each field. 
```
Get-TeamUser -GroupId b95554be-772f-4e4e-834f-138c81c113ca |
    ConvertTo-Csv -NoTypeInformation |
    Out-File -FilePath "teams_members.csv" -Encoding utf8
``` 


# Run the Program
To run the program, open a terminal and navigate to the employee_manager folder.  Run the following command:

python3 ./main.py "old_file" "new_file"

replace old_file and new_file with the names of the excel files, making sure to keep them in double quotes.  This command should generate a file named TeamsUpdates.txt that will tell you who to add and remove from teams.  

