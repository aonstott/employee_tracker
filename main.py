import pandas as pd

def run(old_file:str, new_file:str):
    old_data:pd.DataFrame = pd.read_excel(old_file)
    new_data:pd.DataFrame = pd.read_excel(new_file)
    departed_employee_ids:set = set()
    new_employee_ids:set = set()
    departed_employee_ids, new_employee_ids = get_diffs(old_data, new_data)
    print("Departed Employees: ", get_net_ids(departed_employee_ids, old_data))
    print("New Employees: ", get_net_ids(new_employee_ids, new_data))


def get_diffs(old_data, new_data):
    old_ids_list:list = old_data['Empl ID']
    new_ids_list:list = new_data['Empl ID']
    old_ids:set = set(old_ids_list)
    new_ids:set = set(new_ids_list)
    departed_employee_ids:set = old_ids - new_ids
    new_employee_ids:set = new_ids - old_ids
    return departed_employee_ids, new_employee_ids

def get_net_ids(id_nums:set, data:pd.DataFrame):
    net_ids:set = set()
    for index, employee in data.iterrows():
        if employee['Empl ID'] in id_nums:
            net_ids.add(employee['Net ID'])

    return net_ids
    


run("Copy of Employee Report 3-5-24.xlsx", "Employee List 5-1-2024.xls")
