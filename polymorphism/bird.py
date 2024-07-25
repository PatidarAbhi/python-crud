

class Bird:

    def intro(self):
        print("There are many types of birds")


    def fly(self):
        print("Most of the birds can fly but some cannot")


class Sparrow(Bird):

    def fly(self):
        print("Sparrows can fly.")


class Ostrich(Bird):

    def fly(self):
        print("Ostriches cannot fly.")

