from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import Point, box
import r5py

GTFS_ZIP = "data/gtfs/gtfs_r5.zip"
OSM_PBF  = "data/osm/nord-ovest-260202.osm.pbf"

origin = gpd.GeoDataFrame(
    {"id": ["origin"]},
    geometry=[Point(9.155, 45.402)],
    crs="EPSG:4326"
)

study_bbox = box(8.95, 45.35, 9.35, 45.56)
study_area = gpd.GeoDataFrame(geometry=[study_bbox], crs="EPSG:4326")

cell_size_m = 200
metric_crs = "EPSG:32632"

sa_m = study_area.to_crs(metric_crs)
minx, miny, maxx, maxy = sa_m.total_bounds

cells = []
x = minx
while x < maxx:
    y = miny
    while y < maxy:
        cells.append(box(x, y, x + cell_size_m, y + cell_size_m))
        y += cell_size_m
    x += cell_size_m

grid = gpd.GeoDataFrame(
    {"cell_id": range(len(cells))},
    geometry=cells,
    crs=metric_crs
)

centroids = grid.copy()
centroids["geometry"] = centroids.geometry.centroid
centroids = centroids.to_crs("EPSG:4326")

transport_network = r5py.TransportNetwork(OSM_PBF, [GTFS_ZIP])

departure = datetime(2026, 2, 3, 8, 30)

destinations = centroids.rename(columns={"cell_id": "id"})[["id", "geometry"]]

ttm = r5py.TravelTimeMatrix(
    transport_network,
    origins=origin[["id", "geometry"]],
    destinations=destinations,
    departure=departure,
    transport_modes=[r5py.TransportMode.TRANSIT],
    access_modes=[r5py.TransportMode.WALK],
    max_time=timedelta(minutes=90),
    max_time_walking=timedelta(minutes=20),
    max_public_transport_rides=1,
    departure_time_window=timedelta(minutes=10),
    percentiles=[50],
)

grid_ll = grid.to_crs("EPSG:4326").rename(columns={"cell_id": "id"})
ttm_one = ttm.rename(columns={"to_id": "id"})[["id", "travel_time"]]

out = grid_ll.merge(ttm_one, on="id", how="left")
out.to_file("outputs/transfer_penalty_grid.gpkg", layer="tt", driver="GPKG")

print("Saved outputs/transfer_penalty_grid.gpkg")
