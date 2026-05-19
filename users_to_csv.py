
import sqlite3
import csv

if __name__ == "__main__" :
    db_name="users.db"
    table_name="users"
    connect=sqlite3.connect(db_name)
    connect.row_factory=sqlite3.Row
    cursor=connect.cursor()
    f = open('users.csv', 'w')
    query="SELECT * from "+table_name
    results=cursor.execute(query)
    columns=[]
    for result in results.description :
        columns.append(result[0])
    with f:
        writer = csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        for result in results :
            string =""
            for i in range (len(columns)) :
                string=string + "columns ["+str(i)+"]:"+"result[columns["+str(i)+"]],"
            print(eval("{"+string+"}"))
            writer.writerow (eval("{"+string+"}"))        
    connect.commit()
