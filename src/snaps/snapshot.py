
import os
import json
import datetime
import logging
from hashlib import md5
from prettytable import PrettyTable


class Snapshot:

    def __init__(self, file):

        self.file = file
        self.snapshot_dict = {}
        self.logger = logging.getLogger()
        
        self.logger.info("Initializing snapshot.")

        try:
            with open("{}.snap".format(self.file), 'r') as db:
                self.snapshot_dict = json.load(fp=db)
        except IOError:
            self.logger.info("Creating 1st snapshot.")
            self.rev_cnt = 0
        else:
            self.logger.info("Found existing snapshot.")            
            self.rev_cnt = len(self.snapshot_dict)

        # build version index
        self.version_indx = {}
        for (chksum, snapshot) in self.snapshot_dict.iteritems():
            self.version_indx[snapshot['VERSION']] = chksum

    def create(self):

        with open(self.file, 'r') as rfile:
            content = rfile.readlines()

        # Get content checksum
        chksum = self._get_checksum(content)

        # If change since last snapshot
        if chksum not in self.snapshot_dict.keys():

            self.logger.info("Creating snapshot.")            
            
            self.rev_cnt = self.rev_cnt + 1
            
            self.snapshot_dict[chksum] = {
                'VERSION' : str(self.rev_cnt),
                'DATE-TIME' : str(datetime.datetime.now()),
                'CONTENT' : content
            }

            with open(self.file + '.snap', 'w') as db:
                json.dump(self.snapshot_dict, db)

            self.logger.info("Snapshot [r{}:{}] Created succesfully.".format(new_rev, chksum))  

        else:
            self.logger.info("Snapshot up to date.")  

    def restore(self, version):

        if not version:
            version = self.rev_cnt

        self.logger.info("Checking snapshot.")     

        if version in self.version_indx.keys():
            k = self.version_indx[version]

            snapshot = self.snapshot_dict[k]

            self.logger.info("Dumping snapshot [r{}:{}].".format(snapshot['VERSION'], snapshot['DATE-TIME']))

            with open("{}.r{}".format(self.file, snapshot['VERSION']), 'w') as wfile:
                for line in snapshot['CONTENT']:
                    wfile.write(line)

            self.logger.info("Dump successful.")

        else:
            self.logger.info("Could not find requested version.")

    def tabulate(self):

        table = PrettyTable(['Rev', 'Datetime', 'Checksum'])

        l = self.version_indx.keys()
        l.sort()

        for rev in l:

            chksum = self.version_indx[rev]
            snapshot = self.snapshot_dict[chksum]
            datetime = snapshot['DATE-TIME']

            table.add_row([rev, datetime, chksum])

        return "\n{}".format(table)

    def _get_checksum(self, content):

        return md5(''.join(content)).hexdigest()




















