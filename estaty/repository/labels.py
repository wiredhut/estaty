from estaty.data_source.load.gbif_vector import LoadGBIFLocallyStage
from estaty.data_source.load.osm_vector import LoadOSMStage
from estaty.preprocessing.project import VectorProjectionStage

DATA_SOURCE_POOL_BY_NAME = {'osm': [LoadOSMStage],
                            'gbif_local': [LoadGBIFLocallyStage],
                            'reproject': VectorProjectionStage}
