#Program to verify hypothesis
#A circle with a higher density would have a greater degree of intersection with other circles

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
count = 0
k = 0
count_edge = 0
density_arr = []
degree_intersection = []
circle_name_arr = []
circle_arr = []

def print_all_arrays(k):
  global circle_name_arr
  global density_arr
  global degree_intersection 
  i = 0
  while(i<k):
    max_density = max(density_arr)
    index = density_arr.index(max_density)
    out_file.write("%s, %f, %f\n" % (circle_name_arr[index],density_arr[index],degree_intersection[index]))
    circle_name_arr.pop(index)
    density_arr.pop(index)
    degree_intersection.pop(index)
    i = i + 1


def find_intersection(k):
  global degree_intersection 
  global circle_arr
  i = 0
  while(i<k):
    temp_size = 0.0
    j = 0
    temp_intersection_arr = []
    temp_union_arr = []
    while(j<k):
      if(j != i):
        temp_intersection_arr = set(circle_arr[i]).intersection(circle_arr[j])
        temp_union_arr = set(circle_arr[i]).union(circle_arr[j])
        temp_size =  temp_size + len(temp_intersection_arr)/(len(temp_union_arr) * 1.0)
      j = j+1
    degree_intersection.append(temp_size)
    i = i+1

def create_arr(id,fp):
  mysearch_arr = []
  with open(fp) as f:
    for line in f.readlines():
        arr =  line.strip().split(' ')
        if(int(arr[0]) == id):
	  mysearch_arr.append(arr[1])
  return mysearch_arr


def get_alter_node_ids(fp):
  global k
  global count_edge
  global circle_name_arr
  global density_arr
  global degree_intersection 
  global circle_arr
  temp_nodes = []
  mynodes = []
  int_array = []

  pattern = re.compile("circle[0-9]+")
  with open(fp) as f:
    for line in f.readlines():
       count_edge = 0
       for n in line.strip().split('\t'):
         if pattern.match(n):
            circle_name_arr.append(n) 
         else:
            mynodes.append(n)
       temp_nodes = list(mynodes)
       circle_arr.append(temp_nodes)
       #print circle_arr
       length = len(mynodes)
       total = length
       print length
       while (length > 0):
         temp = mynodes.pop(0)
         length = len(mynodes)
         path_edge = "facebook/" + args.ego_id + ".edges"
         array = create_arr(int(temp),path_edge)
         for elem in mynodes:
           if((elem in array) == True):
             count_edge = count_edge + 1;
       fact = (total * (total-1))/ 2
       density = count_edge/(fact * 1.0)
       density_arr.append(density)
       k = k+1
  find_intersection(k)
  """
  i = 0
  while(i<k):
    temp_size = 0.0
    j = 0
    temp_intersection_arr = []
    temp_union_arr = []
    while(j<k):
      if(j != i):
        temp_intersection_arr = set(circle_arr[i]).intersection(circle_arr[j])
        temp_union_arr = set(circle_arr[i]).union(circle_arr[j])
        temp_size =  temp_size + len(temp_intersection_arr)/(len(temp_union_arr) * 1.0)
      j = j+1
    degree_intersection.append(temp_size)
    i = i+1
  """
  print_all_arrays(k)   



out_file = open(output_file, "w")
path_circles = graphs_dir + "/" + args.ego_id + ".circles"
get_alter_node_ids(path_circles)

out_file.close()
