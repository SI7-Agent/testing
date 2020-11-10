from abc import abstractmethod


class Commands:
    connectmanager = None
    currentid_human = 0
    currentid_event = 0
    currentid_recognition = 0

    def __init__(self, cm):
        self.connectmanager = cm

    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def create_side_funcs(self):
        pass

    @abstractmethod
    def push_face(self, face_metadata):
        pass

    @abstractmethod
    def get_guy(self, params='*', filters=''):
        pass

    @abstractmethod
    def push_event(self, metadata):
        pass

    @abstractmethod
    def get_emotes_with_interval(self, interval, *args):
        pass

    @abstractmethod
    def push_recognition(self, metadata):
        pass

    @abstractmethod
    def get_recognition(self, params='*', filters=''):
        pass

    @abstractmethod
    def get_object_with_interval(self, what_we_need, interval):
        pass

    @abstractmethod
    def update_metadata(self, new_metadata):
        pass

    @abstractmethod
    def push_log(self, table_name, exception_name):
        pass
