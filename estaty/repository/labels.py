from estaty.data_source.load.gbif_vector import LoadGBIFLocallyStage
from estaty.data_source.load.osm_vector import LoadOSMStage

DATA_SOURCE_POOL_BY_NAME = {'osm': [LoadOSMStage],
                            'gbif_local': [LoadGBIFLocallyStage]}
