from django.test import TestCase

# Create your tests here.


class DummySuccessTest(TestCase):
    def test_always_succeeds(self):

        self.assertTrue(True, "This should always pass!")
