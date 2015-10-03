#Program to verify hypothesis
#A node with higher degree would belong to more number of circles

#Author: Ravi Pratap Singh
#Unity-id: rpsingh3
#Course: CSC591 - Social Computing

import argparse
import snap
import os, sys
import re

parser = argparse.ArgumentParser()
parser.add_argument('ego_id', action="store")
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
       for n in line.strip().split('\t'):
         if pattern.match(n):
           test = 1 
         else:
           mynodes.append(n)
       circles_arr[0] = circles_arr[0] + 1
  #print mynodes 
  int_array = [int(s) for s in mynodes]
  for x in int_array:
    circles_arr[x] = circles_arr[x] + 1;  
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
  path_circles = graphs_dir + "/" + args.ego_id + ".circles"
  graph = snap.LoadEdgeList(snap.PNGraph, path_edges, 0, 1)
  graph.AddNode(ego_id)
  int_array = get_circles_count_and_node_ids(path_circles)

  for node_id in int_array:
    #print node_id," "
    global count 
    count = count + 1
    try:
      graph.AddNode(node_id)
    except RuntimeError:
      pass
    graph.AddEdge(ego_id, node_id)
  return graph



out_file = open(output_file, "w")
graph = generate_graph(graphs_dir, int(args.ego_id))
print_node_degrees(graph, int(args.ego_id))
out_file.close()
