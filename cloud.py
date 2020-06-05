from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pandas import DataFrame
from string import Template
from os import getcwd

path_to_bundle = Template('${current_dir}\secure-connect-cassandra-test.zip').substitute(current_dir=getcwd())

cloud_config = {
  'secure_connect_bundle': path_to_bundle
}

auth_provider = PlainTextAuthProvider('ob3_test', 'oceanbrowser')

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('ob3')
