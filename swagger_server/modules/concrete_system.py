from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.object_module import ObjectModule
from modules.people_module import PeopleModule
from modules.object_module import ObjectModuleWeb
from modules.people_module import PeopleModuleWeb
from robot import Robot


class MySystem(Robot):
    @EmoteModule.emt_decorate
    def find_emote(self, frame):
        pass

    @GenderModule.gnd_decorate
    def find_gender(self, frame):
        pass

    @ObjectModule.obj_decorate
    def find_objects(self, frame):
        pass

    @PeopleModule.people_decorate
    def find_persons(self, frame):
        pass


class MySystemWeb(MySystem):
    @ObjectModuleWeb.obj_decorate
    def find_objects(self, frame):
        pass

    @PeopleModuleWeb.people_decorate
    def find_persons(self, frame):
        pass
