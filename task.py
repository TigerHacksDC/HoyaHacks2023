from department import Department

tasks_list = []


class Task:
    def __init__(self, name, description, department):
        self.name = name
        self.description = description
        if department.__class__ == Department:
            self.department = department
        else:
            self.department = Department(department, [])
        tasks_list.append(self)
