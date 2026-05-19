
import sqlite3
import csv

if __name__ == "__main__" :
    connect=sqlite3.connect("users.db")
    # connect.row_factory=sqlite3.Row
    cursor=connect.cursor()
    f = open('users.csv', 'r')
    query="INSERT OR IGNORE INTO users(id,name) VALUES(?,?);"
    with f:
        # reader = csv.DictReader(f, delimiter=",",fieldnames=columns)  
        reader = csv.DictReader(f, delimiter=",")  
        for row in reader :
            to_insert=row['id'],row['name']
            cursor.execute(query,to_insert)
    connect.commit()
