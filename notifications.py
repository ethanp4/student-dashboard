from __future__ import annotations
from datetime import date
from enum import Enum
from colours import Colours
from user import User, Role
from course import Course

class TargetType(Enum):
  ADMINS = 0 #notification for all admins (student is added or removed from a course)
  COURSE_MEMBERS = 1 # notifications for all students of a course and its owner (assignment due dates)

class Notification:
  notification_list: list[Notification] = []

  # when a notification is created, it is automatically added to the notification_list
  # for example: when an assignment is created, a matching notification is also created for the members of that course
  def __init__(self, message: str, target_type: TargetType, due_date: date = date.today(), target_course_id: int = -1):
    self.message = message
    self.target_type = target_type
    self.due_date = due_date
    self.target_course_id = target_course_id
    Notification.notification_list.append(self)

  # any user will call this function and it will return the notifications relevant to them
  @staticmethod
  def get_notifications(user: User) -> list[Notification] | bool:
    ret: list[Notification] = []
    if not user.subscription_status:
      print(f"{Colours.RED}Your subscription status doesn't allow you to view notifications. Consider subscribing today!{Colours.RESET}")
      return False
    match user.role:
      case Role.STUDENT:
        enrolled_courses = Course.find_courses_by_attendee_id(user.user_id)
        enrolled_ids: set[int] = set()
        for course in enrolled_courses:
          enrolled_ids.add(course.course_id)
        for notification in Notification.notification_list:
          if notification.target_type == TargetType.COURSE_MEMBERS and notification.target_course_id in enrolled_ids:
            ret.append(notification)
        pass
      case Role.TEACHER:
        owned_courses = Course.find_courses_by_owner_id(user.user_id)
        owned_ids: set[int] = set()
        for course in owned_courses:
          owned_ids.add(course.course_id)
        for notification in Notification.notification_list:
          if notification.target_type == TargetType.COURSE_MEMBERS and notification.target_course_id in owned_ids:
            ret.append(notification)
        pass
      case Role.ADMIN:
        for notification in Notification.notification_list:
          if notification.target_type == TargetType.ADMINS:
            ret.append(notification)
        pass
    return ret
  
  def __str__(self):
    return f"""{self.message} @ {Colours.UNDERLINE}{self.due_date}{Colours.RESET}"""