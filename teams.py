import pandas as pd

class TeamsManager:
    def __init__(self):
        self.teams = []
        self.teams_file = 'teams.txt'

    def clean_teams(self):
        remove_list = ["Profile picture", "Owner", "Member", "Name", "Title", "Location", "Tags", "Role", "("]
        with open('jobs.txt', 'r') as job_file:
            jobs = job_file.readlines()
            for job in jobs:
                remove_list.append(job.strip())
        for i in range(10):
            remove_list.append(str(i))
        #open teams file
        with open(self.teams_file, 'r') as file:
            teams = file.readlines()
        #remove new line characters
        teams = [team.strip() for team in teams]
        #remove all lines that start with "Profile picture"
        for phrase in remove_list:
            teams = [team for team in teams if not team.startswith(phrase)]
 
        #write file
        with open(self.teams_file, 'w') as file:
            for team in teams:
                if team.strip() != '' and team.strip() != ' ':
                    file.write(team + '\n')
    
    def get_names_from_csv(self):
        df = pd.read_csv('teams_members.csv')
        df = df.dropna()
        with open(self.teams_file, 'w') as file:
            for index, row in df.iterrows():
                file.write(row['Name'] + '\n')

    def get_names(self):
        with open(self.teams_file, 'r') as file:
            teams = file.readlines()
        return [team.strip() for team in teams]
        
  