from typing import Union
from course import Course
from user import User, Role

#admins only
def create_course(calling_user: User, title: str, desc: str) -> Union[PermissionError, Course]:
    if calling_user.role != Role.ADMIN:
        return PermissionError("Access denied!")
    new_course = Course(title, desc, calling_user.user_id)
    Course.course_list.append(new_course)
    return new_course

#all types, different view for each type
def view_your_courses(calling_user: User):
    match calling_user.role:
        case Role.STUDENT:
            print("view student courses")
        case Role.TEACHER:
            print("view teacher courses")
        case Role.ADMIN:
            print("view admin courses")

# instructors only
def edit_course_info(calling_user: User, course_id: int):
    print("edit course info")