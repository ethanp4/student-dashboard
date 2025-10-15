from __future__ import annotations
from enum import Enum
from typing import Union

class Role(Enum):
	STUDENT = 0
	TEACHER = 1
	ADMIN = 2

class User:
	user_list: list[User] = []
	max_id: int = 0

	def __init__(self, username: str, password: str, role: Role):
		self.user_id: int = User.max_id
		User.max_id += 1
		self.username: str = username
		self.password: str = password
		self.role: Role = role

	@staticmethod
	def authenticate_user(username: str, password:str) -> Union[User, bool]:
		for user in User.user_list:
			if user.username == username and user.password == password:
				return user
		return False
	
	def __str__(self):
		return f"""User id: {self.user_id}
Username: {self.username}
Role: {self.role.name}"""
