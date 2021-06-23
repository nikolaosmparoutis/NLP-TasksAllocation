from preprocess_datasets_interface import BuilderPreprocessDatasets


class DirectorOfData:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence.
    Executes the data pipeline of CSVs scanner.
    """

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> BuilderPreprocessDatasets:
        return self._builder

    @builder.setter
    def builder(self, builder):  # BuilderPreprocessDatasetsources
        self._builder = builder

    def build_preprocess_project(self, data_format):
        self.builder.filter_data(proj_id='id', keep_columns=['title', 'objective'])
        self.builder.dump_data(data_format = data_format)

    def build_preprocess_userdata(self, **data_metainfo):
        self.builder.filter_data(cache_file_preproc=data_metainfo['cache_file_preproc'],
                                 cache_file_bow=data_metainfo['cache_file_bow'])
        self.builder.dump_data(cache_file_preproc=data_metainfo['cache_file_preproc'],
                               cache_file_bow=data_metainfo['cache_file_bow'])
