class AppSettings:
    """Singleton class to store widely used settings."""
    instance = None
    dia_path: str = ''
    sql_path: str = ''
    sql_type: str = ''
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance