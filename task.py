from department import Department

tasks = []


def getTasks():
    return tasks


class Task:
    def __init__(self, name, description, department):
        self.name = name
        self.description = description
        if department.__class__ == Department:
            self.department = department
        else:
            self.department = Department(department, [])
        tasks.append(self)
