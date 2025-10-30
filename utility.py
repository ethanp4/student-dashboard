from typing import Union
from course import Course
from user import User, Role
from assignment import Assignment
from datetime import date
from colours import Colours
from notifications import Notification, TargetType

#admin
#create course
#

#admins only
def create_course(calling_user: User) -> Union[bool, Course]:
	if calling_user.role != Role.ADMIN:
		print(f"{Colours.RED}Access denied!{Colours.RESET}")
		return False
	title = input("Enter course title: ")
	owner_id = int(input("Enter owner id: "))
	new_course = Course(title, owner_id)

	print("Created new course!")
	print(new_course)
	return new_course

def delete_course(calling_user: User) -> bool:
	if calling_user.role != Role.ADMIN:
		print(f"{Colours.RED}Access denied!{Colours.RESET}")
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
		print(f"{Colours.RED}Access denied!{Colours.RESET}")
		return False

	course_id = int(input("Enter course id to edit: "))
	course_to_edit = Course.course_list[course_id]
	if course_to_edit.owner_id != calling_user.user_id:
		print("You do not own this course!")
		return False

	action = int(input("""What would you like to edit
1) Change title
2) Add members
3) Remove members
4) Create assignment"""))

	match action:
		case 1:
			new_title = input("Enter new title: ")
			Notification(f"Title of course {course_to_edit.title} changed to {new_title}", TargetType.ADMINS)
			course_to_edit.title = new_title
		case 2:
			ids = input("Enter new member id(s) separated by a space: ")
			new_member_ids = set(map(int, ids.split()))
			Notification(f"New members added to course {course_to_edit.title}: {', '.join(map(str, new_member_ids))}", TargetType.ADMINS)
			course_to_edit.attendees_ids.update(new_member_ids)
		case 3:
			ids = input("Enter member id(s) to remove separated by a space: ")
			remove_member_ids = set(map(int, ids.split()))
			Notification(f"Members removed from course {course_to_edit.title}: {', '.join(map(str, remove_member_ids))}", TargetType.ADMINS)
			course_to_edit.attendees_ids.difference_update(remove_member_ids)
		case 4:
			create_assignment(calling_user, course_to_edit.course_id)
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
		if len(course.assignment_ids) == 0:
			print("No assignments")
		else:
			print("Assignments:")
			for assignment_id in course.assignment_ids:
				assignment = Assignment.find_assignment_by_id(assignment_id)
				if type(assignment) is Assignment:
					submitted = " (Submitted)" if assignment.assignment_id in calling_user.submitted_assignment_ids else ""
					print(f"ID: {assignment.assignment_id} - {Colours.UNDERLINE}{assignment.title}{Colours.RESET} - Due: {assignment.due_date}{submitted}")
		print("====================")


def create_assignment(calling_user: User, course_id: int):
	if calling_user.role != Role.TEACHER and calling_user.role != Role.ADMIN:
		print(f"{Colours.RED}Access denied!{Colours.RESET}")
		return False
	course = Course.find_course_by_id(course_id)
	if type(course) is not Course:
		print("Course not found!")
		return False
	if course.owner_id != calling_user.user_id and calling_user.role != Role.ADMIN:
		print("You do not own this course!")
		return False
	
	assignment_title = input("Enter assignment title: ")
	while True:
		try:
			due_date_str = input("Enter due date (YYYY-MM-DD): ")
			due_date = date.fromisoformat(due_date_str)
			break
		except ValueError:
			print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

	new_assignment = Assignment(assignment_title, due_date, course_id)
	print("Created new assignment!")
	print(new_assignment)
	return new_assignment

def get_assignments_for_user(calling_user: User) -> list[Assignment]:
	assignments: list[Assignment] = []
	match calling_user.role:
		case Role.ADMIN:
			assignments = Assignment.assignment_list
		case Role.TEACHER:
			courses = Course.find_courses_by_owner_id(calling_user.user_id)
			for course in courses:
				assignments.extend(Assignment.find_assignments_by_course_id(course.course_id))
		case Role.STUDENT:
			courses = Course.find_courses_by_attendee_id(calling_user.user_id)
			for course in courses:
				assignments.extend(Assignment.find_assignments_by_course_id(course.course_id))
	return assignments

def view_schedule(calling_user: User):
	assignments = get_assignments_for_user(calling_user)
	if len(assignments) == 0:
		print("No assignments found!")
		return
	assignments.sort(key=lambda x: x.due_date, reverse=True)
	print("Due dates visible for you: ")
	for assignment in assignments:
		print(f"{Colours.BOLD}===================={Colours.RESET}")
		print(assignment)
		if calling_user.role == Role.STUDENT:
			print_submission_status_text(assignment, calling_user)

def print_submission_status_text(assignment: Assignment, calling_user: User):
	if assignment.assignment_id in calling_user.submitted_assignment_ids:
		print(f"{Colours.GREEN}Assignment is submitted!{Colours.RESET}")
	else:
		print(f"{Colours.RED}Assignment is not submitted!{Colours.RESET}")

def submit_assignment(calling_user: User):
	if calling_user.role != Role.STUDENT:
		print(f"{Colours.RED}Access denied!{Colours.RESET}")
		return False
	
	assignment_id = int(input("Enter assignment id to submit: "))
	assignment = Assignment.find_assignment_by_id(assignment_id)
	if type(assignment) is not Assignment:
		return False
	
	course = Course.find_course_by_id(assignment.course_id)
	if type(course) is not Course:
		print("Course not found!")
		return False
	if calling_user.user_id not in course.attendees_ids:
		print("You are not enrolled in the course for this assignment!")
		return False

	if calling_user.submit_assignment(assignment_id):
		print("Assignment submitted successfully!")
		return True
	else:
		return False
	
	