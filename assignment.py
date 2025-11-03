from __future__ import annotations
from datetime import date
from notifications import Notification, TargetType

from course import Course

class Assignment:
  assignment_list: list[Assignment] = []
  max_id: int = 0

  def __init__(self, title: str, due_date: date, course_id: int):
    self.assignment_id: int = Assignment.max_id
    Assignment.max_id += 1

    self.title: str = title
    self.due_date: date = due_date
    self.course_id: int = course_id

    Assignment.assignment_list.append(self)
    course = Course.find_course_by_id(course_id)
    if type(course) is Course:
      course.assignment_ids.add(self.assignment_id)
    # make a notification
    Notification(f"New assignment!: {title} for course {course_id}", TargetType.COURSE_MEMBERS, due_date, course_id)
  
  @staticmethod
  def find_assignment_by_id(assignment_id: int) -> Assignment | bool:
    for assignment in Assignment.assignment_list:
      if assignment.assignment_id == assignment_id:
        return assignment
    print("Assignment not found")
    return False

  @staticmethod
  def find_assignments_by_course_id(course_id: int) -> list[Assignment]:
    ret: list[Assignment] = []
    for assignment in Assignment.assignment_list:
      if assignment.course_id == course_id:
        ret.append(assignment)
    return ret

  def __str__(self):
    return f"""Assignment id: {self.assignment_id}
Title: {self.title}
Due date: {self.due_date}
Course id: {self.course_id}"""