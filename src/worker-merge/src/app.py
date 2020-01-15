#
# By Kaj Nygren, Alexander Ekström, Erik Dahlberg
# December 2019
from merge.Merge import Merge

if __name__ == '__main__':
    #pubsub = SubHandler()
    #print("kalle")
    merge = Merge()
    merge.start_rabbitMQ()
