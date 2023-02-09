import geopandas
import rasterio
import shapely
from rasterio.mask import mask
from scipy.signal import convolve2d
from shapely.geometry import mapping
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from sklearn.ensemble import RandomForestClassifier

import contextily as cx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.utils import resample

from estaty.data.data import VectorData, RasterData
from estaty.stages import Stage, SPATIAL_DATA_LIST

import warnings
warnings.filterwarnings('ignore')

NO_DATA_FLAG = -10000.0
MIN_VALID_THRESHOLD = -10.0


class ExtendClarificationAnalysisStage(Stage):
    """
    Class to perform area calculation for objects into the defined area
    """

    def __init__(self, **params):
        super().__init__(**params)
        self.object_for_analysis = params['object_for_analysis']
        self.radius = self.object_for_analysis['radius']

        self.visualize = False
        if self.params.get('visualize') is not None:
            self.visualize = self.params.get('visualize')

    def apply(self, input_data: SPATIAL_DATA_LIST) -> VectorData:
        """
        Launch compatible analysis vector data with NDVI fields
        """
        # Take vector and raster data
        vector_data, raster_data = self.determine_vector_raster(input_data)
        full_area = list(vector_data.area_of_interest_as_dataframe['geometry'])
        full_geometry = [mapping(geometry) for geometry in full_area]

        # Extract values from raster using vector data
        geometries = list(vector_data.polygons['geometry'])
        geometry = [mapping(geometry) for geometry in geometries]

        # It's important not to set crop as True because it distort output
        with rasterio.open(raster_data.raster) as src:
            out_image, i = mask(src, full_geometry, crop=False, nodata=NO_DATA_FLAG)
            extracted_full_area = out_image[0, :, :]

            out_image, i = mask(src, geometry, crop=False, nodata=NO_DATA_FLAG)
            extracted_geometries = out_image[0, :, :]

        # Clip images to speed up calculation
        non_empty_indices = np.argwhere(extracted_full_area > MIN_VALID_THRESHOLD)
        row_ids = non_empty_indices[:, 0]
        col_ids = non_empty_indices[:, 1]
        # TODO add indices out of extend control mechanism
        left_border = min(col_ids) - 10
        right_border = max(col_ids) + 10
        bottom_border = min(row_ids) - 10
        top_border = max(row_ids) + 10

        # Get small samples
        extracted_full_area = extracted_full_area[bottom_border:top_border,
                              left_border: right_border]
        extracted_geometries = extracted_geometries[bottom_border:top_border,
                               left_border: right_border]

        # Create matrix where 1 is data we want to predict and 0 - no data
        target_matrix = np.zeros(extracted_geometries.shape)
        target_matrix[extracted_geometries > MIN_VALID_THRESHOLD] = 1

        # Apply conv and generate features matrices
        source_sample = pd.DataFrame({'"Зеленые зоны" по данным OSM': np.ravel(target_matrix),
                                      'NDVI значение': np.ravel(extracted_full_area)})
        for col in source_sample.columns:
            source_sample = source_sample[source_sample[col] > MIN_VALID_THRESHOLD]

        non_parks = source_sample[source_sample['"Зеленые зоны" по данным OSM'] == 0]
        parks = source_sample[source_sample['"Зеленые зоны" по данным OSM'] == 1]
        ndvi_non_parks = np.array(non_parks['NDVI значение'])
        ndvi_parks = np.array(parks['NDVI значение'])
        th = (np.median(ndvi_non_parks) + np.median(ndvi_parks)) / 2
        print(th)

        # Determine threshold
        if self.visualize:
            with sns.axes_style('darkgrid'):
                sns.histplot(data=source_sample,
                             hue='"Зеленые зоны" по данным OSM',
                             x="NDVI значение", kde=True)
                line = [0, 600]
                plt.plot([np.median(ndvi_non_parks), np.median(ndvi_non_parks)], line, c='blue', linewidth=1.5)
                plt.plot([np.median(ndvi_parks), np.median(ndvi_parks)], line, c='orange', linewidth=1.5)
                plt.plot([th, th], line, c='black', linewidth=2)
                plt.show()

        if self.visualize:
            # Generate plot with comparison source geometries and other
            masked_array = np.ma.masked_where(extracted_full_area < MIN_VALID_THRESHOLD,
                                              extracted_full_area)

            fig_size = (18, 6.0)
            fig, axs = plt.subplots(1, 3, figsize=fig_size)

            cmap_ndvi = cm.get_cmap('RdYlGn')
            cmap_ndvi.set_bad(color='#C0C0C0')
            cmap_extend = cm.get_cmap('gray')
            cmap_extend.set_bad(color='#ffffff00')

            axs[0].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[0].imshow(np.ma.masked_where(target_matrix < 0.5,
                                             target_matrix),
                          interpolation='nearest', cmap=cmap_extend, alpha=1.0)
            axs[0].set_title('Геометрии "зеленых зон" по данным OSM')

            target_matrix[extracted_full_area >= th] = 1

            axs[1].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[1].imshow(np.ma.masked_where(target_matrix < 0.5,
                                             target_matrix),
                          interpolation='nearest', cmap=cmap_extend, alpha=1.0)

            axs[1].set_title('Расширенные границы "зеленых зон"')

            surf = axs[2].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[2].set_title('Значения NDVI')
            cb = fig.colorbar(surf, shrink=0.8, aspect=22)
            plt.show()

            #######################################
            # Different thresholds visualizations #
            #######################################
            masked_array = np.ma.masked_where(extracted_full_area < MIN_VALID_THRESHOLD, extracted_full_area)

            fig_size = (18, 6.0)
            fig, axs = plt.subplots(1, 3, figsize=fig_size)

            cmap_ndvi = cm.get_cmap('RdYlGn')
            cmap_ndvi.set_bad(color='#C0C0C0')
            cmap_extend = cm.get_cmap('gray')
            cmap_extend.set_bad(color='#ffffff00')

            first_matrix = np.ma.masked_where(masked_array < 0.15, masked_array)
            first_matrix[first_matrix >= 0.15] = 1
            axs[0].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[0].imshow(first_matrix,
                          interpolation='nearest', cmap=cmap_extend, alpha=1.0)
            axs[0].set_title('Порог 0.15')

            target_matrix[extracted_full_area >= th] = 1

            second_matrix = np.ma.masked_where(masked_array < 0.2, masked_array)
            second_matrix[second_matrix >= 0.2] = 1
            axs[1].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[1].imshow(second_matrix,
                          interpolation='nearest', cmap=cmap_extend, alpha=1.0)
            axs[1].set_title('Порог 0.2')

            third_matrix = np.ma.masked_where(masked_array < 0.25, masked_array)
            third_matrix[third_matrix >= 0.25] = 1
            axs[2].imshow(masked_array, interpolation='nearest', cmap=cmap_ndvi)
            axs[2].imshow(third_matrix,
                          interpolation='nearest', cmap=cmap_extend, alpha=1.0)
            axs[2].set_title('Порог 0.25')
            plt.show()
        else:
            target_matrix[extracted_full_area >= th] = 1

        # Create polygons based on defined matrices
        updated_geometries = get_polygons_from_raster(raster_data, bottom_border,
                                                      top_border, left_border,
                                                      right_border, target_matrix)

        return VectorData(polygons=updated_geometries, epsg=vector_data.epsg,
                          area_of_interest=vector_data.area_of_interest)

    @staticmethod
    def determine_vector_raster(input_data: SPATIAL_DATA_LIST):
        """
        Search for and grab vector data and raster datasets for further
        analysis
        """
        vectors = list(filter(lambda x: isinstance(x, VectorData), input_data))
        rasters = list(filter(lambda x: isinstance(x, RasterData), input_data))

        return vectors[0], rasters[0]


def get_polygons_from_raster(raster_data: RasterData,
                             bottom_border: int, top_border: int,
                             left_border: int, right_border: int,
                             target_matrix: np.ndarray):
    """
    Create vector object based on raster values. Vectorize only extend without
    values extraction

    :param raster_data: raster dataset to copy metadata from it
    :param bottom_border: bottom index of target matrix to insert into raster
    :param top_border: top index of target matrix to insert into raster
    :param left_border: left index of target matrix to insert into raster
    :param right_border: right index of target matrix to insert into raster
    :param target_matrix: matrix to insert into raster and then vectorize full
    image
    """
    with rasterio.open(raster_data.raster) as src:
        current_ndvi_field = src.read(1)
        upd_field = np.zeros(current_ndvi_field.shape)
        upd_field[bottom_border:top_border, left_border: right_border] = target_matrix
        upd_field = upd_field.astype(np.int16)

        shapes = rasterio.features.shapes(upd_field, mask=upd_field > 0.5,
                                          transform=src.transform)
        pol = list(shapes)
        geom = [shapely.geometry.shape(i[0]) for i in pol]
        geom = geopandas.GeoSeries(geom, crs=src.crs)
        updated_geometries = geopandas.GeoDataFrame({'geometry': geom})

    return updated_geometries
