class TeamsManager:
    def __init__(self):
        self.teams = []

    def clean_teams(self, teams_file):
        remove_list = ["Profile picture", "Owner", "Member", "Name", "Title", "Location", "Tags", "Role", "("]
        with open('jobs.txt', 'r') as job_file:
            jobs = job_file.readlines()
            for job in jobs:
                remove_list.append(job.strip())
        for i in range(10):
            remove_list.append(str(i))
        #open teams file
        with open(teams_file, 'r') as file:
            teams = file.readlines()
        #remove new line characters
        teams = [team.strip() for team in teams]
        #remove all lines that start with "Profile picture"
        for phrase in remove_list:
            teams = [team for team in teams if not team.startswith(phrase)]

        #write file
        with open(teams_file, 'w') as file:
            for team in teams:
                file.write(team)
        
        with open(teams_file, 'r') as file:
            with open('cleaned_teams.txt', 'w') as cleaned_file:
                for line in file:
                    if line.strip():
                        cleaned_file.write(line)
                        cleaned_file.write("\n")
    
teams_manager = TeamsManager()
teams_manager.clean_teams('teams.txt')
