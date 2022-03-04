from flask import Flask, request
import sqlite3

from sqlite3 import Error

app = Flask(__name__)   # Flask constructor

def create_connection(path):
    connection = None

    try:
        connection = sqlite3.connect(path)

        print("Connection to SQLite DB successful")
    except Error as e:

        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
  cursor = connection.cursor()
  try:
      cursor.execute(query)
      connection.commit()
      print("Query executed successfully")

      return cursor
  except Error as e:
      print(f"The error '{e}' occurred")

@app.route('/')
def create():
  db_conn = create_connection("chat.sqlite")

  create_query = """
CREATE TABLE IF NOT EXISTS chat (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nama TEXT NOT NULL,
pesan TEXT NOT NULL
);
"""

  execute_query(db_conn, create_query)

  return "Successfully created table"

@app.route('/insert', methods=['POST'])      
def insert():
    db_conn = create_connection("chat.sqlite")
    body = request.json

    insert_query = f"""
INSERT INTO chat (nama, pesan) 
VALUES ("{body['namaBody']}", "{body['pesanBody']}")
"""
    execute_query(db_conn, insert_query)
    
    return "Successfully inserted record"

@app.route('/get')      
def get():
    db_conn = create_connection("chat.sqlite")

    get_query = """SELECT * FROM chat"""
    cursor = execute_query(db_conn, get_query)

    rows = cursor.fetchall()
    
    return {
      "data": rows
    }

@app.route('/delete', methods=["DELETE"])
def delete():
    db_conn = create_connection('chat.sqlite')

    deleteQuery = "DROP TABLE chat"
    execute_query(db_conn, deleteQuery)

    return "Table successfully deleted"

if __name__=='__main__':
  app.run()