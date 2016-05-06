import sys
import copy

const_table = []
var_table = []
dir_proc = []
backup_proc = []
temp_table = []

# Variable Table Functions
class variable:
	def __init__(self, var_name, value, tipo, var_dir,var_size):
		self.var_name= var_name
		self.value= value
		self.tipo = tipo
		self.var_dir = var_dir
		self.var_size = var_size

def add_var_table(var_name, value, tipo, var_dir, var_size = 0):
	global var_table
	var_table.append(variable(var_name, value, tipo, var_dir, var_size))

def find_global_var_table(var_name):
    global var_table
    for v in var_table:
        if v.var_name == var_name:
            return v

def get_value_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.value

def set_value_global_var_table(var_name, value):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		v.value = value

def get_type_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.tipo

def get_dir_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.var_dir

def get_size_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.var_size

def find_var_table(v_table, var_name):
    for v in v_table:
        if v.var_name == var_name:
            return v

def get_value_var_table(vtable, var_name):
	v = find_var_table(vtable, var_name)
	if v:
		return v.value

def set_value_var_table(vtable, var_name, value):
	v = find_var_table(vtable, var_name)
	if v:
		v.value = value

def get_type_var_table(vtable, var_name):
	v = find_var_table(vtable, var_name)
	if v:
		return v.tipo

def get_dir_var_table(vtable, var_name):
	v = find_var_table(vtable, var_name)
	if v:
		return v.var_dir

def get_size_var_table(vtable, var_name):
	v = find_var_table(vtable, var_name)
	if v:
		return v.var_size

def print_var_table():
	global var_table
	print("Tabla de Variables Globales:")
	if var_table:
		for var in var_table:
			print (" NAME: " + str(var.var_name) , " VALUE: " + str(var.value) , " TYPE: " + str(var.tipo) , " DIR: " + str(var.var_dir), " SIZE: " + str (var.var_size))
	else:
		print ("No variables declared")
	print("\n")

def clear_var_table():
	global var_table
	var_table[:] = []

# Temporal Table Functions
class temporal:
	def __init__(self, value, tipo, temp_dir):
		self.value= value
		self.tipo = tipo
		self.temp_dir = temp_dir

def add_temp_table(value, tipo, temp_dir):
	global temp_table
	temp_table.append(temporal(value, tipo, temp_dir))

def find_temp_table(temp_dir):
    global temp_table
    for te in temp_table:
        if te.temp_dir == temp_dir:
            return te

def get_value_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.value

def set_value_temp_table(temp_dir, value):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		te.value = value

def get_type_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.tipo

def get_dir_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.temp_dir

def print_temp_table():
	global temp_table
	print("Tabla de Temporales:")
	if temp_table:
		for temp in temp_table:
			print (" VALUE: " + str(temp.value) , " TYPE: " + str(temp.tipo) , " DIR: " + str(temp.temp_dir))
	else:
		print ("No constants declared")
	print("\n")

def clear_temp_table():
	global temp_table
	temp_table[:] = []

#Constant Table Functions
class constant:
	def __init__(self, value, tipo, const_dir):
		self.value= value
		self.tipo = tipo
		self.const_dir = const_dir

def add_const_table(value, tipo, const_dir):
	global const_table
	const_table.append(constant(value, tipo, const_dir))

def print_const_table():
	global const_table
	print("Tabla de Constantes:")
	if const_table:
		for const in const_table:
			print (" VALUE: " + str(const.value) , " TYPE: " + str(const.tipo) , " DIR: " + str(const.const_dir))
	else:
		print ("No constants declared")
	print("\n")

def find_const_table(value):
	global const_table
	for const in const_table:
		if const.value == value:
			return const

def get_dir_const_table(value):
	global const_table
	for const in const_table:
		if const.value == value:
			return const.const_dir

def get_value_const_table(const_dir):
	global const_table
	for const in const_table:
		if const.const_dir == const_dir:
			return const.value

def get_type_const_table(value):
	global const_table
	for const in const_table:
		if const.value == value:
			return const.tipo

def clear_const_table():
	global const_table
	const_table[:] = []

#DirProc Functions
class function:
	def __init__(self, func_name, func_type, func_dir, func_ret):
		self.func_name= func_name
		self.func_type = func_type
		self.func_dir = func_dir
		self.func_vars = []
		self.func_params = []
		self.func_ret = func_ret

def add_dir_proc(func_name, func_type, func_dir,func_ret = None):
	global dir_proc
	dir_proc.append(function(func_name, func_type, func_dir,func_ret))

def add_param_dir_proc(func_name, var_name, value, tipo, var_dir, var_size = 0):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_params.append(variable(var_name, value, tipo, var_dir, var_size))

def add_var_dir_proc(func_name, var_name, value, tipo, var_dir, var_size = 0):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_vars.append(variable(var_name, value, tipo, var_dir, var_size))

def find_dir_proc(func_name):
    global dir_proc
    for d in dir_proc:
        if d.func_name == func_name:
            return d

def get_type_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_type

def get_return_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_ret

def set_return_dir_proc(func_name,ret):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		d.func_ret = ret

def get_dir_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_dir

def get_params_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_params

def get_vars_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_vars

def generate_copy_dir_proc():
	global dir_proc
	global backup_proc
	backup_proc.append(copy.deepcopy(dir_proc))

def get_copy_dir_proc(name):
	global backup_proc
	for proc in backup_proc[0]:
		if proc.func_name == name:
			return copy.deepcopy(proc)

def print_dir_proc():
	global dir_proc
	print("Directorio de procedimientos:")
	for d in dir_proc:
		if d:
			print(" NAME: " +  str(d.func_name) , " TYPE: " + str(d.func_type) , " DIR: " + str(d.func_dir))
			print("Parameters:")
			for param in d.func_params:
				print(" NAME: ", param.var_name, " VALUE: ", param.value, " TYPE: ", param.tipo, " DIR: ", param.var_dir)
			print("Variables:")
			for var in d.func_vars:
				print(" NAME: " + str(var.var_name) , " VALUE: " + str(var.value) , " TYPE: " + str(var.tipo) , " DIR: " + str (var.var_dir), " SIZE: " + str (var.var_size))
			print ("\n")
		else:
			print ("No functions declared")
			print ("\n")

def clear_dir_proc():
	global dir_proc
	for dp in dir_proc:
		dp.func_params[:] = []
		dp.func_vars[:] = []
	dir_proc[:] = []
