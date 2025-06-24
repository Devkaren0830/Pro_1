def procesar(nombre, edad, ciudad):
    print(f"{nombre}, {edad}, {ciudad}")

def controlador(*args):
    procesar(*args)

controlador("Ana", 30, "Bogotá")

