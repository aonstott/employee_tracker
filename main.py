import pandas as pd

def run(old_file:str, new_file:str):
    old_data:pd.DataFrame = pd.read_excel(old_file)
    new_data:pd.DataFrame = pd.read_excel(new_file)
    departed_employee_ids:set = set()
    new_employee_ids:set = set()
    departed_employee_ids, new_employee_ids = get_diffs(old_data, new_data)
    employees_to_delete = get_employee_data(departed_employee_ids, old_data)
    employees_to_add = get_employee_data(new_employee_ids, new_data)
    print("Departed Employees: ")
    for employee in employees_to_delete:
        print_employee_info(employee)
        print("\n")
    print("New Employees: ")
    for employee in employees_to_add:
        print_employee_info(employee)
        print("\n")


def get_diffs(old_data, new_data):
    old_ids_list:list = old_data['Empl ID']
    new_ids_list:list = new_data['Empl ID']
    old_ids:set = set(old_ids_list)
    new_ids:set = set(new_ids_list)
    departed_employee_ids:set = old_ids - new_ids
    new_employee_ids:set = new_ids - old_ids
    return departed_employee_ids, new_employee_ids

def get_employee_data(id_nums:set, data:pd.DataFrame):
    employee_data:list = []
    complete_data = {}
    for index, employee in data.iterrows():
        if employee['Empl ID'] in id_nums:
            employee_data.append(employee)

    return employee_data

def print_employee_info(employee):
    print("Empl ID: ", employee["Empl ID"])
    print("Net ID: ", employee["Net ID"])
    print("Name: ", employee["First Name"], employee["Last Name"])
    


run("Copy of Employee Report 3-5-24.xlsx", "Employee List 5-1-2024.xls")
