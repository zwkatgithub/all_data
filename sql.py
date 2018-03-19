
class Sql:
    insertValue = "INSERT INTO {table}({colNames}) VALUES({value});"
    insertValues = "INSERT INTO {table}({colNames}) VALUES {values};"
    insertIgnoreValue = "INSERT IGNORE INTO {table}({colNames}) VALUES({value});"