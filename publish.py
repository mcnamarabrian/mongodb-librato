import json
import librato
import pymongo
import sys
import time

def get_asserts(server_status):
    return server_status['asserts']

def get_connections(server_status):
    return server_status['connections']

def get_globallock(server_status):
    return server_status['globalLock']

def get_locks(server_status):
    return server_status['locks']

def get_mem(server_status):
    return server_status['mem']

def get_network(server_status):
    return server_status['network']

def get_uptime(server_status):
    return server_status['uptime']

def publish_forever(config, librato_client):
    while True:
        q = librato_client.new_queue()
        for db in config['databases']:
            source = db['librato_source']
            rs_string = 'mongodb://{}/?replicaSet={}'.format(db['hosts'], db['replica_set'])
            try:
                conn = pymongo.MongoClient(rs_string)
                conn.admin.authenticate(db['user'], db['password'])
            except Exception as e:
                print repr(e)
                sys.exit(1)

            database = conn[db['name']]

            try:
                server_status = database.command('serverStatus')
            except pymongo.errors.OperationFailure as e:
                print 'Error: {}'.format(str(e))

            uptime = get_uptime(server_status)
            connections = get_connections(server_status)
            network = get_network(server_status)
            mem = get_mem(server_status)
            asserts = get_asserts(server_status)
            global_lock = get_globallock(server_status)
            locks = get_locks(server_status)

            print 'Uptime (sec): {}'.format(uptime)
            print
            q.add('mongodb.uptime', uptime, source=source)

            for name, value in connections.items():
                q.add('mongodb.connections.' + name, value, description=name, source=source)

            for name, value in network.items():
                q.add('mongodb.network.' + name, value, type='counter', description=name, source=source)

            for name, value in mem.items():
                # Only publish numeric values - a bool may be present
                if type(value) == bool:
                    continue
                q.add('mongodb.mem.' + name, value, source=source)

            for name, value in asserts.items():
                q.add('mongodb.asserts.' + name, value, type='counter', description=name, source=source)

            for name, value in global_lock.items():
                # The globalLock dict will have nested dicts
                if type(value) == dict:
                    for nested_name, nested_value in value.items():
                        q.add('mongodb.globalLock.' + name + '.' + nested_name, nested_value, source=source)
                else:
                    q.add('mongodb.globalLock.' + name, value, type='counter', description=name, source=source)

        q.submit()

        time.sleep(config['sample_rate'])


if __name__ == '__main__':
    config_file = 'config.json'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    with open(config_file) as f:
        config = json.load(f)
        librato_client = librato.connect(config['librato']['user'], config['librato']['token'])

    publish_forever(config, librato_client)
