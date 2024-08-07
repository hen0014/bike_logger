import unittest
from log_config import LogConfig
import logging

class TestLogConfig(unittest.TestCase):
    def setUp(self):
        self.log_config = LogConfig()

    def test_init(self):
        self.assertEqual(self.log_config.config_file, "log_config.yaml")
        self.assertIsInstance(self.log_config.default_config, dict)
        self.assertIn('version', self.log_config.default_config)
        self.assertIn('formatters', self.log_config.default_config)
        self.assertIn('handlers', self.log_config.default_config)
        self.assertIn('root', self.log_config.default_config)
        
    def test_get_logger(self):
        logger = self.log_config.get_logger()
        self.assertIsInstance(logger, logging.Logger)
if __name__ == '__main__':
    unittest.main()