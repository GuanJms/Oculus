import unittest
from data_system.utils.frequency_limiter import FrequencyLimiter

class MyTestFrequencyLimiter(unittest.TestCase):

    def setUp(self):
        # Set up the frequency limiter
        self.l = FrequencyLimiter()

    def test_frequency_limiter(self):
        # Test the frequency limiter
        self.assertFalse(self.l.is_limited("test"))
        self.l.update("test", timestamp=0)
        self.assertTrue(self.l.is_limited("test", timestamp=1))
        self.assertFalse(self.l.is_limited("test", timestamp=2000))
        self.l.update("test", timestamp=2000)
        self.assertTrue(self.l.is_limited("test", timestamp=2001))

        self.l.set_update_frequency(99999999999999999999)
        for i in range(100):
            time = i * 1000
            self.assertTrue(self.l.is_limited("test", timestamp=time))



if __name__ == "__main__":
    unittest.main()
