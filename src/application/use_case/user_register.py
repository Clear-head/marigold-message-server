from fastapi.responses import JSONResponse

from src.application.auth.password_hasher import hash_password
from src.controller.schema.register_schema import RegisterSchema
from src.domain.entity.user import User
from src.domain.exception.domain_exception import DomainException
from src.domain.exception.duplicate_email_exception import DuplicateEmailException
from src.domain.exception.duplicate_phone_number_exception import DuplicatePhoneNumberException
from src.domain.exception.duplicate_user_id_exception import DuplicateUserIdException
from src.infrastructure.mongodb.user_repository_impl import UserRepositoryImpl


class UserRegister:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    async def execute(self, register_schema: RegisterSchema) -> JSONResponse:
        try:
            if await self.user_repository.find_by_id(register_schema.user_id):
                raise DuplicateUserIdException(f"User ID '{register_schema.user_id}' already exists.")

            if await self.user_repository.find_by_email(register_schema.email):
                raise DuplicateEmailException(f"Email '{register_schema.email}' already exists.")

            if await self.user_repository.find_by_phone_number(register_schema.phone_number):
                raise DuplicatePhoneNumberException(f"Phone number '{register_schema.phone_number}' already exists.")

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
            return JSONResponse(status_code=201, content={"message": "User registered successfully", "user_id": user.id.value})
        except DuplicateUserIdException as e:
            return JSONResponse(status_code=400, content={"error_code": "DUPLICATE_USER_ID", "message": str(e)})
        except DuplicateEmailException as e:
            return JSONResponse(status_code=400, content={"error_code": "DUPLICATE_EMAIL", "message": str(e)})
        except DuplicatePhoneNumberException as e:
            return JSONResponse(status_code=400, content={"error_code": "DUPLICATE_PHONE_NUMBER", "message": str(e)})
        except DomainException as e:
            return JSONResponse(status_code=400, content={"error_code": "REGISTRATION_FAILED", "message": f"User registration failed: {e}"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error_code": "INTERNAL_SERVER_ERROR", "message": f"An unexpected error occurred: {e}"})