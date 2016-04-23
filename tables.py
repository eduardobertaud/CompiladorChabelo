import sys

class variable:
	def __init__(self, var_name, var_type, var_dir):
		self.var_name= var_name
		self.var_type = var_type
		self.var_dir = var_dir

class function:
	def __init__(self, func_name, func_ret, func_dir):
		self.func_name= func_name
		self.func_ret = func_ret
		self.func_dir = func_dir
		self.func_vars = []
		self.func_params = []

var_table = []
dir_proc = []

def add_var_table(var_name, var_type, var_dir):
	global var_table
	var_table.append(variable(var_name, var_type, var_dir))

def add_dir_proc(func_name, func_ret, func_dir):
	global dir_proc
	dir_proc.append(function(func_name, func_ret, func_dir))

def add_param_dir_proc(func_name, var_name, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_params.append(variable(var_name, var_type, var_dir))

def add_var_dir_proc(func_name, var_name, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_vars.append(variable(var_name,var_type,var_dir))

def find_dir_proc(func_name):
    global dir_proc
    for d in dir_proc:
        if d.func_name == func_name:
            return d
            sys.exit()

def find_global_var_table(var_name):
    global var_table
    for v in var_table:
        if v.var_name == var_name:
            return v
            sys.exit()

def find_var_table(v_table, var_name):
    for v in v_table:
        if v.var_name == var_name:
            return v
            sys.exit()

def get_params_dir_proc(proc):
	return proc.func_params

def get_vars_dir_proc(proc):
	return proc.func_vars

def print_var_table():
	global var_table
	print("Tabla de Variables:")
	if var_table:
		for var in var_table:
			print (" NAME ", var.var_name, " TYPE ", var.var_type, " DIR ", var.var_dir)
	else:
		print ("No variables declared")
	print("\n")

def print_dir_proc():
	global dir_proc
	print("Directorio de procedimientos:")
	for d in dir_proc:
		if d:
			print(" NAME ", d.func_name, " TYPE ", d.func_ret, " DIR ", d.func_dir)
			print("Parameters:")
			for param in d.func_params:
				print(" NAME ", param.var_name, " TYPE ", param.var_type, " DIR ", param.var_dir)
			print("Variables:")
			for var in d.func_vars:
				print(" NAME ", var.var_name, " TYPE ", var.var_type, " DIR ", var.var_dir)
			print ("\n")
		else:
			print ("No functions declared")
			print ("\n")

def clear_var_table():
	var_table[:] = []

def clear_dir_proc():
	for dp in dir_proc:
		dp.func_params[:] = []
		dp.func_vars[:] = []
	dir_proc[:] = []
