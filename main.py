import requests
from py2neo import Graph, Node
from time import time
import json
import re
from multiprocessing import Pool
import functools


def main():
    pool = Pool(4)
    t1 = time()
    dataset = get_data(
        'https://world.openfoodfacts.org/ingredients.json')["tags"]

    with Pool(processes=4) as pool:
        nargs = [n for n in dataset]
        print(nargs[0])
        pool.map(insert_data, nargs)

    print("Execution Time: ", time() - t1)


def connect_database():
    return Graph(
        host='54.173.133.27',
        port=33411,
        password='welds-symbols-saps'
    )


def get_data(url, type_request="GET", headers={}, querystring={}):
    response = requests.request(
        type_request, url, headers=headers, params=querystring)
    return json.loads(response.text)


def insert_data(data):
    label = "Ingredient"
    attribute = "name"
    translated_data, english = translate_data(data[attribute])

    if translate_data != " ":
        ingredient = Node(label, name=translated_data, english=english) if english == True else Node(
            label, name=translated_data)
        ingredient.__primarylabel__ = label
        ingredient.__primarykey__ = attribute

        connect_database().merge(ingredient)

        print(translated_data)


def translate_data(data):
    data = filter_data(data)
    url = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com/translation/text/translate"
    querystring = {"source": "en", "target": "pt", "input": data}
    headers = {
        'x-rapidapi-host': "systran-systran-platform-for-language-processing-v1.p.rapidapi.com",
        'x-rapidapi-key': "b2448ece4bmsh2e999bf748c5de3p1b0cb4jsn39b94190ee41"
    }
    translated_data = get_data(url, "GET", headers, querystring)
    try:
        return str(translated_data["outputs"][0]["output"]).lower(), False
    except:
        return data.replace("%20", " "), True


def filter_data(data):
    re_validation = re.findall(
        r"[a-zA-Záàâãéèêíïóôõöúçñ][^0-9]\w*", data, re.IGNORECASE)
    return " ".join(re_validation).lower()


if __name__ == "__main__":
    main()
