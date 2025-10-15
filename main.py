from user import User, Role
from utility import create_course, view_your_courses, edit_course_info

User.user_list.append(User("admin", "pass", Role.ADMIN))

user = False
while True:
	username = input("Enter your username: ")
	password = input("Enter your password: ")

	user = User.authenticate_user(username, password)

	if type(user) != User:
		print("Incorrect login, try again")
	else:
		print("Correct login")
		break
		
while True:
	selection = int(input("""0) Exit program
1) Create a new course (admin)
2) View courses (student, instructor, admin)
3) Edit course info (instructor)"""))

	match selection:
		case 1:
			create_course(user)
			pass
		case 2:
			view_your_courses(user)
			pass
		case 3:
			edit_course_info(user)
			pass
		case 0:
			break
		case _:
			print("Invalid selection, try again")
