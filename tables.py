import sys

const_table = []
var_table = []
dir_proc = []
temp_table = []

# Variable Table Functions
class variable:
	def __init__(self, var_name, var_value, var_type, var_dir):
		self.var_name= var_name
		self.var_value= var_value
		self.var_type = var_type
		self.var_dir = var_dir

def add_var_table(var_name, var_value, var_type, var_dir):
	global var_table
	var_table.append(variable(var_name, var_value, var_type, var_dir))

def add_var_table(var_name, var_type, var_dir):
	global var_table
	if var_type == 'int':
		var_table.append(variable(var_name, 0 , var_type, var_dir))
	elif var_type == 'float':
		var_table.append(variable(var_name, 0.0 , var_type, var_dir))
	elif var_type == 'string':
		var_table.append(variable(var_name, ' ' , var_type, var_dir))
	elif var_type == 'bool':
		var_table.append(variable(var_name, 'false' , var_type, var_dir))

def find_global_var_table(var_name):
    global var_table
    for v in var_table:
        if v.var_name == var_name:
            return v

def get_value_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.var_value

def set_value_global_var_table(var_name, value):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		v.value = value

def get_type_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.var_type

def get_dir_global_var_table(var_name):
	global var_table
	v = find_global_var_table(var_name)
	if v:
		return v.var_dir

def find_var_table(v_table, var_name):
    for v in v_table:
        if v.var_name == var_name:
            return v

def get_value_var_table(vtable, var_name):
	global var_table
	v = find_var_table(vtable, var_name)
	if v:
		return v.var_value

def set_value_var_table(vtable, var_name, value):
	global var_table
	v = find_var_table(vtable, var_name)
	if v:
		v.var_value = value

def get_type_var_table(vtable, var_name):
	global var_table
	v = find_var_table(vtable, var_name)
	if v:
		return v.var_type

def get_dir_var_table(vtable, var_name):
	global var_table
	v = find_var_table(vtable, var_name)
	if v:
		return v.var_dir

def print_var_table():
	global var_table
	print("Tabla de Variables Globales:")
	if var_table:
		for var in var_table:
			print (" NAME: " + str(var.var_name) , " VALUE: " + str(var.var_value) , " TYPE: " + str(var.var_type) , " DIR: " + str(var.var_dir))
	else:
		print ("No variables declared")
	print("\n")

def clear_var_table():
	global var_table
	var_table[:] = []

# Tempral Table Functions
class temporal:
	def __init__(self, temp_value, temp_type, temp_dir):
		self.temp_value= temp_value
		self.temp_type = temp_type
		self.temp_dir = temp_dir

def add_temp_table(temp_value, temp_type, temp_dir):
	global temp_table
	temp_table.append(temporal(temp_value, temp_type, temp_dir))

def find_temp_table(temp_dir):
    global temp_table
    for te in temp_table:
        if te.temp_dir == temp_dir:
            return te

def get_value_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.temp_value

def set_value_temp_table(temp_dir, value):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		te.temp_value = value

def get_type_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.temp_type

def get_dir_temp_table(temp_dir):
	global temp_table
	te = find_temp_table(temp_dir)
	if te:
		return te.temp_dir

def clear_temp_table():
	global temp_table
	temp_table[:] = []

#Constant Table Functions
class constant:
	def __init__(self, const_value, const_type, const_dir):
		self.const_value= const_value
		self.const_type = const_type
		self.const_dir = const_dir

def add_const_table(const_value, const_type, const_dir):
	global const_table
	const_table.append(constant(const_value, const_type, const_dir))

def print_const_table():
	global const_table
	print("Tabla de Constantes:")
	if const_table:
		for const in const_table:
			print (" VALUE: " + str(const.const_value) , " TYPE: " + str(const.const_type) , " DIR: " + str(const.const_dir))
	else:
		print ("No constants declared")
	print("\n")

def find_const_table(const_value):
	global const_table
	for const in const_table:
		if const.const_value == const_value:
			return const

def get_dir_const_table(const_value):
	global const_table
	for const in const_table:
		if const.const_value == const_value:
			return const.const_dir

def get_value_const_table(const_dir):
	global const_table
	for const in const_table:
		if const.const_dir == const_dir:
			return const.const_value

def get_type_const_table(const_value):
	global const_table
	for const in const_table:
		if const.const_value == const_value:
			return const.const_type

def clear_const_table():
	global const_table
	const_table[:] = []

#DirProc Functions
class function:
	def __init__(self, func_name, func_ret, func_dir):
		self.func_name= func_name
		self.func_ret = func_ret
		self.func_dir = func_dir
		self.func_vars = []
		self.func_params = []

def add_dir_proc(func_name, func_ret, func_dir):
	global dir_proc
	dir_proc.append(function(func_name, func_ret, func_dir))

def add_param_dir_proc(func_name, var_name, var_value, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_params.append(variable(var_name, var_value, var_type, var_dir))

def add_param_dir_proc(func_name, var_name, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		if var_type == 'int':
			d.func_params.append(variable(var_name, 0 , var_type, var_dir))
		elif var_type == 'float':
			d.func_params.append(variable(var_name, 0.0 , var_type, var_dir))
		elif var_type == 'string':
			d.func_params.append(variable(var_name, ' ' , var_type, var_dir))
		elif var_type == 'bool':
			d.func_params.append(variable(var_name, 'false' , var_type, var_dir))

def add_var_dir_proc(func_name, var_name, var_value, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		d.func_vars.append(variable(var_name, var_value, var_type, var_dir))

def add_var_dir_proc(func_name, var_name, var_type, var_dir):
	global dir_proc
	d = find_dir_proc(func_name)
	if d :
		if var_type == 'int':
			d.func_vars.append(variable(var_name, 0 , var_type, var_dir))
		elif var_type == 'float':
			d.func_vars.append(variable(var_name, 0.0 , var_type, var_dir))
		elif var_type == 'string':
			d.func_vars.append(variable(var_name, ' ' , var_type, var_dir))
		elif var_type == 'bool':
			d.func_vars.append(variable(var_name, 'false' , var_type, var_dir))

def find_dir_proc(func_name):
    global dir_proc
    for d in dir_proc:
        if d.func_name == func_name:
            return d

def get_type_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_ret

def get_dir_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_dir

def get_params_dir_proc(proc):
	return proc.func_params

def get_vars_dir_proc(func_name):
	global dir_proc
	d = find_dir_proc(func_name)
	if d:
		return d.func_vars

def print_dir_proc():
	global dir_proc
	print("Directorio de procedimientos:")
	for d in dir_proc:
		if d:
			print(" NAME: " +  str(d.func_name) , " TYPE: " + str(d.func_ret) , " DIR: " + str(d.func_dir))
			#print("Parameters:")
			#for param in d.func_params:
			#	print(" NAME: ", param.var_name, " VALUE: ", param.var_value, " TYPE: ", param.var_type, " DIR: ", param.var_dir)
			print("Variables:")
			for var in d.func_vars:
				print(" NAME: " + str(var.var_name) , " VALUE: " + str(var.var_value) , " TYPE: " + str(var.var_type) , " DIR: " + str (var.var_dir))
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
