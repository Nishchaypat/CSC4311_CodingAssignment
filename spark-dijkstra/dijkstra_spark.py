from pyspark.sql import SparkSession
from pyspark import SparkFiles
import sys
import time

INF = float("inf")

def parse_header(line):
    try:
        parts = line.strip().split()
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        raise ValueError("Invalid header format. Expected: num_nodes num_edges")

def parse_edge(line):
    try:
        u, v, w = line.strip().split()
        return int(u), (int(v), float(w))
    except (ValueError, IndexError):
        raise ValueError(f"Invalid edge format in line: {line}. Expected: u v weight")

def run_dijkstra(sc, input_path, source=0):
    # Ensure source given by the submit command is an integer
    source = int(source)
    start_time = time.time()

    try:
        path = SparkFiles.get(input_path)
    except Exception:
        path = input_path

    print(f"Reading graph from {path}")
    
    # Load each lines in the text file, skip blanks
    lines = sc.textFile(path).filter(lambda l: l.strip() != "")
    
    # Parse header
    try:
        header = lines.first()
        num_nodes, num_edges = parse_header(header)
        print(f"Graph has {num_nodes} nodes and {num_edges} edges")
    except Exception as e:
        print(f"Error parsing header: {e}")
        sys.exit(1)

    # Function to drop header in first partition
    def drop_header(idx, iterator):
        it = iter(iterator)
        if idx == 0:
            next(it, None)
        return it

    # Build adjacency list RDD
    try:
        edges_rdd = lines.mapPartitionsWithIndex(drop_header).map(parse_edge)
        adjacency = edges_rdd.groupByKey().mapValues(list).cache()
        print(f"Built adjacency list with {adjacency.count()} source nodes")
    except Exception as e:
        print(f"Error building adjacency list: {e}")
        sys.exit(1)

    # Initialize active nodes and distances
    active_nodes = {source}
    distances = {i: INF for i in range(num_nodes)}
    distances[source] = 0.0
    
    iteration = 0
    while active_nodes:
        iteration += 1
        # Broadcast current distances and active nodes
        dist_bcast = sc.broadcast(distances)
        active_bcast = sc.broadcast(active_nodes)
        
        # Only process edges from active nodes for better performance
        candidates = adjacency.filter(lambda x: x[0] in active_bcast.value).flatMap(
            lambda item: [(v, dist_bcast.value[item[0]] + w) for v, w in item[1]]
        )

        # Find minimum candidate per node and collect updates
        min_cands = candidates.reduceByKey(min).filter(
            lambda x: x[1] < dist_bcast.value.get(x[0], INF)
        ).collect()
        
        # Clear active nodes for next iteration to have fressh start
        active_nodes = set()
        
        # Update distances; track nodes that changed
        for node, new_dist in min_cands:
            if new_dist < distances.get(node, INF):
                distances[node] = new_dist
                active_nodes.add(node)  # Only process nodes with updated distances
        
        # Clean up broadcast variables
        dist_bcast.unpersist()
        active_bcast.unpersist()
        
        print(f"Iteration {iteration}: {len(active_nodes)} active nodes")
        
        if not active_nodes:
            break
    
    end_time = time.time()
    print(f"Completed in {iteration} iterations, {end_time - start_time:.2f} seconds")

    print("\nShortest distances from node", source)
    for node in range(num_nodes):
        dist = distances.get(node, INF)
        out = f"{dist:.2f}" if dist != INF else "INF"
        print(f"Node {node}: {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: spark-submit dijkstra_spark.py <input_file> [<source_node>]")
        sys.exit(1)

    input_file = sys.argv[1]
    source_node = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    spark = SparkSession.builder.appName("DijkstraOnSpark").getOrCreate()
    run_dijkstra(spark.sparkContext, input_file, source_node)
    spark.stop()
