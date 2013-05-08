# datatype.py: get datatype from ArcGIS
# -*- coding: utf-8 -*-
import arcpy

class DataType(object):
    """ Determine whether we should use keyword parameter types or names. 
    Names were originally used in 10.1, but don't work for localized 
	environments, which was resolved by switching to keywords in 10.1SP1. 
	Detect our version, and do the correct one based on the version.
    """ 
    version = None
    sp = None
    types = None
    labels = None
    keywords = None
    descriptions = None

    def __init__(self):
        self.version = self.get_version()
        self.service_pack = self.get_sp()
        self.types = self.get_types()
        self.labels = self.get_labels()
        self.keywords = self.get_keywords()
        self.descriptions = self.get_descriptions()

    def get_version(self):
        """ Get installation major release verson (e.g. 10.0, 10.1)."""
        return arcpy.GetInstallInfo()['Version']

    def get_sp(self):
        """ Get installation service pack number (e.g. 1, N/A)."""
        return arcpy.GetInstallInfo()['SPNumber']

    def normalize(self, raw_type):
        """ Determine the appropriate naming convention based on release, 
        normalize the input datatype as needed."""
        normalized = None
        type_of = None
        # determine what we're getting
        if raw_type in self.labels:
            type_of = 'label'
        elif raw_type in self.keywords:
            type_of = 'keyword'

        # only continue if we have a recognized type
        if type_of is not None:
            if (self.version == '10.0') or \
                    (self.version == 10.1 and self.service_pack == 'N/A'):
                if type_of == 'keyword':
                    normalized = self.keyword_to_label(raw_type)

            if self.version == '10.1' and self.service_pack == '1':
                # keywords are the default type in 10.1SP1+
                if type_of == 'label':
                    normalized = self.label_to_keyword(raw_type)
            
            if normalized is None:
                # haven't needed to modify the output; return the input
                normalized = raw_type

        return normalized

    def keyword_to_label(self, keyword=None):
        """ convert a keyword to a label (old datatype strings)."""
        label = None 
        for (k, label_info) in self.get_types().items():
            if label_info['keyword'] == keyword:
                label = k
        return label

    def label_to_keyword(self, label=None):
        """ convert an old datatype string to a keyword."""
        # convert label to keyword
        return self.types[label]['keyword']
               
    def get_labels(self):
        """ get all labels (old datatype strings)."""
        return self.get_types().keys()

    def get_keywords(self):
        """ get all keywords (locale-independent types)."""
        return [v['keyword'] for v in self.get_types().values()]

    def get_descriptions(self):
        """ get all descriptions of our types."""
        return [v['description'] for v in self.get_types().values()]
 
    def get_types(self):
        """ A dictionary of all types, pulled from the 10.1 documentation.
http://resources.arcgis.com/en/help/main/10.1/index.html#//001500000035000000
        """
        types = { 
  'Address Locator': {'keyword': 'DEAddressLocator',  'description': 'A dataset, used for geocoding, that stores the address attributes, associated indexes, and rules that define the process for translating nonspatial descriptions of places to spatial data.'},
  'Address Locator Style': {'keyword': 'GPAddressLocatorStyle',  'description': 'A template on which to base the new address locator.'},
  'Analysis Cell Size': {'keyword': 'analysis_cell_size',  'description': 'The cell size used by raster tools.'},
  'Any Value': {'keyword': 'GPType',  'description': 'A data type that accepts any value.'},
  'ArcMap Document': {'keyword': 'DEMapDocument',  'description': 'A file that contains one map, its layout, and its associated layers, tables, charts, and reports.'},
  'Areal Unit': {'keyword': 'GPArealUnit',  'description': 'An areal unit type and value such as square meter or acre.'},
  'Boolean': {'keyword': 'GPBoolean',  'description': 'A Boolean value.'},
  'CAD Drawing Dataset': {'keyword': 'DECadDrawingDataset',  'description': 'A vector data source with a mix of feature types with symbology. The dataset is not usable for feature class-based queries or analysis.'},
  'Calculator Expression': {'keyword': 'GPCalculatorExpression',  'description': 'A calculator expression.'},
  'Catalog Root': {'keyword': 'DECatalogRoot',  'description': 'The top-level node in the Catalog tree.'},
  'Cell Size': {'keyword': 'GPSACellSize',  'description': 'The cell size used byArcGIS Spatial Analyst extension.'},
  'Cell Size XY': {'keyword': 'GPCellSizeXY',  'description': 'Defines the two sides of a raster cell.'},
  'Composite Layer': {'keyword': 'GPCompositeLayer',  'description': 'A reference to several children layers, including symbology and rendering properties.'},
  'Compression': {'keyword': 'GPSAGDBEnvCompression',  'description': 'Specifies the type of compression used for a raster.'},
  'Coordinate System': {'keyword': 'GPCoordinateSystem',  'description': 'A reference framework&mdash;such as the UTM system&mdash;consisting of a set of points, lines, and/or surfaces, and a set of rules, used to define the positions of points in two- and three-dimensional space.'},
  'Coordinate Systems Folder': {'keyword': 'DESpatialReferencesFolder',  'description': 'A folder on disk storing coordinate systems.'},
  'Coverage': {'keyword': 'DECoverage',  'description': 'A coverage dataset, a proprietary data model for storing geographic features as points, arcs, and polygons with associated feature attribute tables.'},
  'Coverage Feature Class': {'keyword': 'DECoverageFeatureClasses',  'description': 'A coverage feature class, such as point, arc, node, route, route system, section, polygon, and region.'},
  'Data Element': {'keyword': 'DEType',  'description': 'A dataset visible in ArcCatalog.'},
  'Data File': {'keyword': 'GPDataFile',  'description': 'A data file.'},
  'Database Connections': {'keyword': 'DERemoteDatabaseFolder',  'description': 'The database connection folder in ArcCatalog.'},
  'Dataset': {'keyword': 'DEDatasetType',  'description': 'A collection of related data, usually grouped or stored together.'},
  'Date': {'keyword': 'GPDate',  'description': 'A date value.'},
  'dBase Table': {'keyword': 'DEDbaseTable',  'description': 'Attribute data stored in dBASE format.'},
  'Decimate': {'keyword': 'GP3DADecimate',  'description': 'Specifies a subset of nodes of a TIN to create a generalized version of that TIN.'},
  'Disk Connection': {'keyword': 'DEDiskConnection',  'description': 'An access path to a data storage device.'},
  'Double': {'keyword': 'GPDouble',  'description': 'Any floating-point number will be stored as a double-precision, 64-bit value.'},
  'Encrypted String': {'keyword': 'GPEncryptedString',  'description': 'Encrypted string for passwords.'},
  'Envelope': {'keyword': 'GPEnvelope',  'description': 'The coordinate pairs that define the minimum bounding rectangle the data source falls within.'},
  'Evaluation Scale': {'keyword': 'GPEvaluationScale',  'description': 'The scale value range and increment value applied to inputs in a weighted overlay operation.'},
  'Extent': {'keyword': 'GPExtent',  'description': 'Specifies the coordinate pairs that define the minimum bounding rectangle (xmin, ymin and xmax, ymax) of a data source. All coordinates for the data source fall within this boundary.'},
  'Extract Values': {'keyword': 'GPSAExtractValues',  'description': 'An extract values parameter.'},
  'Feature Class': {'keyword': 'DEFeatureClass',  'description': 'A collection of spatial data with the same shape type: point, multipoint, polyline, and polygon.'},
  'Feature Dataset': {'keyword': 'DEFeatureDataset',  'description': 'A collection of feature classes that share a common geographic area and the same spatial reference system.'},
  'Feature Layer': {'keyword': 'GPFeatureLayer',  'description': 'A reference to a feature class, including symbology and rendering properties.'},
  'Feature Set': {'keyword': 'GPFeatureRecordSetLayer',  'description': 'Interactive features; draw the features when the tool is run.'},
  'Field': {'keyword': 'Field',  'description': 'A column in a table that stores the values for a single attribute.'},
  'Field Info': {'keyword': 'GPFieldInfo',  'description': 'The details about a field in a FieldMap.'},
  'Field Mappings': {'keyword': 'GPFieldMapping',  'description': 'A collection of fields in one or more input tables.'},
  'File': {'keyword': 'DEFile',  'description': 'A file on disk.'},
  'Folder': {'keyword': 'DEFolder',  'description': 'Specifies a location on a disk where data is stored.'},
  'Formulated Raster': {'keyword': 'GPRasterFormulated',  'description': 'A raster surface whose cell values are represented by a formula or constant.'},
  'Fuzzy function': {'keyword': 'GPSAFuzzyFunction',  'description': 'Fuzzy function.'},
  'Geodataset': {'keyword': 'DEGeodatasetType',  'description': 'A collection of data with a common theme in a geodatabase.'},
  'GeoDataServer': {'keyword': 'DEGeoDataServer',  'description': 'A coarse-grained object that references a geodatabase.'},
  'Geometric Network': {'keyword': 'DEGeometricNetwork',  'description': 'A linear network represented by topologically connected edge and junction features. Feature connectivity is based on their geometric coincidence.'},
  'Geostatistical Layer': {'keyword': 'GPGALayer',  'description': 'A reference to a geostatistical data source, including symbology and rendering properties.'},
  'Geostatistical Search Neighborhood': {'keyword': 'GPGASearchNeighborhood',  'description': 'Defines the searching neighborhood parameters for a geostatistical layer.'},
  'Geostatistical Value Table': {'keyword': 'GPGALayer',  'description': 'A collection of data sources and fields that define a geostatistical layer.'},
  'GlobeServer': {'keyword': 'DEGlobeServer',  'description': 'A Globe server.'},
  'GPServer': {'keyword': 'DEGPServer',  'description': 'A geoprocessing server.'},
  'Graph': {'keyword': 'GPGraph',  'description': 'A graph.'},
  'Graph Data Table': {'keyword': 'GPGraphDataTable',  'description': 'A graph data table.'},
  'Group Layer': {'keyword': 'GPGroupLayer',  'description': 'A collection of layers that appear and act as a single layer. Group layers make it easier to organize a map, assign advanced drawing order options, and share layers for use in other maps.'},
  'Horizontal Factor': {'keyword': 'GPSAHorizontalFactor',  'description': 'The relationship between the horizontal cost factor and the horizontal relative moving angle.'},
  'Image Service': {'keyword': 'DEImageServer',  'description': 'An image service.'},
  'Index': {'keyword': 'Index',  'description': 'A data structure used to speed the search for records in geographic datasets and databases.'},
  'INFO Expression': {'keyword': 'GPINFOExpression',  'description': 'A syntax for defining and manipulating data in an INFO table.'},
  'INFO Item': {'keyword': 'GPArcInfoItem',  'description': 'An item in an INFO table.'},
  'INFO Table': {'keyword': 'DEArcInfoTable',  'description': 'A table in an INFO database.'},
  'LAS Dataset': {'keyword': 'DELasDataset',  'description': 'A LAS dataset stores reference to one or more LAS files on disk, as well as to additional surface features. A LAS file is a binary file that is designed to store airborne lidar data.'},
  'LAS Dataset Layer': {'keyword': 'GPLasDatasetLayer',  'description': 'A layer that references a LAS dataset on disk. This layer can apply filters on lidar files and surface constraints referenced by a LAS dataset.'},
  'Layer': {'keyword': 'GPLayer',  'description': 'A reference to a data source, such as a shapefile, coverage, geodatabase feature class, or raster, including symbology and rendering properties.'},
  'Layer File': {'keyword': 'DELayer',  'description': 'A file with a .lyr extension that stores the layer definition, including symbology and rendering properties.'},
  'Line': {'keyword': 'GPLine',  'description': 'A shape, straight or curved, defined by a connected series of unique x,y coordinate pairs.'},
  'Linear Unit': {'keyword': 'GPLinearUnit',  'description': 'A linear unit type and value such as meter or feet.'},
  'Long': {'keyword': 'GPLong',  'description': 'An integer number value.'},
  'M Domain': {'keyword': 'GPMDomain',  'description': 'A range of lowest and highest possible value for m coordinates.'},
  'MapServer': {'keyword': 'DEMapServer',  'description': 'A map server.'},
  'Mosaic Dataset': {'keyword': 'DEMosaicDataset',  'description': 'A collection of raster and image data that allows you to store, view, and query the data. It is a data model within the geodatabase used to manage a collection of raster datasets (images) stored as a catalog and viewed as a mosaicked image.'},
  'Mosaic Layer': {'keyword': 'GPMosaicLayer',  'description': 'A layer that references a mosaic dataset.'},
  'Neighborhood': {'keyword': 'GPSANeighborhood',  'description': 'The shape of the area around each cell used to calculate statistics.'},
  'Network Analyst Class FieldMap': {'keyword': 'NAClassFieldMap',  'description': 'Mapping between location properties in a Network Analyst layer (such as stops, facilities and incidents) and a point feature class.'},
  'Network Analyst Hierarchy Settings': {'keyword': 'GPNAHierarchySettings',  'description': 'A hierarchy attribute that divides hierarchy values of a network dataset into three groups using two integers. The first integer, high_rank_ends, sets the ending value of the first group; the second number, low_rank_begin, sets the beginning value of the third group.'},
  'Network Analyst Layer': {'keyword': 'GPNALayer',  'description': 'A special group layer used to express and solve network routing problems. Each sublayer held in memory in a Network Analyst layer represents some aspect of the routing problem and the routing solution.'},
  'Network Dataset': {'keyword': 'DENetworkDataset',  'description': 'A collection of topologically connected network elements (edges, junctions, and turns), derived from network sources and associated with a collection of network attributes.'},
  'Network Dataset Layer': {'keyword': 'GPNetworkDatasetLayer',  'description': 'A reference to a network dataset, including symbology and rendering properties.'},
  'Parcel Fabric': {'keyword': 'DECadastralFabric',  'description': 'A parcel fabric is a dataset for the storage, maintenance, and editing of a continuous surface of connected parcels or parcel network.'},
  'Parcel Fabric Layer': {'keyword': 'GPCadastralFabricLayer',  'description': 'A layer referencing a parcel fabric on disk. This layer works as a group layer organizing a set of related layers under a single layer.'},
  'Point': {'keyword': 'GPPoint',  'description': 'A pair of x,y coordinates.'},
  'Polygon': {'keyword': 'GPPolygon',  'description': 'A connected sequence of x,y coordinate pairs, where the first and last coordinate pair are the same.'},
  'Projection File': {'keyword': 'DEPrjFile',  'description': 'A file storing coordinate system information for spatial data.'},
  'Pyramid': {'keyword': 'GPSAGDBEnvPyramid',  'description': 'Specifies if pyramids will be built.'},
  'Radius': {'keyword': 'GPSARadius',  'description': 'Specifies which surrounding points will be used for interpolation.'},
  'Random Number Generator': {'keyword': 'GPRandomNumberGenerator',  'description': 'Specifies the seed and the generator to be used when creating random values.'},
  'Raster Band': {'keyword': 'DERasterBand',  'description': 'A layer in a raster dataset.'},
  'Raster Calculator Expression': {'keyword': 'GPRasterCalculatorExpression',  'description': 'A raster calculator expression.'},
  'Raster Catalog': {'keyword': 'DERasterCatalog',  'description': 'A collection of raster datasets defined in a table; each table record defines an individual raster dataset in the catalog.'},
  'Raster Catalog Layer': {'keyword': 'GPRasterCatalogLayer',  'description': 'A reference to a raster catalog, including symbology and rendering properties.'},
  'Raster Data Layer': {'keyword': 'GPRasterDataLayer',  'description': 'A raster data layer.'},
  'Raster Dataset': {'keyword': 'DERasterDataset',  'description': 'A single dataset built from one or more rasters.'},
  'Raster Layer': {'keyword': 'GPRasterLayer',  'description': 'A reference to a raster, including symbology and rendering properties.'},
  'Raster Statistics': {'keyword': 'GPSAGDBEnvStatistics',  'description': 'Specifies if raster statistics will be built.'},
  'Raster Type': {'keyword': 'GPRasterBuilder',  'description': 'Raster data is added to a mosaic dataset by specifying a raster type. The raster type identifies metadata, such as georeferencing, acquisition date, and sensor type, along with a raster format.'},
  'Record Set': {'keyword': 'GPRecordSet',  'description': 'Interactive table; type in the table values when the tool is run.'},
  'Relationship Class': {'keyword': 'DERelationshipClass',  'description': 'The details about the relationship between objects in the geodatabase.'},
  'Remap': {'keyword': 'GPSARemap',  'description': 'A table that defines how raster cell values will be reclassified.'},
  'Route Measure Event Properties': {'keyword': 'GPRouteMeasureEventProperties',  'description': 'Specifies the fields on a table that describe events that are measured by a linear reference route system.'},
  'Schematic Dataset': {'keyword': 'DESchematicDataset',  'description': 'A schematic dataset contains a collection of schematic diagram templates and schematic feature classes that share the same application domain, for example, water or electrical. It can reside in a personal, file, or ArcSDE geodatabase.'},
  'Schematic Diagram': {'keyword': 'DESchematicDiagram',  'description': 'A schematic diagram.'},
  'Schematic Folder': {'keyword': 'DESchematicFolder',  'description': 'A schematic folder.'},
  'Schematic Layer': {'keyword': 'GPSchematicLayer',  'description': 'A schematic layer is a composite layer composed of feature layers based on the schematic feature classes associated with the template on which the schematic diagram is based.'},
  'Semivariogram': {'keyword': 'GPSASemiVariogram',  'description': 'Specifies the distance and direction representing two locations that are used to quantify autocorrelation.'},
  'ServerConnection': {'keyword': 'DEServerConnection',  'description': 'A server connection.'},
  'Shapefile': {'keyword': 'DEShapefile',  'description': 'Spatial data in shapefile format.'},
  'Spatial Reference': {'keyword': 'GPSpatialReference',  'description': 'The coordinate system used to store a spatial dataset, including the spatial domain.'},
  'SQL Expression': {'keyword': 'GPSQLExpression',  'description': 'A syntax for defining and manipulating data from a relational database.'},
  'String': {'keyword': 'GPString',  'description': 'A text value.'},
  'Table': {'keyword': 'DETable',  'description': 'Tabular data.'},
  'Table View': {'keyword': 'GPTableView',  'description': 'A representation of tabular data for viewing and editing purposes, stored in memory or on disk.'},
  'Terrain Layer': {'keyword': 'GPTerrainLayer',  'description': 'A reference to a terrain, including symbology and rendering properties. It\'s used to draw a terrain.'},
  'Text File': {'keyword': 'DETextfile',  'description': 'Data stored in ASCII format.'},
  'Tile Size': {'keyword': 'GPSAGDBEnvTileSize',  'description': 'Specifies the width and the height of a data stored in block.'},
  'Time configuration': {'keyword': 'GPSATimeConfiguration',  'description': 'Specifies the time periods used for calculating solar radiation at specific locations.'},
  'TIN': {'keyword': 'DETin',  'description': 'A vector data structure that partitions geographic space into contiguous, nonoverlapping triangles. The vertices of each triangle are sample data points with x-, y-, and z-values.'},
  'Tin Layer': {'keyword': 'GPTinLayer',  'description': 'A reference to a TIN, including topological relationships, symbology, and rendering properties.'},
  'Tool': {'keyword': 'DETool',  'description': 'A geoprocessing tool.'},
  'Toolbox': {'keyword': 'DEToolbox',  'description': 'A geoprocessing toolbox.'},
  'Topo Features': {'keyword': 'GPSATopoFeatures',  'description': 'Features that are input to the interpolation.'},
  'Topology': {'keyword': 'DETopology',  'description': 'A topology that defines and enforces data integrity rules for spatial data.'},
  'Topology Layer': {'keyword': 'GPTopologyLayer',  'description': 'A reference to a topology, including symbology and rendering properties.'},
  'Value Table': {'keyword': 'GPValueTable',  'description': 'A collection of columns of values.'},
  'Variant': {'keyword': 'GPVariant',  'description': 'A data value that can contain any basic type: Boolean, date, double, long, and string.'},
  'Vertical Factor': {'keyword': 'GPSAVerticalFactor',  'description': 'Specifies the relationship between the vertical cost factor and the vertical, relative moving angle.'},
  'VPF Coverage': {'keyword': 'DEVPFCoverage',  'description': 'Spatial data stored in Vector Product Format.'},
  'VPF Table': {'keyword': 'DEVPFTable',  'description': 'Attribute data stored in Vector Product Format.'},
  'WCS Coverage': {'keyword': 'DEWCSCoverage',  'description': 'Web Coverage Service (WCS) is an open specification for sharing raster datasets on the web.'},
  'Weighted Overlay Table': {'keyword': 'GPSAWeightedOverlayTable',  'description': 'A table with data to combine multiple rasters by applying a common measurement scale of values to each raster, weighing each according to its importance.'},
  'Weighted Sum': {'keyword': 'GPSAWeightedSum',  'description': 'Specifies data for overlaying several rasters multiplied each by their given weight and then summed.'},
  'WMS Map': {'keyword': 'DEWMSMap',  'description': 'A WMS Map.'},
  'Workspace': {'keyword': 'DEWorkspace',  'description': 'A container such as a geodatabase or folder.'},
  'XY Domain': {'keyword': 'GPXYDomain',  'description': 'A range of lowest and highest possible values for x,y coordinates.'},
  'Z Domain': {'keyword': 'GPZDomain',  'description': 'A range of lowest and highest possible values for z coordinates.'}}
        return types

datatype = DataType()
