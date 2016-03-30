

# MongoDB &rarr; Librato

Publishes statistics from MongoDB's serverstatus to Librato.  This code is compatible with MongoDB 3.x, not 2.x.

This code is strongly influenced by [6wunderkinder's postgres-librato code](https://github.com/6wunderkinder/postgres-librato).


## Features

Compatible with MongoDB 3.2.

Exposes the following stats:

 - `mongodb.connections` - gauge
 - `mongodb.network` - counter
 - `mongodb.mem` - gauge
 - `mongodb.asserts` - counter
 - `mongodb.globalLock.totalTime` - counter
 - `mongodb.globalLock.activeClients` - gauge
 - `mongodb.globalLock.currentQueue` - gauge

## Setup (Ubuntu)

```bash
$ sudo apt-get -q -y install python-pip
$ sudo pip install -r requirements.txt
```

## Related Work

 - [MongoDB serverStatus](https://docs.mongodb.org/manual/reference/command/serverStatus/)
 