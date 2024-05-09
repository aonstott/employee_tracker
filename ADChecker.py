import subprocess


class ADChecker:
    def check(self, username:str):
        command = f"dsquery user -samid {username} | dsget user -company"
        result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
        return result.stdout.decode('utf-8').strip()
    
    def get_company(self, output:str):
        return output.split('\n')[1].strip()
    

    def company_exists(self, company:str):
        return company != ""
