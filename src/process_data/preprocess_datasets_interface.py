import abc


class BuilderPreprocessDatasets(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'client_load_datasource') and
                callable(subclass.client_load_datasource) and
                hasattr(subclass, 'filter_data') and
                callable(subclass.filter_data) and
                hasattr(subclass, 'dump_data') and
                callable(subclass.dump_data) or
                NotImplemented)

    @abc.abstractmethod
    def client_load_datasource(self, data_format: str):
        """Get the client's choice for the dataset to load"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def filter_data(self):
        raise NotImplementedError

    @filter_data.setter
    @abc.abstractmethod
    def filter_data(self, **value: tuple):  # (column_id: str, keep_columns:list)
        """Responsible for actions as: Filtering the most iportant features,
        or Preprocessing data"""
        raise NotImplementedError

    @abc.abstractmethod
    def dump_data(self, **data_metainfo):
        """Dump preprocessed data"""
        raise NotImplementedError


