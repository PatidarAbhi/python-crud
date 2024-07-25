from fastapi import FastAPI
from controllers import (
    user_controller,
    post_controller,
    project_controller,
    team_controller,
    person_controller,
    passport_controller
)
from database.db_connection import create_tables
from exceptions.not_found_exception import NotFoundException
from exceptions.global_exception_handler import not_found_exception_handler
from inheritence.employee import Employee
from polymorphism.bird import Bird, Sparrow, Ostrich


create_tables()

app = FastAPI()

app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.include_router(user_controller.router, prefix="/api")
app.include_router(post_controller.router, prefix="/api")
app.include_router(project_controller.router, prefix="/api")
app.include_router(team_controller.router, prefix="/api")
app.include_router(project_controller.router, prefix="/api")
app.include_router(person_controller.router, prefix="/api")
app.include_router(passport_controller.router, prefix="/api")

#
# a = Employee("Abhi", 1, 150.00, "SDE")
# a.details()
# a.display()
# #
# bird = Bird()
# bird.intro()
# bird.fly()
#
# spr = Sparrow()
# spr.fly()
#
# ost = Ostrich()
# ost.fly()
# ost.intro()
