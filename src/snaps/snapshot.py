
import os
import json
import zlib
import datetime
import logging


class Snapshot:

    def __init__(self, file):

        self.file = file
        self.snapshot_dict = {}
        self.logger = logging.getLogger()

        try:
            with open("{}.snap".format(self.file), 'r') as db:
                self.snapshot_dict = json.load(fp=db)
        except IOError:
            self.logger.info("Initial snapshot.")
            self.rev_cnt = 0
        else:
            self.logger.info("Found existing snapshot.")            
            self.rev_cnt = len(self.snapshot_dict)

        # build version index
        self.version_indx = {}
        for (a32c, snapshot) in self.snapshot_dict.iteritems():
            self.version_indx[snapshot['VERSION']] = a32c

    def create(self):

        self.logger.info("Creating snapshot.")            

        with open(self.file, 'r') as rfile:
            content = rfile.readlines()

        a32chksum = zlib.adler32(''.join(content))

        new_rev = self.rev_cnt + 1

        self.snapshot_dict[a32chksum] = {
                'VERSION' : new_rev,
                'DATE-TIME' : str(datetime.datetime.now()),
                'CONTENT' : content
        }

        with open(self.file + '.snap', 'w') as db:
            json.dump(self.snapshot_dict, db)

        self.logger.info("Snapshot [r{}:{}] Created succesfully.".format(new_rev, a32chksum))  


    def restore(self, version):

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




















