int_global = 0
float_global = 2000
string_global = 4000

int_local=6000
float_local=8000
string_local=10000

int_const=15000
float_const=17000
string_const=19000

int_temp=12000
float_temp=13000
string_tamp=14000


def global_memory_assignment(v_type):
    global int_global
    global float_global
    global string_global
    global memory
    if v_type == 'int':
      memory = int_global
      int_global += 1
    elif v_type == 'float':
      memory = float_global
      float_global += 1
    elif v_type == 'string':
      memory = string_global
      string_global += 1
    return memory

def local_memory_assignment(v_type):
    global int_local
    global float_local
    global string_local
    global memory
    if v_type == 'int':
      memory = int_local
      int_local += 1
    elif v_type == 'float':
      memory = float_local
      float_local += 1
    elif v_type == 'string':
      memory = string_local
      string_local += 1
    return memory

def const_memory_assignment(v_type):
    global int_const
    global float_const
    global string_const
    global memory
    if v_type == 'int':
      memory = int_const
      int_const += 1
    elif v_type == 'float':
      memory = float_const
      float_const += 1
    elif v_type == 'string':
      memory = string_const
      string_const += 1
    return memory

def temp_memory_assignment(v_type):
    global int_temp
    global float_temp
    global string_temp
    global memory
    if v_type == 'int':
      memory = int_temp
      int_temp += 1
    elif v_type == 'float':
      memory = float_temp
      float_temp += 1
    elif v_type == 'string':
      memory = string_temp
      string_temp += 1
    return memory
