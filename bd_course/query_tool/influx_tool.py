from query_tool.abstract_query_tool import Commands


class InfluxDBTool(Commands):
    def push_face(self, face_metadata):
        pass

    def push_event(self, metadata):
        pass

    def push_recognition(self, metadata):
        pass

    def get_guy(self, params='*', filters=''):
        pass

    def get_emotes_with_interval(self, interval, *args):
        pass

    def get_recognition(self, params='*', filters=''):
        pass

    def get_object_with_interval(self, what_we_need, interval):
        pass

    def update_metadata(self, new_metadata):
        pass
