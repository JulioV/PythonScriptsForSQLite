import os, sqlite3

dbOutputDirectory = "/home/FOLDER_WHERE_TO_SAVE_NEW_DB"
dbDirectory = "/home/FOLDER_WHERE_DATABASES_ARE_ORGANIZED_IN_SUBFOLDERS"
uniqueColumn = "A_COLUMN_NAME" # A column which values should be unique in the ouput db. This is a way to filter repeated records
ignoredColumns = ["A_COLUMN_NAME"] # Columns to ignore when copying in all the tables of the input database. This is a way to avoid copying primary indexes

# Get all the subfolders in dbDirectory which contain the different SQLite databases
def getDbDirectories():
	os.chdir(dbDirectory)
	return sorted([os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)])

# Get all the SQLite databases in a folder
def getDbFilesInDirectory(folder):
	os.chdir(folder)
	return [os.path.abspath(name) for name in os.listdir(".") if os.path.isfile(name) and os.path.splitext(name)[1] == '.db']

# Create output db file with the same scheme as inputDBFile
def createEmptyOutputDB(inputDBFile, outputDBFile):
	# Create output db in output directory
	outputConnection = sqlite3.connect(outputDBFile)
	outputCursor = outputConnection.cursor()

	# Extract db scheme 
	inputConnection = sqlite3.connect(inputDBFile)
	cursor = inputConnection.cursor()
	cursor.execute("select sql from sqlite_master where sql not NULL and name <> 'sqlite_sequence'")
	# Execute db scheme into output db
	for row in cursor.fetchall():
		outputCursor.execute(row[0])

	inputConnection.close()
	outputConnection.close()

# Transfer data of table "tableName" in inputDBFile to the same table in outputDBFile
def transferTableData(tableName, inputDBFile, outputDBFile):

	# Prepare in and out connections
	outputConnection = sqlite3.connect(outputDBFile)
	outputCursor = outputConnection.cursor()
	inputConnection = sqlite3.connect(inputDBFile)
	inputCursor = inputConnection.cursor()


	# Get the list of columns to transfer from table
	inputCursor.execute("PRAGMA table_info("+ tableName +")")
	columnNames = [column[1] for column in inputCursor.fetchall()]

	# Get ride of columns to ignore
	columnNames = [name for name in columnNames if name not in ignoredColumns]

	joinedColumnNames = ','.join(columnNames)
	marksToSubstitueValues = ','.join(['?'] * len(columnNames))

	for row in inputCursor.execute("SELECT %s from %s" % (joinedColumnNames,tableName)):
	  # TODO. If you want to check for more than one uniqueColumn, then modify the underlying if and put it in a for loop
		if uniqueColumn in columnNames:
			outputCursor.execute("SELECT * from %s where %s = ?" % (tableName, uniqueColumn), (row[columnNames.index(uniqueColumn)], ))
			if outputCursor.fetchone() != None:
				continue
		
		outputCursor.execute("INSERT INTO %s(%s) values(%s)" % (tableName, joinedColumnNames, marksToSubstitueValues), row)

  # Close conections
	outputConnection.commit()
	inputConnection.close()
	outputConnection.close()

# Merge SQLite databse (dbFile) into a file with the same name and structure in dbOutput
def mergeDbFile(dbFile):
	

	#Check if the output db already existis, if not create one with the same schema
	outputDBFile = os.path.join(dbOutputDirectory, os.path.basename(dbFile))
	if not os.path.exists(outputDBFile):
		createEmptyOutputDB(dbFile, outputDBFile)

	# Get list of tables to transfer and transfer data from dbFile to outputDBFile
	connection = sqlite3.connect(dbFile)
	cursor = connection.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name <> 'sqlite_sequence';")
	tables = cursor.fetchall()
	connection.close()
	
	# Transfer data from each table to the output database
	for table in tables:
		transferTableData(table[0], dbFile, outputDBFile)

# Main method
def main():
	dbFolders = getDbDirectories()
	for folder in dbFolders:
		for dbFile in getDbFilesInDirectory(folder):
			mergeDbFile(dbFile)
		print folder

	

main()
