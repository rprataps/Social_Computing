#Program to calculate graph statistics 
#A node with higher degree would belong to more number of circles

#Author: Ravi Pratap Singh
#Unity-id: rpsingh3
#Course: CSC591 - Social Computing

import argparse
import snap
import os, sys
import re

parser = argparse.ArgumentParser()
#parser.add_argument('ego_id', action="store")
parser.add_argument('dir', action="store")
parser.add_argument('outfile', action="store")

args = parser.parse_args()
graphs_dir = args.dir
output_file = args.outfile
circles_arr = []
count = 0

#############################################################################
# Class of Node
################################################################################
class Node:
  def __init__(self, id, degree):
    self.id = id
    self.degree = degree

###############################################################################
# Function to get circles count and node_ids
################################################################################
def get_circles_count_and_node_ids(fp):
  mynodes = []
  int_array = []
  global circles_arr
  #circles_arr = [0] * 400
  for i in xrange(0,1000):
    circles_arr.append(0)
  pattern = re.compile("circle[0-9]+")
  with open(fp) as f:
    for line in f.readlines():
      temp = int(line.partition(' ')[0])
      int_array.append(temp)
  return int_array


###############################################################################
# Function to dump degree and count for each node in output file
################################################################################
def print_node_degrees(graph, ego_id):
  global out_file
  global circles_arr
  nodes = []
  for node in graph.Nodes():
    nodes.append(Node(node.GetId(), node.GetDeg()))
  for node in sorted(nodes, key=lambda node: circles_arr[node.id],reverse=True):
    out_file.write("%d,%d,%d\n" % ( node.id, node.degree,circles_arr[node.id]))


################################################################################
# Function to load and generate graph
################################################################################
def generate_graph(graphs_dir, ego_id):
  path_edges = graphs_dir + "/" + args.ego_id + ".edges"
  graph = snap.LoadEdgeList(snap.PNGraph, path_edges, 0, 1)
  graph.AddNode(ego_id)
  int_array = get_circles_count_and_node_ids(path_edges)

  for node_id in int_array:
    try:
      graph.AddNode(node_id)
    except RuntimeError:
      pass
    graph.AddEdge(ego_id, node_id)
  return graph


################################################################################
# Function to load and generate undirected graph
################################################################################
def generate_ugraph(graphs_dir, ego_id):
  path_edges = graphs_dir + "/" + args.ego_id + ".edges"
  graph = snap.LoadEdgeList(snap.PUNGraph, path_edges, 0, 1)
  graph.AddNode(ego_id)
  int_array = get_circles_count_and_node_ids(path_edges)

  for node_id in int_array:
    try:
      graph.AddNode(node_id)
    except RuntimeError:
      pass
    graph.AddEdge(ego_id, node_id)
    graph.AddEdge(node_id, ego_id)
  return graph


out_file = open(output_file, "w")

# Commenting this section which I was planning to calculate
# the statistics within the ego network
"""
graph = generate_graph(graphs_dir, int(args.ego_id))
GraphClusterCoeff = snap.GetClustCf (graph, -1)
print "Clustering coefficient: %f" % GraphClusterCoeff

ugraph = generate_ugraph(graphs_dir, int(args.ego_id))
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(ugraph, Nodes, Edges, 1.0)
for node in Nodes:
    print "node: %d centrality: %f" % (node, Nodes[node])
    
for edge in Edges:
    print "edge: (%d, %d) centrality: %f" % (edge.GetVal1(), edge.GetVal2(), Edges[edge])
"""

out_file.write("Graph Statistics:\n\n")
count_nodes = 0
# Calculate the statistics based on the facebook_combined file
path_edges = graphs_dir + "/" + "facebook_combined.txt"
graph = snap.LoadEdgeList(snap.PNGraph, path_edges, 0, 1)
for node in graph.Nodes():
  count_nodes = count_nodes + 1
#print count_nodes
out_file.write("Number of nodes in graph is %d\n" % (count_nodes))
GraphClusterCoeff = snap.GetClustCf (graph, -1)
#print "Clustering coefficient: %f" % GraphClusterCoeff
out_file.write("Clustering Coefficient for graph is %f\n" % (GraphClusterCoeff))

count_directed_edges = 0
count_undirected_edges = 0

ugraph = snap.LoadEdgeList(snap.PUNGraph, path_edges, 0, 1)
count_directed_edges = snap.CntUniqDirEdges(ugraph)
#print "Undirected Graph: Count of unique Directed edges is %d" % count_directed_edges
out_file.write("Count of unique directed edges in graph is %d\n" % (count_directed_edges))

count_undirected_edges = snap.CntUniqUndirEdges(ugraph)
#print "Undirected Graph: Count of unique Undirected edges is %d" % count_undirected_edges
out_file.write("Count of unique undirected edges in graph is %d\n" % (count_undirected_edges))


Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(ugraph, Nodes, Edges, 1.0)

for node in Nodes:
    #print "node: %d centrality: %f" % (node, Nodes[node])
    if(node == 0 or node == 107 or node == 348 or node == 414 or node == 686 or node == 698):
      out_file.write("Betweenness centrality for node:%d is %f\n" % ( node,Nodes[node]))

# For each edge, calculate centraility
"""
for edge in Edges:
    print "edge: (%d, %d) centrality: %f" % (edge.GetVal1(), edge.GetVal2(), Edges[edge])
"""

out_file.close()
