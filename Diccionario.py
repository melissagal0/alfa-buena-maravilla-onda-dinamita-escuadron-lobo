import time

# ====================================================================
# CLASE 1: NORMALIZADOR DE TEXTO
# ====================================================================
class Normalizador:
    # El metodo __init__ se ejecuta cuando creamos nuestro "departamento"
    def __init__(self):
        # Un pequeño diccionario para limpiar las vocales con tilde
        self.mapa_letras = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u'
        }

    def limpiar_texto(self, texto):
        # Validacion: si nos pasan texto vacio, lanzamos un error claro
        if texto == "" or texto.isspace():
            raise ValueError("Error: El texto esta vacio.")

        texto_limpio = ""
        texto_minusculas = texto.lower() # Todo a minusculas

        # Recorremos letra por letra
        for letra in texto_minusculas:
            if letra in self.mapa_letras:
                texto_limpio += self.mapa_letras[letra]
            elif letra.isalpha() or letra.isspace():
                # isalpha() verifica si es una letra normal (a-z)
                texto_limpio += letra
            else:
                # Si es un numero o simbolo, ponemos un espacio
                texto_limpio += " "

        # split() separa el texto por espacios y nos da una lista de palabras
        return texto_limpio.split()


# ====================================================================
# CLASE 2: TABLA HASH (Estructura propia)
# ====================================================================
class TablaHash:
    def __init__(self, tamano_tabla=100):
        # Esta es la base de nuestra tabla hash: la capacidad de cubetas (buckets)
        self.capacidad = tamano_tabla
        self.buckets = []
        
        # Creamos una lista de listas. Es decir, 100 listas vacias.
        # Cada lista vacia es un "bucket" donde guardaremos palabras.
        for numero in range(self.capacidad):
            self.buckets.append([])

    def _funcion_hash(self, palabra):
        # La funcion hash convierte una palabra de texto a un numero entero (indice)
        suma_ascii = 0
        for letra in palabra:
            suma_ascii += ord(letra) # ord() obtiene el valor numerico de la letra
            
        # El modulo (%) asegura que el numero no pase de la cantidad de buckets (100)
        return suma_ascii % self.capacidad

    def insertar(self, palabra):
        # 1. Calculamos en que bucket debe ir la palabra
        indice = self._funcion_hash(palabra)
        bucket_destino = self.buckets[indice]

        # 2. RESOLUCION DE COLISIONES
        # Revisamos si la palabra ya existe dentro de ese bucket especifico
        # Cada elemento guardado es una pequeña lista asi: ["palabra", frecuencia]
        for elemento in bucket_destino:
            if elemento[0] == palabra:
                # Si la encuentra, solo aumenta el contador de frecuencia y termina
                elemento[1] += 1
                return 

        # 3. Si el ciclo termina y no la encontro, es una palabra nueva.
        # La guardamos en el bucket con una frecuencia inicial de 1.
        bucket_destino.append([palabra, 1])

    def obtener_datos(self):
        # Este metodo simplemente recorre todos los buckets para darnos 
        # una sola lista con todas las palabras y sus frecuencias.
        resultado_final = []
        for bucket in self.buckets:
            for elemento in bucket:
                resultado_final.append(elemento)
        return resultado_final


# ====================================================================
# CLASE 3: ORDENADOR (Merge Sort y Quick Sort)
# ====================================================================
class Ordenador:
    # --- MERGE SORT (O(n log n)) ---
    def merge_sort(self, lista):
        # Si la lista tiene 1 elemento o menos, ya esta ordenada
        if len(lista) <= 1:
            return lista

        # Divide el problema en dos mitades
        medio = len(lista) // 2
        izquierda = lista[:medio]
        derecha = lista[medio:]

        # La recursividad (llamarse a si misma) sigue partiendo la lista
        izquierda_ordenada = self.merge_sort(izquierda)
        derecha_ordenada = self.merge_sort(derecha)

        # Junta todo en orden
        return self._mezclar(izquierda_ordenada, derecha_ordenada)

    def _mezclar(self, izquierda, derecha):
        resultado = []
        i = 0
        j = 0

        # Compara elementos de ambas listas y mete el mas pequeño al resultado
        # Recuerda: [0] es la palabra, [1] es la frecuencia
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i][0] <= derecha[j][0]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado


    # --- QUICK SORT (O(n log n)) ---
    def quick_sort(self, lista):
        if len(lista) <= 1:
            return lista

        # Escoge un punto de apoyo llamado "pivote"
        pivote = lista[len(lista) // 2]
        
        menores = []
        iguales = []
        mayores = []

        # Separa los elementos comparandolos con el pivote
        for elemento in lista:
            if elemento[0] < pivote[0]:
                menores.append(elemento)
            elif elemento[0] == pivote[0]:
                iguales.append(elemento)
            else:
                mayores.append(elemento)

        return self.quick_sort(menores) + iguales + self.quick_sort(mayores)


# ====================================================================
# CLASE 4: CRONOMETRO DE PRUEBAS EMPIRICAS
# ====================================================================
class Cronometro:
    def generar_texto(self, cantidad):
        palabras = ["manzana", "codigo", "python", "clase", "tarea"]
        texto = []
        for i in range(cantidad):
            texto.append(palabras[i % len(palabras)])
        return " ".join(texto)

    def ejecutar_pruebas(self):
        tamanos = [100, 1000, 10000]
        print("\n--- PRUEBAS DE TIEMPO EMPIRICO ---")
        
        normalizador = Normalizador()
        ordenador = Ordenador()

        for cantidad in tamanos:
            texto = self.generar_texto(cantidad)
            palabras = normalizador.limpiar_texto(texto)

            tabla = TablaHash(tamano_tabla=1000)
            for p in palabras:
                tabla.insertar(p)
            lista_unicas = tabla.obtener_datos()

            inicio_m = time.time()
            ordenador.merge_sort(lista_unicas)
            fin_m = time.time()

            inicio_q = time.time()
            ordenador.quick_sort(lista_unicas)
            fin_q = time.time()

            print(f"Texto de {cantidad} palabras:")
            print(f"  Merge Sort: {fin_m - inicio_m:.6f} seg")
            print(f"  Quick Sort: {fin_q - inicio_q:.6f} seg")
            print("-" * 30)


# ====================================================================
# PUNTO DE INICIO DEL PROGRAMA
# ====================================================================
if __name__ == "__main__":
    texto_ejemplo = "Hola!! Pepe hace su tarea de programacion. Hola Pepe."
    print("Texto original:", texto_ejemplo)

    try:
        # 1. Limpiamos
        normalizador = Normalizador()
        palabras_sueltas = normalizador.limpiar_texto(texto_ejemplo)

        # 2. Usamos nuestra Tabla Hash Formal
        tabla_hash = TablaHash(tamano_tabla=50) # Creamos 50 buckets
        for palabra in palabras_sueltas:
            tabla_hash.insertar(palabra)
        
        datos_listos = tabla_hash.obtener_datos()

        # 3. Ordenamos
        ordenador = Ordenador()
        datos_ordenados = ordenador.merge_sort(datos_listos)

        print("\nDiccionario Final:")
        for elemento in datos_ordenados:
            print(f" -> {elemento[0]}: {elemento[1]} apariciones")

    except ValueError as e:
        print(e)

    # 4. Medimos tiempos
    pruebas = Cronometro()
    pruebas.ejecutar_pruebas()