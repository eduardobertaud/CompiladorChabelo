int_global = 0
float_global = 1000
string_global = 2000
bool_global = 3000

int_local=4000
float_local=50000
string_local=6000
bool_local=7000

int_const=8000
float_const=9000
string_const=10000
bool_const=11000

int_temp=12000
float_temp=13000
string_temp=14000
bool_temp=15000


def global_memory_assignment(v_type, offset = 0):
    global int_global
    global float_global
    global string_global
    global bool_global
    global memory
    if v_type == 'int':
        memory = int_global
        int_global += 1 + offset
    elif v_type == 'float':
        memory = float_global
        float_global += 1 + offset
    elif v_type == 'string':
        memory = string_global
        string_global += 1 + offset
    elif v_type == 'bool':
        memory = bool_global
        bool_global += 1 + offset
    return memory

def local_memory_assignment(v_type, offset = 0):
    global int_local
    global float_local
    global string_local
    global bool_local
    global memory
    if v_type == 'int':
      memory = int_local
      int_local += 1 + offset
    elif v_type == 'float':
      memory = float_local
      float_local += 1 + offset
    elif v_type == 'string':
      memory = string_local
      string_local += 1 + offset
    elif v_type == 'bool':
      memory = bool_local
      bool_local += 1 + offset
    return memory


def const_memory_assignment(v_type):
    global int_const
    global float_const
    global string_const
    global bool_const
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
    elif v_type == 'bool':
      memory = bool_const
      bool_const += 1
    return memory

def temp_memory_assignment(v_type):
    global int_temp
    global float_temp
    global string_temp
    global bool_temp
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
    elif v_type == 'bool':
      memory = bool_temp
      bool_temp += 1
    return memory
