from __future__ import annotations

class Course:
    course_list: list[Course]

    def __init__(self, title: str, desc: str, owner_id: int):
        self.course_id = len(Course.course_list)
        self.title = title
        self.desc = desc
        self.owner_id = owner_id

        
    