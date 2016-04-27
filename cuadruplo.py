class cuadruplo:

    def __init__(self, c_id, operador, operando1, operando2, resultado):
        self.c_id     = c_id
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado   = resultado

cuadruplos = []
cuadCont = 1

def add_cuadruplo(operador, operando1, operando2, resultado):
    global cuadruplos
    global cuadCont
    cuadruplos.append(cuadruplo(cuadCont, operador, operando1, operando2, resultado))
    cuadCont += 1

def find_cuadruplo(c_id):
    global cuadruplos
    for cuad in cuadruplos:
        if cuad.c_id == c_id:
            return cuad

def set_operador(c_id, operador):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        cuad.operador = operador

def set_operando1(c_id, operando1):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        cuad.operando1 = operando1

def set_operando2(c_id, operando2):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        cuad.operando2 = operando2

def set_resultado(c_id, resultado):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        cuad.resultado = resultado

def get_operador(c_id):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        return cuad.operador

def get_operando1(c_id):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        return cuad.operando1

def get_operando2(c_id):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        return cuad.operando2

def get_resultado(c_id):
    global cuadruplos
    cuad = find_cuadruplo(c_id)
    if cuad:
        return cuad.resultado

def print_cuadruplos():
    global cuadruplos
    print("Cuadruplos:")
    if cuadruplos:
        for cuad in cuadruplos:
            print (" ID: " + str(cuad.c_id) , " Operador: " + str(cuad.operador) , " Operando1: " + str(cuad.operando1) , " Operando2: " + str(cuad.operando2) , " Resultado: " + str(cuad.resultado))
    else:
        print("No hay cuadruplos.")
    print ("\n")
