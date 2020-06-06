from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from os import getcwd
from os import path

path_to_bundle = path.join(getcwd(), 'secure-connect-cassandra-test.zip')
  
cloud_config = {
  'secure_connect_bundle': path_to_bundle
}

auth_provider = PlainTextAuthProvider('ob3_test', 'oceanbrowser')

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('ob3')
