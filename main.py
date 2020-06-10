from translate import Translator
import requests
from py2neo import Graph, Node


def main():
    connection = connect_database()
    data = get_data()
    insert_data(connection, data)


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


def tranlate_data(data):
    return Translator(to_lang="pt").translator.translate(data)


if __name__ == "__main__":
    main()
