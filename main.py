from course import Course
from user import User, Role
from utility import create_course, delete_course, view_your_courses, edit_course_info

def authenticate_user(username = "", password = "") -> User:
	# for testing purposes
	if username != "" and password != "":
		authenticated_user = User.authenticate_user(username, password)

		if type(authenticated_user) != User:
			print("Incorrect login, try again")
			return authenticate_user()
		else:
			print("Correct login")
			return authenticated_user

	while True:
		username = input("Enter your username: ")
		password = input("Enter your password: ")

		authenticated_user = User.authenticate_user(username, password)

		if type(authenticated_user) != User:
			print("Incorrect login, try again")
		else:
			print("Correct login")
			return authenticated_user

User.user_list.extend([
	User("a1", "pass", Role.ADMIN),
	User("t1", "pass", Role.TEACHER), # id 1
	User("t2", "pass", Role.TEACHER), # id 2
	User("s1", "pass", Role.STUDENT),
	User("s2", "pass", Role.STUDENT),
	User("s3", "pass", Role.STUDENT),
	User("s4", "pass", Role.STUDENT),
	User("s5", "pass", Role.STUDENT),
	User("s6", "pass", Role.STUDENT),
])

Course.course_list.extend([
	Course("Math 100", 1),
	Course("Physics 100", 1),
	Course("Chemistry 200", 1),
	Course("Biology 200", 2),
	Course("History 200", 2),
	Course("English 300", 2)
])

authenticated_user = authenticate_user()
		
while True:
	selection = int(input("""0) Exit program
1) Create a new course (admin)
2) Delete course
3) View courses (student, instructor, admin)
4) Edit course info (instructor)
5) View user list
6) Change user\n"""))

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
			authenticated_user = authenticate_user()
		case 0:
			break
		case _:
			print("Invalid selection, try again")

