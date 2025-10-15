from typing import Union
from course import Course
from user import User, Role

#admin
#create course
#

#admins only
def create_course(calling_user: User) -> Union[bool, Course]:
	if calling_user.role != Role.ADMIN:
		print("Access denied!")
		return False
	title = input("Enter course title: ")
	owner_id = int(input("Enter owner id: "))
	new_course = Course(title, owner_id)

	Course.course_list.append(new_course)
	print("Created new course!")
	print(new_course)
	return new_course

def delete_course(calling_user: User) -> bool:
	if calling_user.role != Role.ADMIN:
		print("Access denied!")
		return False
	
	course_id = int(input("Enter course id to delete: "))
	course = Course.find_course_by_id(course_id)

	if type(course) is not Course:
		return False

	Course.course_list.remove(course)
	print("Course deleted successfully!")
	return True

# instructors only
def edit_course_info(calling_user: User) -> Union[bool, None]:
	if calling_user.role != Role.TEACHER and calling_user.role != Role.ADMIN:
		print("Access denied!")
		return False

	course_id = int(input("Enter course id to edit: "))
	course_to_edit = Course.course_list[course_id]
	if course_to_edit.owner_id != calling_user.user_id:
		print("You do not own this course!")
		return False

	action = int(input("""What would you like to edit
1) Change title
2) Add members
3) Remove members"""))

	match action:
		case 1:
			new_title = input("Enter new title: ")
			course_to_edit.title = new_title
		case 2:
			ids = input("Enter new member id(s) separated by a space: ")
			new_member_ids = set(map(int, ids.split()))
			course_to_edit.attendees_ids.update(new_member_ids)
		case 3:
			ids = input("Enter member id(s) to remove separated by a space: ")
			remove_member_ids = set(map(int, ids.split()))
			course_to_edit.attendees_ids.difference_update(remove_member_ids)
		case _:
			pass

	print("Course information updated successfully!")

#all types, different view for each type
def view_your_courses(calling_user: User):
	courses = []
	match calling_user.role:
		case Role.STUDENT:
			courses = Course.find_courses_by_attendee_id(calling_user.user_id)
		case Role.TEACHER:
			courses = Course.find_courses_by_owner_id(calling_user.user_id)
		case Role.ADMIN:
			courses = Course.course_list

	for course in courses:
		print(course)
		print("====================")