from datetime import date, timedelta
from assignment import Assignment
from course import Course
from user import User, Role
from utility import create_course, delete_course, notify_of_due_dates, submit_assignment, view_schedule, view_your_courses, edit_course_info

def authenticate_user(username: str = "", password: str = "") -> User:
	while True:
		username = input("Enter your username: ")
		password = input("Enter your password: ")

		authenticated_user = User.authenticate_user(username, password)

		if type(authenticated_user) != User:
			print("Incorrect login, try again")
		else:
			print("Correct login")
			if (authenticated_user.role != Role.ADMIN):
				notify_of_due_dates(authenticated_user, 3)
			return authenticated_user

User("a1", "pass", Role.ADMIN)
User("t1", "pass", Role.TEACHER) # id 1
User("t2", "pass", Role.TEACHER) # id 2
User("s1", "pass", Role.STUDENT)
User("s2", "pass", Role.STUDENT)
User("s3", "pass", Role.STUDENT)
User("s4", "pass", Role.STUDENT)
User("s5", "pass", Role.STUDENT)
User("s6", "pass", Role.STUDENT)

Course("Math 100", 1)
Course("Physics 100", 1)
Course("Chemistry 200", 1)
Course("Biology 200", 2)
Course("History 200", 2)
Course("English 300", 2)

today = date.today()
Assignment("Math Assignment 1", today, 0)
Assignment("Physics Assignment 1", today + timedelta(days=1), 1)
Assignment("Chemistry Assignment 1", today + timedelta(days=1), 2)
Assignment("Biology Assignment 1", today + timedelta(days=1), 3)
Assignment("History Assignment 1", today + timedelta(days=2), 4)
Assignment("English Assignment 1", today + timedelta(days=2), 5)

Assignment("Math Assignment 2", today + timedelta(days=7), 0)
Assignment("Physics Assignment 2", today + timedelta(days=8), 1)
Assignment("Chemistry Assignment 2", today + timedelta(days=8), 2)
Assignment("Biology Assignment 2", today + timedelta(days=8), 3)
Assignment("History Assignment 2", today + timedelta(days=9), 4)
Assignment("English Assignment 2", today + timedelta(days=9), 5)

Course.course_list[0].attendees_ids.update({3, 4, 5})
Course.course_list[1].attendees_ids.update({3, 4})
Course.course_list[2].attendees_ids.update({4, 5, 6})
Course.course_list[3].attendees_ids.update({5, 6})
Course.course_list[4].attendees_ids.update({3, 6})
Course.course_list[5].attendees_ids.update({3, 4, 5, 6})

authenticated_user = authenticate_user()
		
while True:
	selection = int(input("""\n0) Exit program
1) Create a new course (admin only)
2) Delete course (admin only)
3) View courses (all roles)
4) Edit course info (instructor only)
5) View user list (all roles)
6) View upcoming dates (all roles)
7) Submit assignment (students only)										 
8) Change user\n"""))

	match selection:
		case 1:
			create_course(authenticated_user)
			pass
		case 2:
			delete_course(authenticated_user)
			pass
		case 3:
			print("====================")
			view_your_courses(authenticated_user)
			pass
		case 4:
			edit_course_info(authenticated_user)
		case 5:
			print("====================")
			for user in User.user_list:
				print(user)
				print("====================")
		case 6:
			view_schedule(authenticated_user)
		case 7:
			submit_assignment(authenticated_user)
		case 8:
			authenticated_user = authenticate_user()
		case 0:
			break
		case _:
			print("Invalid selection, try again")

