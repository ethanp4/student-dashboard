from __future__ import annotations

class Course:
	course_list: list[Course] = []
	max_id: int = 0

	def __init__(self, title: str, owner_id: int):
		self.course_id = Course.max_id
		Course.max_id += 1

		self.title = title
		self.owner_id = owner_id
		self.attendees_ids: set[int] = set() # unique ids of users attending the course
		self.assignment_ids: set[int] = set()

	
	@staticmethod
	def find_course_by_id(course_id: int) -> Course | bool:
		for course in Course.course_list:
			if course.course_id == course_id:
				return course
		print("Course not found")
		return False

	@staticmethod
	def find_courses_by_attendee_id(attendee_id: int) -> list[Course]:
		ret: list[Course] = []
		for course in Course.course_list:
			if attendee_id in course.attendees_ids:
				ret.append(course)
		return ret
	
	@staticmethod
	def find_courses_by_owner_id(owner_id: int) -> list[Course]:
		ret: list[Course] = []
		for course in Course.course_list:
			if owner_id == course.owner_id:
				ret.append(course)
		return ret

	def __str__(self):
		return f"""Course id: {self.course_id}
Title: {self.title}
Owner id: {self.owner_id}
Attendee ids: {', '.join(map(str, self.attendees_ids)) if len(self.attendees_ids) > 0 else 'None'}"""