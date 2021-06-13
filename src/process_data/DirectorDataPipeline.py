from ProcessDatasetInterface import FormalProcessDatasetInterface as BuilderProcessDatasources
from process_project_data import ConcreteBuilderProcessProjectData


class DirectorOfData:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence.
    Executes the data pipeline of CSVs scanner.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> BuilderProcessDatasources:
        return self._builder()

    @builder.setter
    def builder(self, builder: BuilderProcessDatasources):
        self._builder = builder

    def build_datapipeline_project(self):
        self.builder.client_load_datasource('xslx')
        self.builder.filter_data(proj_id='id', keep_columns=['title', 'objective'])
        self.builder.dump_data()

    def build_datapipeline_user(self):
        pass


director = DirectorOfData()
builder_project_data = ConcreteBuilderProcessProjectData()
director.builder = builder_project_data
