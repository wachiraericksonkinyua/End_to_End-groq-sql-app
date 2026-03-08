import sqlite3

connection = sqlite3.connect('Students.db')
cursor = connection.cursor()

table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25));
"""
cursor.execute(table_info)

cursor.execute('''INSERT INTO STUDENT VALUES('John','datascience','A')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Jane','datascience','B')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Doe','datascience','C')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Smith','devops','A')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Emily','devops','B')''')

connection.commit()  # ← THIS WAS MISSING

print("The inserted records are:")
data = cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

connection.close()