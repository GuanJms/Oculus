import unittest
from data_system.containers.builders import QueuePipelineBuilder
from data_system.containers.cores import QueuePipeline

class TestQueuePipelineBuilder(unittest.TestCase):
    def test_build(self):
        builder = QueuePipelineBuilder()
        p = QueuePipeline()



if __name__ == "__main__":
    unittest.main()
