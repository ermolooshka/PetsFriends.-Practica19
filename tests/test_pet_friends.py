# from api import PetFriends
# from settings import valid_email, valid_password

import requests
from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что ответ на запрос приходит со статусом 200 и в теле ответа есть ключ"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets_valid_key(filter=''):
    """Проверка возможности получения списка питомцев. Статус 200 и списка питомцев """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_pet_without_photo_valid(name=pet_without_photo['name'], animal_type=pet_without_photo['animal_type'],
                                      age=pet_without_photo['age']):
    """Проверка возможности добавления питомца без фото.
    Статус 200 в теле ответа есть добавленный питомец с указанным именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == pet_without_photo['name']

def test_post_pet_with_photo_valid(
        name=pet_without_photo['name'],
        animal_type=pet_without_photo['animal_type'],
        age=pet_without_photo['age'],
        pet_photo='images\cat.jpg'
):
    """Проверка возможности добавления питомца с фото, статус 200 и в теле ответа значение pet_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_put_new_info_valid(
        name=pet_new_info['name'],
        animal_type=pet_new_info['animal_type'],
        age=pet_new_info['age']):
    """Проверка возможности изменения информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.put_new_info(auth_key, name, animal_type, age, pet_id['pets'][0]['id'])
    assert status == 200
    assert result['name'] == pet_new_info['name']

def test_post_new_foto_for_pet_valid(pet_photo='images\dog.jpg'):
    """Проверка, можно ли добавить или изменить фото питомца,
    статус 200 и тело ответа имеет значение pet_photo"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    status, result = pf.post_new_foto_for_pet(auth_key, pet_id['pets'][0]['id'], pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_delete_pet_pass():
    """Проверка, можно ли удалить существующее домашнее животное"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(pet_id['pets']) == 0:
        pf.status, result = pf.post_pet_without_photo(auth_key, 'Bill', 'Dog', '4')
        _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()
    assert len(result) == 0


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Убедитесь, что запрос ключа API не возвращает статус 200"""
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'This user wasn&#x27;t found in database' in result

def test_get_list_of_pets_invalid_key(filter=''):
    """Проверка, возможно ли получить список питомцев с неверным auth_key. Статус 403 и сообщение"""
    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result

def test_post_new_pet_with_incorrect_data(name='%$#@!', animal_type='54321', age='100'):
    """Проверка возможности добавления питомца с некорректными данными, статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert 'Provided data is incorrect' in result

def test_delete_not_my_pet_pass():
    """Проверка возможности удаления чужого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pet_id = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(pet_id['pets']) != 0:
        for i in range(len(pet_id['pets'])):
            _, result = pf.delete_pet(auth_key, pet_id['pets'][i]['id'])

    _, pet_id = pf.get_list_of_pets(auth_key, '')
    status, result = pf.delete_pet(auth_key, pet_id['pets'][0]['id'])

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id['pets'][0]['id'] not in my_pets.values()