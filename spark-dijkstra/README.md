# Spark Dijkstra Implementation

This project implements Dijkstra's algorithm using Apache Spark to find the shortest paths in a weighted graph.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed and configured:

* An Azure Virtual Machine (VM) running Linux (ubuntu 20.04).
* VM Size Standard B2s (2 vcpus, 4 GiB memory)
* Java Development Kit (JDK) version 8 or higher.
* Python version 3.10 or higher.
* Apache Spark version 3.5.5.

## Installation and Setup Instructions

Follow these steps to set up the environment on your Azure VM.

### 1. Setting Up the Azure VM

If you don't have an Azure VM, create one using the Azure CLI:

Example:

```bash
az vm create \
  --resource-group cloudclass \
  --name node1 \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B2s

```
Configure Networking (Network Security Group - NSG)

For Spark's standalone cluster and web UIs to work correctly, you need to open specific ports in the VM's Network Security Group (NSG).

* `7077`: Spark Master communication port.
* `8080`: Spark Master Web UI.
* `4040`: Spark Application/Driver Web UI (when a job is running).
* `22`: SSH (already open by default typically).


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
git clone https://github.com/Nishchaypat/CSC4311_CodingAssignment.git
cd spark-dijkstra
```

### 2. Run the Application on a Spark Cluster

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
├── dijkstra_spark.py
├── weighted_graph.txt
├── README.md             
└── report.pdf             
└── screenshots/            

