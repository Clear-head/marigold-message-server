from src.application.auth.password_hasher import hash_password
from src.controller.schema.register_schema import RegisterSchema
from src.domain.entity.user import User
from src.domain.exception.domain_exception import DomainException
from src.domain.exception.user_already_exists_exception import UserAlreadyExistsException
from src.infrastructure.mongodb.user_repository_impl import UserRepositoryImpl


class UserRegister:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    async def execute(self, register_schema: RegisterSchema) -> User:
        if await self.user_repository.find_by_id(register_schema.user_id):
            raise UserAlreadyExistsException(f"User ID '{register_schema.user_id}' already exists.")

        if await self.user_repository.find_by_email(register_schema.email):
            raise UserAlreadyExistsException(f"Email '{register_schema.email}' already exists.")

        if await self.user_repository.find_by_phone_number(register_schema.phone_number):
            raise UserAlreadyExistsException(f"Phone number '{register_schema.phone_number}' already exists.")

        try:
            hashed_password = hash_password(register_schema.password)
            user = User.create(
                user_id=register_schema.user_id,
                username=register_schema.username,
                password=hashed_password,
                email=register_schema.email,
                phone_number=register_schema.phone_number,
                birth_date=register_schema.birth_date,
                gender=register_schema.gender
            )
            await self.user_repository.save(user)
            return user
        except Exception as e:
            raise DomainException(f"User registration failed: {e}")