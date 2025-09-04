from unittest_extensions import TestCase, args

from micromanager.tests.integration.runner import run


class TestMicromanager(TestCase):
    def subject(self, input, compose_teardown=True):
        response = run(input, compose_teardown=compose_teardown)
        return response.output

    def assert_in_result(self, result_str):
        self.assertIn(result_str, self.result())

    @args("start")
    def test_start_no_arguments(self):
        self.assert_in_result("Started projects:")

    @args(["start", "payments"])
    def test_start_with_argument(self):
        self.assert_in_result("Started projects: ['payments']")

    @args(["start", "payments", "customers"])
    def test_start_with_multiple_arguments(self):
        self.assert_in_result("Started projects: ['payments', 'customers']")

    @args("stop")
    def test_stop_without_starting(self):
        self.assert_in_result("Stopped projects:")

    def test_stop_all_started_services(self):
        run("start", compose_teardown=False)
        response = run("stop")
        self.assertIn("Stopped projects:", response.output)

    @args(["stop", "payments"])
    def test_stop_with_argument(self):
        self.assert_in_result("Stopped projects: ['payments']")

    @args(["stop", "payments", "customers"])
    def test_stop_with_multiple_arguments(self):
        self.assert_in_result("Stopped projects: ['payments', 'customers']")

    def test_stop_started_services_with_argument(self):
        run("start", compose_teardown=False)
        response = run(["stop", "payments"])
        self.assertIn("Stopped projects: ['payments']", response.output)

    @args(["use", "social-media-platform"], compose_teardown=False)
    def test_use(self):
        self.assert_in_result("Using system: social-media-platform")

    @args(["use", "eshop"], compose_teardown=False)
    def test_use_current_system(self):
        self.assert_in_result("Using system: eshop")
