def connection_string():
    server = 'DESKTOP-CHJO2FQ\MYSQL'
    database = 'Project'
    use_windows_authentication = True 
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return connection_string