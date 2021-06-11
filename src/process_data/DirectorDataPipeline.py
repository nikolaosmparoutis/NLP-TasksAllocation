from ProcessDatasetInterface import FormalProcessDatasetInterface as BuilderProcessDatasources


class DirectorOfData:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. Executes the data pipeline of CSVs scanner.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> BuilderProcessDatasources:

        return self._builder()

    @builder.setter
    def builder(self, builder: BuilderProcessDatasources) -> None:
        self._builder = builder

    def build_datapipeline_project(self) -> None:
        self.builder.client_process()
        self.builder.read_CSVs()
        self.builder.produce_part_c()

    def build_datapipeline_csv(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()
