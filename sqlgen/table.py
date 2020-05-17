from app.settings import AppSettings

class TableInterface:
    name: str
    comment: str
    columns: [dict]

    def getSQL(self) -> str:
        """Get generated SQL for current table."""
        pass

class TableFactory:
    """Create table according to the SQL type given in the App settings."""
    def get_table(self, table_data: set):
        settings = AppSettings()
        sqltype = settings.sql_type
        if sqltype == '':
            return None
        elif sqltype == 'mysql':
            return MySQLTable(table_data)

class MySQLTable(TableInterface):
    def __init__(self, table_data: set):
        super().__init__()
        self.name = table_data['name']
        self.comment = table_data['comment']
        self.columns = table_data['columns']
    
    def getSQL(self):
        #TODO: implement generation of SQL Table schema
        super().getSQL()
        pass


