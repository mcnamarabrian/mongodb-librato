import json
import pymongo
import sys

def fetch_mongo_version(conn):
    pass

if __name__ == '__main__':
    config_file = 'config.json'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    with open(config_file) as f:
        config = json.load(f)
        librato_client = librato.connect(config['librato']['user'], config['librato']['token'])
    connection = MongoClient('')


    from pymongo.mongo_client import MongoClient
connection = MongoClient('localhost', 27017)
db = connection['admin']
workingSetMetrics = db.command("serverStatus", "workingSet")


