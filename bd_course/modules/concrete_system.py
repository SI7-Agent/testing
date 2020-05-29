from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.object_module import ObjectModule
from modules.people_module import PeopleModule
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
