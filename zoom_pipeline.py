import dlt

from zoom import source

pipeline = dlt.pipeline(
    pipeline_name="zoom_test", destination="duckdb", dataset_name="zoom", progress="log"
)
load_info = pipeline.run(source)
print(load_info)
