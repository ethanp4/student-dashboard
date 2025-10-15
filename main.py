from user import User, Role

User.user_list.append(User("admin", "pass", Role.ADMIN))

username = input("Enter your username: ")
password = input("Enter your password: ")

result = User.authenticate_user(username, password)

selection = input("""1) Create a new course (admin)
                  2) View courses (student, instructor, admin)
                  3) Edit course info (instructor)""")

print(result)