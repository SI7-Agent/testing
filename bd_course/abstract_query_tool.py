from abc import abstractmethod


class Commands:
    connectmanager = None
    currentid_human = 1
    currentid_event = 1
    currentid_recognition = 1
    currentid_log = 1

    @abstractmethod
    def create_tables(self):
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
    def push_recognition(self, metadata):
        pass

    @abstractmethod
    def get_recognition(self, params='*', filters=''):
        pass

    @abstractmethod
    def update_metadata(self, new_metadata):
        pass

    @abstractmethod
    def push_log(self, table_name, exception_name):
        pass