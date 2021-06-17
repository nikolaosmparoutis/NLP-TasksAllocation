from preprocess_datasets_interface import BuilderPreprocessDataset as BuilderPreprocessDatasetsources
from builder_preprocess_dataset import BuilderPreprocessDataset

class DirectorOfData:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence.
    Executes the data pipeline of CSVs scanner.
    """

    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        return self._builder()

    @builder.setter
    def builder(self, builder):  # BuilderPreprocessDatasetsources
        self._builder = builder

    def build_preprocess_dataset(self):
        data_format = 'xlsx'
        self.builders.client_load_datasource(data_format)
        self.builders.filter_data(proj_id='id', keep_columns=['title', 'objective'])
        self.builders.dump_data(data_format)

    def build_datapipeline_user(self):
        pass


director = DirectorOfData()
builder_project_data = BuilderPreprocessDataset(datasets_name_list,
                                                files_path,
                                                path_data_internal,
                                                path_data_internal_txt)
director.builder = builder_project_data
