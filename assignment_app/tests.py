from django.test import TestCase

# NOTE: All tests must start with the word 'test'

# TODO: Delete this class once we have actual tests, only needed to make sure github actions works
class InitialTest(TestCase):

  def setUp(self):
        x = 1
        y = 1
    
  def test_one_equals_one(self):
        self.assertEqual(1, 1)