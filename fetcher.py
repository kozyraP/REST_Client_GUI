import json
import urllib.request
import tkinter as tk
import requests
from tkinter import messagebox


class App:
    API_ROOT = "https://flask-rest-api-crud-app.herokuapp.com"

    # API_ROOT = "http://localhost:5000"

    def __init__(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.grid()
        self.create_main_view()
        self.root.mainloop()

    def create_main_view(self):
        self.clear_screen()
        tk.Button(self.frame, text='Get all employees', command=self.get_all).grid(row=0, column=0)
        tk.Button(self.frame, text='Get employee by ID', command=self.get_by_id).grid(row=1, column=0)
        tk.Button(self.frame, text='Add employee', command=self.post_employee).grid(row=2, column=0)
        tk.Button(self.frame, text='Update employee', command=self.put_employee).grid(row=3, column=0)
        tk.Button(self.frame, text='Delete employee', command=self.delete_employee).grid(row=4, column=0)

    def get_all(self):
        self.clear_screen()
        self.create_table()
        row_num = 1
        with urllib.request.urlopen("https://flask-rest-api-crud-app.herokuapp.com/api/employees") as url:
            data = json.loads(url.read().decode())
            for item in data:
                tk.Label(self.frame, text=str(item['id'])).grid(row=row_num, column=0)
                tk.Label(self.frame, text=str(item['name'])).grid(row=row_num, column=1)
                tk.Label(self.frame, text=str(item['birth_day'])).grid(row=row_num, column=2)
                tk.Label(self.frame, text=str(item['email'])).grid(row=row_num, column=3)
                tk.Label(self.frame, text=str(item['phone_number'])).grid(row=row_num, column=4)
                row_num += 1

        tk.Button(self.frame, text='Back', command=self.create_main_view).grid(row=row_num)

    def get_by_id(self):
        self.clear_screen()

        def load_employee_data():
            rowid = id_field.get()
            self.clear_screen()
            self.create_table()
            with urllib.request.urlopen(self.API_ROOT + f"/api/employees/{rowid}") as url:
                data = json.loads(url.read().decode())
                row_num = 1
                for item in data:
                    tk.Label(self.frame, text=str(item['id'])).grid(row=row_num, column=0)
                    tk.Label(self.frame, text=str(item['name'])).grid(row=row_num, column=1)
                    tk.Label(self.frame, text=str(item['birth_day'])).grid(row=row_num, column=2)
                    tk.Label(self.frame, text=str(item['email'])).grid(row=row_num, column=3)
                    tk.Label(self.frame, text=str(item['phone_number'])).grid(row=row_num, column=4)
                    row_num += 1
            tk.Button(self.frame, text='Back', command=self.create_main_view).grid(row=row_num)

        self.clear_screen()
        tk.Label(self.frame, text=str('ID')).grid(row=0, column=0)
        id_field = tk.Entry(self.frame)
        id_field.grid(row=0, column=1)
        tk.Button(self.frame,
                  text='Load user',
                  command=load_employee_data).grid(row=1, column=0)

    def post_employee(self):
        def create_employee():
            url = self.API_ROOT + "/api/employees"
            employee_json = {'name': f'{name_field.get()}',
                             'birth_day': f'{birth_day_field.get()}',
                             'email': f'{email_field.get()}',
                             'phone_number': f'{phone_number_field.get()}'}
            try:
                x = requests.post(url, json=employee_json)
                print(x.text)
                messagebox.showinfo("New employee info", f"Employee was added correctly")
            except requests.exceptions.RequestException as e:
                print('error:', e)
                messagebox.showinfo("New employee info", f"Can not add employee, please try again!")
            finally:
                self.create_main_view()

        self.clear_screen()
        tk.Label(self.frame, text='name').grid(row=0, column=0)
        tk.Label(self.frame, text='birth_day').grid(row=1, column=0)
        tk.Label(self.frame, text='email').grid(row=2, column=0)
        tk.Label(self.frame, text='phone_number').grid(row=3, column=0)
        name_field = tk.Entry(self.frame)
        name_field.grid(row=0, column=1)
        birth_day_field = tk.Entry(self.frame)
        birth_day_field.grid(row=1, column=1)
        email_field = tk.Entry(self.frame)
        email_field.grid(row=2, column=1)
        phone_number_field = tk.Entry(self.frame)
        phone_number_field.grid(row=3, column=1)
        tk.Button(self.frame,
                  text='Create employee',
                  command=create_employee).grid(row=4, column=1)

    def put_employee(self):

        def load_employee_data():
            def update_employee():
                api_url = self.API_ROOT + f"/api/employees/{rowid}"
                employee_json = {'name': f'{name_field.get()}',
                                 'birth_day': f'{birth_day_field.get()}',
                                 'email': f'{email_field.get()}',
                                 'phone_number': f'{phone_number_field.get()}'}
                try:
                    x = requests.put(api_url, json=employee_json)
                    print(x.text)
                    messagebox.showinfo("New employee info", f"Employee was update correctly")
                except requests.exceptions.RequestException as e:
                    print('error:', e)
                    messagebox.showinfo("New employee info", f"Can not update employee, please try again!")
                finally:
                    self.create_main_view()

            rowid = id_field.get()
            with urllib.request.urlopen(self.API_ROOT + f"/api/employees/{rowid}") as url:
                all_data = json.loads(url.read().decode())
                if len(all_data) < 1:
                    messagebox.showinfo("New employee info", f"Employee with id: {rowid} not exist")
                    self.create_main_view()
                else:
                    data = all_data[0]
                    self.clear_screen()
                    tk.Label(self.frame, text='name').grid(row=0, column=0)
                    tk.Label(self.frame, text='birth_day').grid(row=1, column=0)
                    tk.Label(self.frame, text='email').grid(row=2, column=0)
                    tk.Label(self.frame, text='phone_number').grid(row=3, column=0)
                    name_field = tk.Entry(self.frame)
                    name_field.insert(0, data['name'])
                    name_field.grid(row=0, column=1)
                    birth_day_field = tk.Entry(self.frame)
                    birth_day_field.insert(0, data['birth_day'])
                    birth_day_field.grid(row=1, column=1)
                    email_field = tk.Entry(self.frame)
                    email_field.insert(0, data['email'])
                    email_field.grid(row=2, column=1)
                    phone_number_field = tk.Entry(self.frame)
                    phone_number_field.insert(0, data['phone_number'])
                    phone_number_field.grid(row=3, column=1)
                    tk.Button(self.frame,
                              text='Back',
                              command=self.create_main_view).grid(row=4, column=0)
                    tk.Button(self.frame,
                              text='Update employee',
                              command=update_employee).grid(row=4, column=1)

        self.clear_screen()
        tk.Label(self.frame, text=str('ID')).grid(row=0, column=0)
        id_field = tk.Entry(self.frame)
        id_field.grid(row=0, column=1)
        tk.Button(self.frame,
                  text='Load user',
                  command=load_employee_data).grid(row=1, column=0)

    def delete_employee(self):
        def delete_by_id():
            api_url = self.API_ROOT + f"/api/employees/{id_field.get()}"
            try:
                x = requests.delete(api_url)
                print(x.text)
                messagebox.showinfo("New employee info", f"Employee was deleted correctly")
            except requests.exceptions.RequestException as e:
                print('error:', e)
                messagebox.showinfo("New employee info", f"Can not delete employee, please try again!")
            finally:
                self.create_main_view()

        self.clear_screen()
        tk.Label(self.frame, text=str('ID')).grid(row=0, column=0)
        id_field = tk.Entry(self.frame)
        id_field.grid(row=0, column=1)
        tk.Button(self.frame,
                  text='Delete user',
                  command=delete_by_id).grid(row=1, column=0)

    def clear_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_table(self):
        tk.Label(self.frame, text='id').grid(row=0, column=0)
        tk.Label(self.frame, text='name').grid(row=0, column=1)
        tk.Label(self.frame, text='birth_day').grid(row=0, column=2)
        tk.Label(self.frame, text='email').grid(row=0, column=3)
        tk.Label(self.frame, text='phone_number').grid(row=0, column=4)


def main():
    app = App()


main()
