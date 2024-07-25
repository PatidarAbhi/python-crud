from inheritence.department import Department
from inheritence.person import Person


class Employee(Person, Department):
    def __init__(self, name, person_id, salary, post):
        Person.__init__(self, name, person_id)
        self.salary = salary
        self.post = post

    def details(self):
        print("My name is {}".format(self.name))
        print("Id: {}".format(self.id))
        print("Post: {}".format(self.post))
        print("Post: {}".format(self.salary))
