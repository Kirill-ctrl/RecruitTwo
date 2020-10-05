from UsedClass.UsersClass import Users, PictureUsers
import os
from function.check_correct_token import check_token
from function.response import incorrect_token, incorrect_mimetype


def photo(file, token: str):
    if check_token(token):
        user = Users()
        email = user.get_email(token)
        user_id = user.get_id_users(email)
        picture = PictureUsers()
        if file.content_type == 'image/png':
            naming = f"image_user_{user_id}.png"
            path = f'C:/users/kpech/photousers/{naming}'
            file.save(f'C:/users/kpech/photousers/{naming}')
            return picture.add_photo(path, user_id)
        elif file.content_type == 'image/jpeg':
            naming = f"image_user_{user_id}.jpg"
            path = f'C:/users/kpech/photousers/{naming}'
            file.save(f'C:/users/kpech/photousers/{naming}')
            return picture.add_photo(path, user_id)
    else:
        return incorrect_token()


def find(name: str):
    path = 'C:/users/kpech/photousers/'
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_picture(token: str):
    if check_token(token):
        picture = PictureUsers()
        path = picture.get_path_picture(token)
        if 'jpeg' in path or 'jpg' in path:
            mimetype = 'image/jpeg'
            return path, mimetype
        elif 'png' in path:
            mimetype = 'image/png'
            return path, mimetype
        else:
            return incorrect_mimetype()
    else:
        return incorrect_token()
