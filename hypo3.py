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
ego_nodes_arr = []
common_feature_arr = []
count = 0

def get_alter_node_ids(fp_circle,fp_feat,fp_egofeat):
  mynodes = []
  int_array = []
  global circles_arr
  global common_feature_arr
  global ego_nodes_arr
  ego_feature_arr = []
  egonode_feature_arr = []
  #circles_arr = [0] * 400
  total_features = 0
  with open(fp_egofeat) as f:
    for line in f.readlines():
       for n in line.strip().split(' '):
         total_features = total_features + 1
         ego_feature_arr.append(int(n))
  print total_features
    
  pattern = re.compile("circle[0-9]+")
  with open(fp_circle) as f:
    for line in f.readlines():
       for n in line.strip().split('\t'):
         if pattern.match(n):
           total_features = total_features 
         else:
           mynodes.append(n)
      # ego_user_circle_count = ego_user_circle_count + 1
  #print mynodes 
  int_array = [int(s) for s in mynodes]
 
  with open(fp_feat) as f:
    for line in f.readlines():
       ego_node = int(line.partition(' ')[0]) 
       ego_nodes_arr.append(ego_node)

  with open(fp_feat) as f:
    for line in f.readlines():
       for n in line.strip().split(' '):
         egonode_feature_arr.append(int(n))
       k = 0
       common_feature = 0
       while(k < total_features):
         if(ego_feature_arr[k] == 1 and egonode_feature_arr[k+1] == 1):
           common_feature = common_feature + 1 
         k = k+1
       common_feature_arr.append(common_feature)
       egonode_feature_arr[:] = []
      
  for x in ego_nodes_arr:
    count = int_array.count(x)
    circles_arr.append(count)
    print "Node: ",x,"and Count: ",count
  return int_array
            
         
out_file = open(output_file, "w")

ego_ids = [int(args.ego_id)]
# Print node degrees
for ego_id in ego_ids:
  path_feat = graphs_dir + "/" + args.ego_id + ".feat"
  path_egofeat = graphs_dir + "/" + args.ego_id + ".egofeat"
  path_circle = graphs_dir + "/" + args.ego_id + ".circles"
  int_array = get_alter_node_ids(path_circle, path_feat,path_egofeat)

  k = len(ego_nodes_arr)
  i = 0
  while(i<k):
    max_circle = max(circles_arr)
    index = circles_arr.index(max_circle)
    out_file.write("%s, %f, %f\n" % (ego_nodes_arr[index],circles_arr[index],common_feature_arr[index]))
    ego_nodes_arr.pop(index)
    circles_arr.pop(index)
    common_feature_arr.pop(index)
    i = i + 1

out_file.close()
