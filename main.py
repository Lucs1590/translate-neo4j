from translation import google
import requests
from py2neo import Graph, Node


def main():
    connection = connect_database()
    data = get_data()
    insert_data(data)


def connect_database():
    return Graph(
        host='localhost',
        port=7687,
        password='',
        database=''
    )


def get_data():
    return requests.get('https://world.openfoodfacts.org/ingredients.json')


def insert_data(data):
    ...


if __name__ == "__main__":
    main()
