#! /home/aananth/bin/python2.7

from snapshot import Snapshot


class Snappy:

    def __init__(self):

        self.logger = logging.getLogger()

    def create_snapshot(self, file):

        if not file:
            self.logger.info("Please enter a valid filename.")
            return None

        s = Snapshot(file)
        s.create()

    def restore_snapshot(self, file, version):

        if not file:
            self.logger.info("Please enter a valid filename.")
            return None

        if not version:
            self.logger.info("Please enter a valid version.")
            return None

        s = Snapshot(file)
        s.restore(version)


if __name__ == '__main__':

    import argparse
    import logging

    logging_format = logging.Formatter("[%(levelname)s] %(message)s")
    mod_logger = logging.getLogger()
    mod_logger.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(logging_format)
    mod_logger.addHandler(log_handler)

    parser = argparse.ArgumentParser()

    ## Variables
    # File
    parser.add_argument("--file", help="Create snapshot of file.")
    # Revision
    parser.add_argument("--rev", help="Revision of snapshot.")

    ## Actions
    # Create snapshot
    parser.add_argument("--snap", help="Create snapshot of file.", action="store_true")
    # Get snapshot
    parser.add_argument("--restore", help="Get file snapshot of given version.", action="store_true")

    args = parser.parse_args()

    # Initialize tool
    S = Snappy()

    if args.snap:
        S.create_snapshot(args.file)

    elif args.restore:
        args.rev = int(args.rev)
        S.restore_snapshot(args.file, args.rev)


