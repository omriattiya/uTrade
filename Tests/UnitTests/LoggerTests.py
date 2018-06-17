import os
import unittest

from DatabaseLayer import Logger
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import LoggerLogic, UsersLogic
from SharedClasses.RegisteredUser import RegisteredUser


class LoggerTests(unittest.TestCase):
    def setUp(self):
        init_database(DB_NAME)

    def test_add_event(self):
        self.assertTrue(LoggerLogic.add_event_log("omri", "open shop"))
        logs = Logger.get_all_event_logs()
        self.assertTrue(len(logs) == 1)
        event_log = logs[0]
        self.assertEqual(event_log.username, "omri")
        self.assertEqual(event_log.event, "open shop")

    def test_get_all_events(self):
        LoggerLogic.add_event_log("omri", "open shop")
        LoggerLogic.add_event_log("omri2", "payAll")
        logs = Logger.get_all_event_logs()
        self.assertTrue(len(logs) == 2)
        event_log = logs[1]
        self.assertEqual(event_log.username, "omri")
        self.assertEqual(event_log.event, "open shop")
        event_log = logs[0]
        self.assertEqual(event_log.username, "omri2")
        self.assertEqual(event_log.event, "payAll")

    def test_get_events_by_event(self):
        LoggerLogic.add_event_log("omri", "open shop")
        LoggerLogic.add_event_log("omri2", "payAll")
        logs = Logger.get_event_logs_by_event("open shop")
        self.assertTrue(len(logs) == 1)
        event_log = logs[0]
        self.assertEqual(event_log.username, "omri")
        self.assertEqual(event_log.event, "open shop")
        logs = Logger.get_event_logs_by_event("payAll")
        self.assertTrue(len(logs) == 1)
        event_log = logs[0]
        self.assertEqual(event_log.username, "omri2")
        self.assertEqual(event_log.event, "payAll")

    def test_add_error(self):
        self.assertTrue(LoggerLogic.add_error_log("omri", "open shop", "shop name already exists"))
        logs = Logger.get_all_error_logs()
        self.assertTrue(len(logs) == 1)
        error_log = logs[0]
        self.assertEqual(error_log.username, "omri")
        self.assertEqual(error_log.event, "open shop")
        self.assertEqual(error_log.additional_details, "shop name already exists")

    def test_get_all_errors(self):
        LoggerLogic.add_error_log("omri", "open shop", "shop name already exists")
        LoggerLogic.add_error_log("omri2", "payAll", "error in pay")

        logs = Logger.get_error_logs_by_event("open shop")
        self.assertTrue(len(logs) == 1)
        error_log = logs[0]
        self.assertEqual(error_log.username, "omri")
        self.assertEqual(error_log.event, "open shop")
        self.assertEqual(error_log.additional_details, "shop name already exists")

        logs = Logger.get_error_logs_by_event("payAll")
        self.assertTrue(len(logs) == 1)
        error_log = logs[0]
        self.assertEqual(error_log.username, "omri2")
        self.assertEqual(error_log.event, "payAll")
        self.assertEqual(error_log.additional_details, "error in pay")

    def test_get_errors_by_event(self):
        LoggerLogic.add_error_log("omri", "open shop", "shop name already exists")
        LoggerLogic.add_error_log("omri2", "payAll", "error in pay")
        logs = Logger.get_error_logs_by_event("open shop")
        self.assertTrue(len(logs) == 1)
        error_log = logs[0]
        self.assertEqual(error_log.username, "omri")
        self.assertEqual(error_log.event, "open shop")
        logs = Logger.get_error_logs_by_event("payAll")
        self.assertTrue(len(logs) == 1)
        error_log = logs[0]
        self.assertEqual(error_log.username, "omri2")
        self.assertEqual(error_log.event, "payAll")

    def test_add_login(self):
        UsersLogic.register(RegisteredUser("user1user1", "13245678"))
        self.assertTrue(LoggerLogic.add_login_log("user1user1"))
        logs = Logger.get_all_login_logs()
        self.assertTrue(len(logs) == 1)
        login_log = logs[0]
        self.assertEqual(login_log.username, "user1user1")

    def test_get_all_logging(self):
        UsersLogic.register(RegisteredUser("user1user1", "13245678"))
        UsersLogic.register(RegisteredUser("user2user2", "13245678"))

        LoggerLogic.add_login_log("user1user1")
        LoggerLogic.add_login_log("user2user2")
        logs = Logger.get_all_login_logs()
        self.assertTrue(len(logs) == 2)
        login_log = logs[1]
        self.assertEqual(login_log.username, "user1user1")
        login_log = logs[0]
        self.assertEqual(login_log.username, "user2user2")

    def test_add_security(self):
        self.assertTrue(LoggerLogic.add_security_log("sql injection", "event1"))
        logs = Logger.get_all_security_logs()
        self.assertTrue(len(logs) == 1)
        security_log = logs[0]
        self.assertEqual(security_log.event, "sql injection")
        self.assertEqual(security_log.additional_details, "event1")

    def test_get_all_security(self):
        LoggerLogic.identify_sql_injection("#", "event1")
        LoggerLogic.identify_sql_injection("'SELECT * FROM Items;--", "event2")
        logs = Logger.get_all_security_logs()
        self.assertTrue(len(logs) == 2)
        security_log = logs[1]
        self.assertEqual(security_log.event, "event1")
        security_log = logs[0]
        self.assertEqual(security_log.event, "event2")

    def tearDown(self):
        os.remove(DB_NAME)


if __name__ == '__main__':
    unittest.main()

DB_NAME = 'db.sqlite3'
