from ._container_builder import ContainerBuilder


class QueuePipelineBuilder(ContainerBuilder):

    def build(self, container, **kwargs):
        raise NotImplementedError
