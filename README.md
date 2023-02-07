<img src="./docs/media/estaty_logo.png" width="750"/>

Module for spatial data fusion and processing for real estate objects.
**estaty** is Python-based platform to obtain and merge open spatial data with not very open and not very spatial to create “real estate use cases”.
Library provide tools for loaded data merging, pairwise source verification, proximity analysis, etc. 

## Documentation 

### Brief dive into spatial data processing

The variety of spatial data can be reduced to two large groups: raster and vector. 
Vector data can be presented as follows: point data, lines, polygons (Figure 1). So, 
**estaty** reduces completely all assimilated data to the following four types.

<img src="./docs/media/spatial_data.png" width="650"/>

Figure 1. Possible types of spatial data

The module thus downloads spatial data in just 
four formats (1 raster fields and 3 vector). The module is 
designed so that the most important parts are isolated from each other 
(multi-layer architecture). The DataSource layer is responsible for loading 
and generalising the data. So, there are exists the following 5 layers: 

- `DataSource`  - load and cache data,  reduce data to known and commonly used types;
- `Preprocessor` - preprocessing operation to prepare data for merging. For example, assign new CRS (re-projection);
- `Merger`  - merge raster and vector data if it is required;
- `Analyzer` - core of the system - use simple data representations and primitives to constract sequential analysis pipelines;
- `Report` - submodule for preparing PDF reports, data visualization and data send operations (for example POST request to desired service)

All above submodules can be flexibly configured to create custom data analysis pipelines:

<img src="./docs/media/arc_animation.gif" width="650"/>

## Usage examples 

Some use cases presented in a form of Python scripts - check [examples](./examples) folder for details.

## Cases 

The service is designed to provide a cases. Therefore, all existing demonstration cases are located separately:
check folder [cases](./cases):
- [green_area_simple.py](./cases/green_area_simple.py) - calculate "green" are nearby property 
  using only open street map data.
  
## Docker image

To compose docker image and run container follow instructions:
* Open terminal: set directory with source code, for example `D:/work/estaty>`
* Image creation command: `docker build -t estatyimage .`
* Launch container: `docker run -d --name greencaseconntainer -p 80:80 estatyimage`
* Check running containers: `docker ps -a`
* Check link with Swagger documentation at localhost: `http://127.0.0.1/docs`