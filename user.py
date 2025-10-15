from __future__ import annotations
from enum import Enum
from typing import Union

class Role(Enum):
	STUDENT = 0
	TEACHER = 1
	ADMIN = 2

class User:
	user_list: list[User] = []

	def __init__(self, username: str, password: str, role: Role):
		self.user_id: int = len(User.user_list)
		self.username: str = username
		self.password: str = password
		self.role: Role = role
		self.

	@staticmethod
	def authenticate_user(username: str, password:str) -> Union[User, bool]:
		for user in User.user_list:
			if user.username == username and user.password == password:
				return user
		return False
	
