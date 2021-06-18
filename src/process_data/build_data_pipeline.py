from director_data_pipeline import DirectorOfData
from builder_preprocess_dataset import BuilderPreprocessProjects
from builder_preprocess_userdata import BuilderPreprocessUsers

if __name__ == "__main__":
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """

    datasets_name_list = ['Projects_datasets.xlsx', 'Projects2.xlsx']
    files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw'
    path_data_internal = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal'
    path_data_internal_txt = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal/txt/'

    director = DirectorOfData()
    builder_preprocess_dataset = BuilderPreprocessProjects(
        datasets_name_list,
        files_path,
        path_data_internal,
        path_data_internal_txt
    )
    director.builder = builder_preprocess_dataset
    director.build_preprocess_data_pipeline(data_format='xslx')

    builder_preprocess_userdata = BuilderPreprocessUsers() #TODO
    director.build_preprocess_userdata()# TODO
