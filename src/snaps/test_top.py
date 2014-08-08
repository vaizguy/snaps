
import unittest
import logging
import sys
from tests import test_differ

if __name__ == '__main__':

    # Get logger
    logging_format = logging.Formatter("[%(levelname)s] %(message)s")
    mod_logger = logging.getLogger()
    mod_logger.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(logging_format)
    mod_logger.addHandler(log_handler)


    # Init test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(test_differ.TestDiffContentFunctions)
    # Run test suite
    mod_logger.info("Begining Test Suite Run.")    
    unittest.TextTestRunner(verbosity=2).run(suite)
    mod_logger.info("Ended Test Suite Run.")

