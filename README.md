# PythonScriptsForSQLite
Some pythons scripts to manipulate SQLite databases

## MergeDatabasesWithSameName.py

This script merges all the databases with the same name that are contained in different folders. For example, it is possible to unify all the daily logs (dbs) from a certain tool.

**Initial folder structure**
````shell
¬ 01/01/2015
  ¬ LogServer.db -(100 records)
  ¬ ClientServer.db
  ¬ OtherDB.db
¬ 02/01/2015
  ¬ LogServer.db -(50 records)
  ¬ ClientServer.db
  ¬ OtherDB.db
¬ 03/01/2015
  ¬ LogServer.db -(200 records)
  ¬ ClientServer.db
  ¬ OtherDB.db
````

**Final folder structure:**
````shell
¬ OutputFolder
  ¬ LogServer.db -(350 records)
  ¬ ClientServer.db
  ¬ OtherDB.db
````


