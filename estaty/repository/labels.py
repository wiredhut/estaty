from estaty.analysis.stages.area import AreaAnalysisStage
from estaty.analysis.stages.extend_clarification import \
    ExtendClarificationAnalysisStage
from estaty.data_source.load.vector_csv import LoadCsvVectorStage
from estaty.data_source.load.landsat_raster import NDVILandsatLocallyStage
from estaty.data_source.load.osm_vector import LoadOSMStage
from estaty.merge.vector_merge import VectorDataMergingStage
from estaty.preprocessing.stages.project import CommonProjectionStage
from estaty.analysis.stages.distance import DistanceAnalysisStage
from estaty.stages import DummyStage


DATA_SOURCE_POOL_BY_NAME = {'osm': [LoadOSMStage],
                            'csv': [LoadCsvVectorStage],
                            'ndvi_local': [NDVILandsatLocallyStage],
                            'reproject': CommonProjectionStage,
                            'vector': VectorDataMergingStage,
                            'distance': DistanceAnalysisStage,
                            'area': AreaAnalysisStage,
                            'extend_clarification': ExtendClarificationAnalysisStage,
                            'dummy': DummyStage,
                            'stdout': None}
