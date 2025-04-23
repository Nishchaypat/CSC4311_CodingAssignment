# Spark Dijkstra Implementation

This project implements Dijkstra's algorithm using Apache Spark to find the shortest paths in a weighted graph.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed and configured:

* An Azure Virtual Machine (VM) running Ubuntu 20.04 LTS or later.
* Java Development Kit (JDK) version 8 or higher.
* Python version 3.7 or higher.
* Apache Spark version 3.1.2 or higher.

## Installation and Setup Instructions

Follow these steps to set up the environment on your Azure VM.

### 1. Setting Up the Azure VM

If you don't have an Azure VM, create one using the Azure CLI:

```bash
az vm create \
  --resource-group SparkAssignment \
  --name spark-master \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_D4s_v3

```
Connect to your VM using SSH.

### 2. Install Java

Update the package list and install OpenJDK 8:

```bash
sudo apt update
sudo apt install -y openjdk-8-jdk
```

Verify the installation:

```bash
java -version
```

### 3. Install Python and PySpark

Install Python 3 pip and then install PySpark:

```bash
sudo apt install -y python3-pip
pip3 install pyspark==3.1.2
```

### 4. Download and Extract Apache Spark

Download the specified Spark version and extract it:

```bash
wget [https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz]
tar -xzf spark-3.5.5-bin-hadoop3.tgz
mv spark-3.5.5-bin-hadoop3 spark
```

### 5. Set Environment Variables

Add Spark environment variables to your `.bashrc` file to make them persistent:

```bash
echo 'export SPARK_HOME=~/spark' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc
source ~/.bashrc
```

Verify Spark installation by running the Spark shell:

```bash
spark-shell
```

(Exit the shell using `:quit`)

## Running the Application

### 1. Clone the Repository

Clone the project repository to your local machine or VM:

```bash
# Replace 'yourusername' with the actual GitHub username
git clone https://github.com/Nishchaypat/CSC4311_CodingAssignment.git
cd spark-dijkstra
```

### 2. Run the Application Locally

You can run the Spark application locally using `spark-submit`. This is useful for testing on smaller datasets.

```bash
# Runs the Dijkstra algorithm on weighted_graph.txt starting from node 0
spark-submit dijkstra_spark.py weighted_graph.txt 0
```

### 3. Run the Application on a Spark Cluster

To run the application on a standalone Spark cluster, use `spark-submit` and specify the master node's URL. Ensure the graph file is accessible to all worker nodes, for example, by using the `--files` option.

```bash
# Replace YOUR_SPARK_MASTER with the actual hostname or IP of your Spark master
spark-submit \
  --master spark://YOUR_SPARK_MASTER:7077 \
  --files weighted_graph.txt \
  dijkstra_spark.py weighted_graph.txt 0
```

## File Structure

The project repository has the following structure:

```
spark-dijkstra/
├── dijkstra_spark.py       # Main Spark application script implementing Dijkstra's algorithm
├── weighted_graph.txt      # Example weighted graph data file for testing
├── README.md               # This README file
└── report.pdf              # Detailed implementation report (if applicable)

