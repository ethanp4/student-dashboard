from typing import Union
from course import Course
from user import User, Role

#admins only
def create_course(calling_user: User) -> Union[bool, Course]:
	if calling_user.role != Role.ADMIN:
		print("Access denied!")
		return False
	title = input("Enter course title: ")
	desc = input("Enter course description: ")
	new_course = Course(title, desc, calling_user.user_id)
	Course.course_list.append(new_course)
	print("Created new course!")
	print(new_course)
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
def edit_course_info(calling_user: User) -> Union[bool, None]:
	if calling_user.role != Role.TEACHER and calling_user.role != Role.ADMIN:
		print("Access denied!")
		return False
	while True:
		try:
			course_id = int(input("Enter course id to edit: "))
			course_to_edit = Course.course_list[course_id]
			if course_to_edit.owner_id != calling_user.user_id:
				print("You do not own this course!")
				return False
			break
		except (ValueError, IndexError):
			print("Invalid course id, try again")
	new_title = input("Enter new title: ")
	new_desc = input("Enter new description: ")
	course_to_edit.title = new_title
	course_to_edit.desc = new_desc
	print("Course information updated successfully!")