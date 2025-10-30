from datetime import date, timedelta
from assignment import Assignment
from colours import Colours
from course import Course
from notifications import Notification, TargetType
from user import User, Role
from utility import create_course, delete_course, submit_assignment, view_schedule, view_your_courses, edit_course_info

def authenticate_user() -> User:
	while True:
		username = input("Enter your username: ")
		password = input("Enter your password: ")

		authenticated_user = User.authenticate_user(username, password)

		if type(authenticated_user) != User:
			Notification("Failed login attempt", TargetType.ADMINS)
			print("Incorrect login, try again")
		else:
			print("Correct login")
			match authenticated_user.subscription_status:
				case True:
					print(f"{Colours.GREEN}Welcome, premium user!{Colours.RESET}")
				case False:
					print(f"{Colours.YELLOW}Welcome, free user! Consider upgrading to premium for more features.{Colours.RESET}")
			return authenticated_user
		

User("a1", "pass", Role.ADMIN, True)
User("t1", "pass", Role.TEACHER, False) # id 1
User("t2", "pass", Role.TEACHER, True) # id 2
User("s1", "pass", Role.STUDENT, True)
User("s2", "pass", Role.STUDENT, True)
User("s3", "pass", Role.STUDENT, False)
User("s4", "pass", Role.STUDENT, False)
User("s5", "pass", Role.STUDENT, False)
User("s6", "pass", Role.STUDENT, False)

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
	selection = int(input(f"""\n0) Exit program
1) Create a new course (admin only)
2) Delete course (admin only)
3) View courses (all roles)
4) Edit course info (instructor only)
5) View user list (all roles)
6) View upcoming dates (all roles)
7) Submit assignment (students only)
8) Change user
9) View notifications (all roles)
10) {"Subscribe to premium ($5.99 / month)" if not authenticated_user.subscription_status else "Unsubscribe from premium"} (all roles)
"""))

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
		case 9:
			notifications = Notification.get_notifications(authenticated_user)
			if type(notifications) is bool:
				pass
			else:
				if not notifications:
					print("You have no notifications at this time")
				for notification in notifications:
					print(notification)

		case 10:
			print(f"{Colours.YELLOW}We're sad to see you go.{Colours.RESET}" if authenticated_user.subscription_status else f"{Colours.GREEN}Thank you for choosing to become a premium D4L member!{Colours.RESET}")
			authenticated_user.subscription_status = not authenticated_user.subscription_status
		case 0:
			break
		case _:
			print("Invalid selection, try again")

