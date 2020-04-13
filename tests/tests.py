import os
import requests
import unittest
from sqlalchemy import create_engine
import psycopg2

class DockerComposeTestCase(unittest.TestCase):
    def test_post(self):
        expression = {'expression': "1+5"}
        result = requests.post('http://localhost:5000/add', data=expression)
        self.assertEqual(result.status_code, 200)
        
    def test_error_post(self):
        incorrect = {"expression": "incorrect test"}
        result = requests.post('http://localhost:5000/add', data=incorrect)
        self.assertNotEqual(result.status_code, 200)

    def test_database(self):
        expression = {'expression': "1+5"}
        result = requests.post('http://localhost:5000/add', data=expression)
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        connection = engine.connect()
        results = connection.execute("SELECT * FROM Expression WHERE text='1+5'").fetchall()

        self.assertNotEqual(len(results), 0)

    def test_database_error(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+'")
            rows = rs.fetchall()

        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    unittest.main()
