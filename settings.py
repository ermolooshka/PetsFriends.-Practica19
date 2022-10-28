import os

from dotenv import load_dotenv

load_dotenv()
valid_email = os.getenv("valid_email")
valid_password = os.getenv("valid_password")


invalid_email = "test@test.qa"
invalid_password = "1234"

pet_without_photo = {'name': 'Wilson', 'animal_type': 'cat', 'age': '12' }
pet_new_info = {'name': 'Rey', 'animal_type': 'Dog', 'age': '10'}