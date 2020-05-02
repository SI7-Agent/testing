from admin_tools.admin_tool import AdminTool
from query_tool.select_tool import SelectPostgreSQL
from query_tool.abstract_query_tool import Commands

import pickle
import psycopg2


class UpdatePostgreSQL(Commands):
    def update_metadata(self, new_metadata):
        try:
            data_to_upd = pickle.dumps(new_metadata)

            name = "'" + new_metadata['name'] + "'"
            param = 'id_people'
            filter = 'where name = ' + name
            ids = SelectPostgreSQL(self.connectmanager).get_guy(param, filter)[0][0]

            self.connectmanager.cursor.execute("UPDATE people_id SET face = %s where id_people = %s",
                                               (data_to_upd, str(ids)))

            self.connectmanager.database.commit()
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'Face metadata update succeeded')
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'Face metadata update failed. NULL restriction')


class UpdateInfluxDB(Commands):
    def update_metadata(self, new_metadata):
        pass
