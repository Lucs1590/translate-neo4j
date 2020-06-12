from googletrans import Translator
import requests
from py2neo import Graph, Node
from time import time
import json
import re


def main():
    t1 = time()
    connection = connect_database()
    dataset = get_data()["tags"]
    insert_data(connection, dataset, "Ingredient", "name")
    print("Execution Time: ", time() - t1)


def connect_database():
    return Graph(
        host='54.173.133.27',
        port=33411,
        password='welds-symbols-saps'
    )


def get_data():
    return json.loads(requests.get('https://world.openfoodfacts.org/ingredients.json').text)


def insert_data(connection, dataset, label, attribute):
    for data in dataset:
        translated_data = filter_data(translate_data(data[attribute]).lower())

        ingredient = Node(label, name=translated_data)
        ingredient.__primarylabel__ = label
        ingredient.__primarykey__ = attribute

        connection.merge(ingredient)

        print(translated_data)


def translate_data(data):
    return Translator().translate(str(data), dest="pt").text


def filter_data(data):
    re_validation = re.findall(
        r"[a-zA-Záàâãéèêíïóôõöúçñ][^0-9]\w*", data, re.IGNORECASE)
    return " ".join(re_validation)


if __name__ == "__main__":
    main()
