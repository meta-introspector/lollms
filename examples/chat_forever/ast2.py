from PIL import Image
from PIL import Image, ImageFile
from _ast import AST
from ast import parse
from collections import Counter
from contextlib import suppress
from six import StringIO 
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (OneHotEncoder,LabelBinarizer)
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import ast
import asttokens
import codecs
import collections
import glob
import inspect
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas
import pandas as pd
import pprint
import psutil
import seaborn as sns
import sklearn
import types

results = dict(
  entities = {},
  relations = {})
nextid = dict(
  entities = 0,
  relations = 0)


def encode_node(x,y):
  ent = results[y]
  nxt = nextid[y]
  if x not in ent:
    ent[x] = nxt
    nextid[y] = nxt + 1
  else:
    nxt = end[x]
  return nxt # also the id found



module_global = {
   x:y for x,y in globals().items()
    if isinstance(y, types.ModuleType)
    and x not in  ('__builtins__',
                   '__builtin__',
                  )
}


#module_global

module_sources = {
 x : inspect.getsource(y)
       for x,y in globals().items()
    if isinstance(y, types.ModuleType)
    and x not in  ('__builtins__',
                   '__builtin__',
                  )
}

parsed_modules_ast_tokens ={
    x : asttokens.ASTTokens(module_sources[x], parse=True) 
    for x,y in globals().items()
    if isinstance(y, types.ModuleType)
    and x not in  ('__builtins__',
                   '__builtin__',
                  )  }

all_asts = []
module_asts={}

for module in parsed_modules_ast_tokens:
    module_asts[module]=[]    
    astoks= parsed_modules_ast_tokens[module]
    start_node = astoks.tree
    walkpos = 0
    lst_token = None
    class DFVisitorLocal(ast.NodeVisitor):
      def generic_visit(self, node):
        global lst_token
        global walkpos
        node._module = module
        #node._parent_name = name
        all_asts.append(node)
        if module not in module_asts:
          module_asts[module]={}
        module_asts[module].append(node)
        #node._walkpos = i
        node._newmodule = module
        #tok =  getattr(n,"first_token", lst_token)
        #n._first_token = tok
        #tok =  getattr(n,"last_token", lst_token)
        #n._last_token = tok
        #lst_token = tok
        #all_asts.append(n)
        if module not in module_asts:
          module_asts[module]={}            
        #module_asts[module].append(n)
        walkpos = walkpos +1
        ast.NodeVisitor.generic_visit(self, node)
    dfvistor = DFVisitorLocal()
    walkpos = 1
    dfvistor.visit(start_node)

"""the token size metric above gives us an idea of the size of the ast nodes, are they large and full of data?
we could use that plus the distance metric to create a new pca variable

"""

def append_typename(f,v): 
    tn = type(v).__name__ 
    return f + "_"+ tn        

#mem_status()
# First we iterate over all the modules that are not built in
# and find the globals that are modules and for each of those we parse the ast of the module.

def process_node(vn,f,qt,i,vt,vin):
  if vn not in user_index:
    user_index[vn]=[]
  user_index[vn].append(i)
  from_node =reverse_index[i]
  return dict(
              module= getattr(i,"_module",i._newmodule),
              #parent_name= i._parent_name,
              from_node=from_node, 
              from_node_obj=i, 
              from_type=qt,
              field=f,
              #n=n,
              value=vn,
              value_type=vt,
              value_index=vin,
              width = vin - from_node,
              )

# who uses this nodes?
reverse_index = {}
user_index = {}
for n,o in enumerate(all_asts):
  reverse_index[o]=n
#mem_status()
def flatten_ast_to_array(i):
  qt = type(i).__name__
  print(qt)
  stack = []  

  for f,v in ast.iter_fields(i):    
  
    if isinstance(v,list):
      for n, y in enumerate(v):
        vt=type(y).__name__
        if y in reverse_index:
          vn = reverse_index[y]          
          stack.append(process_node(y,f,qt,i,vt,vn))
    elif v in reverse_index:
      vn = reverse_index[v]
      
      vt=type(v).__name__
      stack.append(process_node(v,f,qt,i,vt,vn))
    elif isinstance(v,int):
      # int
      pass
    elif isinstance(v,dict):
      # int
      pass
    elif isinstance(v,tuple):
      # int
      pass
    elif isinstance(v,str):
      # int
      pass
    elif isinstance(v,bytes):
      # int
      pass
    elif str(type(v)   ) == "<class 'ellipsis'>":
      pass
    elif isinstance(v,float):
      # int
      pass
    elif v is None:
      # null
      pass
    elif isinstance(v, AST):
      #vt = str(type(v)   )
      vt = "ast"+type(v).__name__  
      vn = reverse_index[v]
      stack.append(
          process_node(v,f,qt,i,vt,vn))
    else:
      vt = str(type(v)   )
      raise Exception(vt)
    
    
  return stack
#
array_asts=[]
for i,x in enumerate(all_asts):
  #print(x)
  for t in flatten_ast_to_array(x):
    t['node_pos']=i
    array_asts.append(t)

    #print(t)
