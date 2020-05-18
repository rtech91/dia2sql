from app.settings import AppSettings
from collections import deque

class TableInterface:
    name: str
    comment: str
    columns = deque()

    def getSQL(self) -> str:
        """Get generated SQL for current table."""
        pass

class TableFactory:

    """Create table according to the SQL type given in the App settings."""
    def get_table(self, table_data: set):
        #TODO: add support for acceptable database systems only.
        settings = AppSettings()
        sqltype = settings.sql_type
        if sqltype == '':
            return None
        elif sqltype == 'mysql':
            return MySQLTable(table_data)

class MySQLTable(TableInterface):

    #default_engine: str = 'myisam'
    #acceptable_engines: [] = ['myisam', 'innodb']
    #TODO: add support for different engines

    def __init__(self, table_data: set):
        super().__init__()
        self.name = table_data['name']
        self.comment = table_data['comment']
        self.columns = table_data['columns']
    
    def getSQL(self):
        super().getSQL()
        sql_text: str = ''
        primary_column: str = ''
        sql_text += "CREATE TABLE `{table_name}` (\n".format(table_name=self.name)
        while self.columns:
            column = self.columns.popleft()
            attr_is_null = 'NOT NULL' if column['is_null'] == 'false' else 'NULL'
            attr_is_unique = 'UNIQUE' if column['is_unique'] == 'true' else ''
            attr_auto_increment = 'AUTO_INCREMENT' if column['is_primary'] == 'true' else ''
            attr_comment = "COMMENT \"{comment}\"".format(comment=column['comment']) if column['comment'] != '' else ''
            column_text = "\t`{col_name}` {type} {is_null} {is_ai} {is_unique} {comment},{sep}".format(
                col_name=column['name'],
                type=column['type'],
                is_null=attr_is_null,
                is_ai=attr_auto_increment,
                is_unique=attr_is_unique,
                comment=attr_comment,
                sep="\n"
            )
            sql_text += column_text

            if column['is_primary'] and primary_column == '':
                primary_column = "\tPRIMARY KEY (`{column_name}`)\n".format(column_name=column['name'], sep="\n")

        if primary_column != '':
            sql_text += primary_column
        
        sql_text += ") ENGINE=MYISAM COMMENT=\"{comment}\";\n\n".format(comment=self.comment)
        return sql_text

