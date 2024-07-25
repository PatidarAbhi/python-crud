

class Person:
    def __init__(self, name, person_id):
        self.id = person_id
        self.name = name

    def display(self):
        print(self.name)
        print(self.id)

    def details(self):
        print("My name is {}".format(self.name))
        print("id: {}".format(self.id))




