import cudf
from cuml.cluster import DBSCAN


def test_cuml_fit_clusters():
    # Create and populate a GPU DataFrame
    gdf_float = cudf.DataFrame()
    gdf_float['0'] = [1.0, 2.0, 5.0]
    gdf_float['1'] = [4.0, 2.0, 1.0]
    gdf_float['2'] = [4.0, 2.0, 1.0]

    # Setup and fit clusters
    dbscan_float = DBSCAN(eps=1.0, min_samples=1)
    dbscan_float.fit(gdf_float)

    print(dbscan_float.labels_)
