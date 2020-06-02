from string_methods import StringsMethods

import os
import urllib
import vk


class IntegrateWithVk:
    @staticmethod
    def __connect(username, password):
        pass

    def get_images(self):
        pass

    @staticmethod
    def read_config():
        with open(os.getcwd() + "\\configs\\album_url.ini", "r") as f:
            data = f.read()
        user = StringsMethods.user_by_url(data)
        album = StringsMethods.album_by_url(data)
        return user, album

class IntegrateWithVkVkLib(IntegrateWithVk):
    @staticmethod
    def __connect(username, password):
        app_id = 7495454
        session = vk.AuthSession(app_id, username, password, "photos, wall")
        vk_api = vk.API(session)
        return vk_api

    def get_images(self):
        vk_api = self.__connect(u := input("Username: "), p := input("Password: "))
        owner, album = self.read_config()
        test = vk_api.photos.get(owner_id=owner, v=5.107, album_id=album)

        os.chdir(os.getcwd() + "\\pic_folder")

        num = 0
        for items in test["items"]:
            num += 1
            url = items["sizes"][-1]["url"]

            name = os.getcwd() + "\\" + str(num) + ".png"
            urllib.request.urlretrieve(url, name)
