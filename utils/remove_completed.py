#!/usr/bin/env python
#
# This simple script removes completed torrents from Transmission (without deleting their data)
#

import os
import sys

import transmissionrpc
from transmissionrpc.error import TransmissionError


def main():
    try:
        client = transmissionrpc.Client(address=os.environ.get('TRANSMISSION_ADDRESS', 'localhost'), 
                                        port=int(os.environ.get('TRANSMISSION_PORT', '9091')), 
                                        user=os.environ.get('TRANSMISSION_USER'), 
                                        password=os.environ.get('TRANSMISSION_PASSWORD'))
    except TransmissionError as e:
        print 'Unable to create Transmission client ({})'.format(str(e))
        sys.exit(1)
    torrents_to_remove = [t.id for t in client.get_torrents() if t.progress == 100.0]

    if torrents_to_remove:
        print 'Removing {} torrents'.format(str(len(torrents_to_remove)))
        client.remove_torrent(ids=torrents_to_remove, delete_data=False)
    else:
        print 'No completed torrents found'


if __name__ == '__main__':
    main()
