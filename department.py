departments = []

class Department:
    def __init__(self, name, members):
        self.name = name
        if members.__class__ == list:
            self.members = members
        else:
            self.members = [members]
        departments.append(self)