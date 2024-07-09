import pandas as pd
from teams import TeamsManager
from ADChecker import ADChecker
import argparse
import time

class EmployeeManager:
    def run(self, old_file:str, new_file:str):
        #save start time
        start_time = time.time()
        old_data:pd.DataFrame = pd.read_excel(old_file)
        new_data:pd.DataFrame = pd.read_excel(new_file)
        departed_employee_ids:set = set()
        new_employee_ids:set = set()

        #get employees that appear in one file but not the other
        departed_employee_ids, new_employee_ids = self.get_diffs(old_data, new_data)

        #Use the ids to get all employee data for the employees we need to add/remove
        self.employees_to_delete = self.get_employee_data(departed_employee_ids, old_data)
        self.employees_to_add = self.get_employee_data(new_employee_ids, new_data)

        teams_manager = TeamsManager()
        #Use our csv file to get the names of employees in teams
        teams_manager.get_names_from_csv()
        teams = teams_manager.get_names()

        #Check if the employees we need to add/remove are in teams
        not_found_departed, check_man_departed, to_delete = self.check_if_in_teams(self.employees_to_delete, teams)
        not_found_new, check_man_new, in_teams = self.check_if_in_teams(self.employees_to_add, teams)

        #Final categories
        confirmed_to_delete = []
        unconfirmed_to_delete = []

        uncomfirmed_to_add = []
        confirmed_to_add = []

        ad_checker = ADChecker()
        for employee in to_delete:
            result = ad_checker.check(employee["Net ID"])
            company = ad_checker.get_company(result)
            if not(ad_checker.company_exists(company)):
                #Employee is no longer in active directory, safe to delete
                confirmed_to_delete.append(employee)
            else:
                #Employee still has company lsited in active directory
                #Not necessarily our company, could be at a different department in BYU
                #Check manually if employee should be deleted
                unconfirmed_to_delete.append(employee)
        
        for employee in not_found_new:
            result = ad_checker.check(employee["Net ID"])
            company = ad_checker.get_company(result)
            if ad_checker.company_exists(company):
                #Employee is in active directory, safe to add
                confirmed_to_add.append(employee)
            else:
                #Employee is not in active directory
                #Might not have been added yet, check manually
                uncomfirmed_to_add.append(employee)


        #make file

        with open("TeamsUpdates.txt", "w") as file:
            file.write("Teams Updates\n")
            file.write("Date: " + time.strftime("%m/%d/%Y") + "\n\n")
            file.write("Departed Employees:\n")
            file.write("Confirmed to Delete (No longer in Active Directory):\n")
            for employee in confirmed_to_delete:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nUnconfirmed to Delete (Active Directory Verification Failed):\n")
            for employee in unconfirmed_to_delete:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nCheck Manually to Determine Deletion:\n")
            for employee in check_man_departed:
                file.write(employee["First Name"] + " " + employee["Last Name"] +  " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nDeparted but Not Found in Teams:\n")
            for employee in not_found_departed:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\n\n\n")


            file.write("New Employees:\n")
            file.write("Confirmed to Add (Active Directory Verification Passed):\n")
            for employee in confirmed_to_add:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nUnconfirmed to Add (Active Directory Verification Failed):\n")
            for employee in uncomfirmed_to_add:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nCheck Manually to Determine Addition:\n")
            for employee in check_man_new:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\nAlready in Teams:\n")
            for employee in in_teams:
                file.write(employee["First Name"] + " " + employee["Last Name"] + " (Net ID: " + employee['Net ID'] + ")\n")
            file.write("\n\n\n")
            file.write("Done in: " + str(time.time() - start_time) + " seconds")



    def get_diffs(self, old_data, new_data):
        old_ids_list:list = old_data['Empl ID']
        new_ids_list:list = new_data['Empl ID']
        old_ids:set = set(old_ids_list)
        new_ids:set = set(new_ids_list)
        departed_employee_ids:set = old_ids - new_ids
        new_employee_ids:set = new_ids - old_ids
        return departed_employee_ids, new_employee_ids

    def get_employee_data(self, id_nums:set, data:pd.DataFrame):
        employee_data:list = []
        complete_data = {}
        for index, employee in data.iterrows():
            if employee['Empl ID'] in id_nums:
                employee_data.append(employee)

        return employee_data
    

    def check_if_in_teams(self, employees:dict, teams_names:list):
        not_found = []
        check_manually = []
        to_change = []
        teams_last_names = [team.split()[1] for team in teams_names]
        #print("\nTeams Last Names: ", teams_last_names)
        for employee in employees:
            if str(employee["First Name"]) + " " + str(employee["Last Name"]) in teams_names:
                to_change.append(employee)
            elif (str(employee["Last Name"]) in teams_last_names):
                #we found didn't find the full name in teams but we found the last name, so we need to check manually
                check_manually.append(employee)
            else:
                #didn't find last name anywhere in teams
                not_found.append(employee)
        
        return not_found, check_manually, to_change
        

    def print_employee_info(self, employee):
        print("Empl ID: ", employee["Empl ID"])
        print("Net ID: ", employee["Net ID"])
        print("Name: ", employee["First Name"], employee["Last Name"])
    
parser = argparse.ArgumentParser(description="Employee Manager")
parser.add_argument("old_file", help="The old employee file")
parser.add_argument("new_file", help="The new employee file")
args = parser.parse_args()

employee_manager = EmployeeManager()
employee_manager.run(args.old_file, args.new_file)
