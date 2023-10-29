from arcgis.gis import GIS

gis = GIS()

webmap_search = gis.content.search(
  query="School District Characteristics - Current tags:tutorial owner:esri_devlabs",
  item_type="Web Map"
)
webmap_search

School District Characteristics - Current