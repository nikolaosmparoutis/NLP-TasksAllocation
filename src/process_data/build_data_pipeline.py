from director_data_pipeline import DirectorOfData
from builder_preprocess_dataset import BuilderPreprocessProjects
from builder_preprocess_userdata import BuilderPreprocessUsers

if __name__ == "__main__":
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """
    director = DirectorOfData()

    datasets_name_list = ['Projects_datasets.xlsx', 'Projects2.xlsx'],
    files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw',
    path_data_internal = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal',
    path_data_internal_txt = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal/txt/'

    builder_preprocess_projects = BuilderPreprocessProjects(
        datasets_name_list, files_path, path_data_internal, path_data_internal_txt
    )
    director.builder = builder_preprocess_projects
    director.build_preprocess_project(data_format='xslx',
                                      proj_id='id',
                                      keep_columns=['title', 'objective']
                                      )

    txt_data_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/external/txt',
    cache_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/final_processed',
    utils_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/utils'

    builder_preprocess_userdata = BuilderPreprocessUsers(
        txt_data_dir, cache_dir, utils_dir
    )
    director.builder = builder_preprocess_userdata
    director.build_preprocess_userdata(
        cache_file_preproc="preprocessed_data.pkl",
        vocabulary_size=1000,   # most 1000 frequent words
        cache_file_bow='bow_features.pkl')
