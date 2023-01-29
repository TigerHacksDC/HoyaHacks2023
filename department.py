departments_list = []


def contains_member(member):
    for department in departments_list:
        if member in department.members:
            return True
    return False


def contains_department_name(name):
    for department in departments_list:
        if name == department.name:
            return True
    return False


class Department:
    def __init__(self, name, members):
        self.name = name
        if members.__class__ == list:
            self.members = members
        else:
            self.members = [members]
        departments_list.append(self)

