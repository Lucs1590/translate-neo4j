from translation import google
import requests
from py2neo import Graph, Node


def main():
    connect_database()
    data = get_data()
    insert_data(data)


def connect_database():
    ...


def get_data():
    ...


def insert_data(data):
    ...


if __name__ == "__main__":
    main()