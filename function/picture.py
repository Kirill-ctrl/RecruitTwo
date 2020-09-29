from UsedClass.UsersClass import Users, PictureApplicant
import os
from function.response import added


def photo(file, name, token):
    user = Users()
    email = user.get_email(token)
    user_id = user.get_id_users(email)

    content = search_content_type(file)

    y = dict(content_type=content[20:24], name=name)

    picture = PictureApplicant()

    if y['content_type'] == 'jpeg':
        path, pathjpg = get_good_filename_to_jpg(content, name)

        if path:
            picture.add_photo(path, user_id)

        elif pathjpg:
            picture.add_photo(pathjpg, user_id)

    else:
        path = get_good_filename_to_png(content, name)
        picture.add_photo(path, user_id)

    return added()


def find(name):
    for root, dirs, files in os.walk('/'):
        if name in files:
            return os.path.join(root, name)


def search_content_type(file):
    ContentType = 'Content-Type'.encode('utf-8')
    a = file.find(ContentType)
    content = file[a: a + 24].decode('utf-8')
    return content


def get_good_filename_to_jpg(content, name):
    y = dict(content_type=content[20:24], name=name)
    filename = f"{name}.{y['content_type']}"
    filenamejpg = f"{name}.jpg"
    path = find(filename)
    pathjpg = find(filenamejpg)
    return path, pathjpg

def get_good_filename_to_png(content, name):
    y = dict(content_type=content[20:23], name=name)
    filename = f"{name}.{y['content_type']}"
    path = find(filename)
    return path
