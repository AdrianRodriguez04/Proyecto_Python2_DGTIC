import mysql.connector
from getpass import getpass

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Cortana33',
    database='proyecto'
)

cursor = conexion.cursor()

class Mesa:
    def __init__(self, numero, capacidad):
        self.numero = numero
        self.capacidad = capacidad
        self.estado = self.cargarEstadoBD()

    def cargarEstadoBD(self):
        consulta = "SELECT estado FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (self.numero,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            print(f"Error: La mesa {self.numero} no existe en la base de datos")
            return 'libre'

    def reservar(self):
        if self.estado == 'libre':
            self.estado = 'ocupada'
            consulta = "UPDATE mesas SET estado = 'ocupada' WHERE numero = %s"
            cursor.execute(consulta, (self.numero,))
            conexion.commit()
            return True
        return False
    
    def liberar(self):
        if self.estado == 'ocupada':
            self.estado = 'libre'
            consulta = "UPDATE mesas SET estado = 'libre' WHERE numero = %s"
            cursor.execute(consulta, (self.numero,))
            conexion.commit()
            print(f"Mesa {self.numero} liberada correctamente.")
            return True
        return False
    
    def verificarEstado (self):
        consulta = "SELECT estado FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (self.numero,))
        estadoBD = cursor.fetchone()
        if estadoBD:
            self.estado = estadoBD[0]
        return self.estado
    
class Pedido:
    def __init__(self, clienteId):
        self.clienteId = clienteId
        self.items = []
        self.estado = 'preparando'
        self.id = None

    def agregarItem(self, itemId, cantidad = 1):
        self.items.append((itemId, cantidad))

    def guardarPedido(self):
        consulta = "INSERT INTO pedidos (clienteId, estado) VALUES (%s,%s)"
        cursor.execute(consulta,(self.clienteId, self.estado))
        conexion.commit

        self.id = cursor.lastrowid

        for itemId, cantidad in self.items:
            consulta = "INSERT INTO detallePedidos (pedidoId, itemId, cantidad) VALUES (%s,%s,%s)"
            cursor.execute(consulta, (self.id, itemId, cantidad))
            conexion.commit()

        print(f"Pedido {self.id} guardado correctamente.")

    def eliminarItem(self, itemId):
        self.items = [(i, q) for (i, q) in self.items if 1 != itemId]
        print(f"Item {itemId} eliminado del pedido.")

    def calcularTotal(self):
        total = 0
        for itemId, cantidad in self.items:
            consulta = "SELECT precio FROM menu WHERE id = %s"
            cursor.execute(consulta, (itemId,))
            resultado = cursor.fetchone()
            if resultado:
                precio = resultado[0]
                total += precio * cantidad
        return total
    
    def cambiarEstado(self, nuevoEstado):
        if self.id:
            consulta = "UPDATE pedido SET estado = %s WHERE id = %s"
            cursor.execute(consulta, (nuevoEstado, self.id))
            conexion.commit()
            self.estado = nuevoEstado
            print(f"EStado del pedido {self.id} actualizado a '{nuevoEstado}'")
        else:
            print("Error: EL pedido no ha sido guardado en la base de datos")

class Menu:
    def __init__(self):
        self.items = []
        self.cargarBD()

    def cargarBD(self):
        consulta = "SELECT id, nombre, descripcion, precio FROM menu WHERE activo = 1"
        cursor.execute(consulta)
        for id, nombre, descripcion, precio in cursor.fetchall():
            self.items.append(ItemMenu(id, nombre, descripcion, precio))

    def agregarItem(self, nombre, descripcion, precio):
        consulta = "INSERT INTO menu (nombre, descripcion, precio) VALUES (%s,%s,%s,1)"
        cursor.execute(consulta,(nombre,descripcion,precio))
        conexion.commit()
        self.items.append(ItemMenu(cursor.lastrowid, nombre, descripcion, precio))
        print(f"Item '{nombre}' añadido al menu")

    def eliminarItem(self, nombre):
        consulta = "SELECT id FROM menu WHERE nombre = %s"
        cursor.execute(consulta, (nombre,))
        resultado = cursor.fetchone()

        if resultado:
            itemId = resultado[0]
            consulta = "UPDATE menu SET activo = 0 WHERE id = %s"
            cursor.execute(consulta, (itemId,))
            conexion.commit()

            self.items = [item for item in self.items if item.nombre != nombre]
            print(f"Item '{nombre}' desactivado correctamente.")
        else:
            print(f"Error: El item '{nombre}' no existe en el menú.")

    def mostrarMenu(self):
        if not self.items:
            print("El menú está vació")
            return
        
        print("\n--- MENÚ ---")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item.nombre} - ${item.precio}")

class ItemMenu:
    def __init__(self, id, nombre, descripcion, precio):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mesaAsignada = None
        self.pedidoActual = None
        self.id = None

        consulta = "SELECT id FROM clientes WHERE nombre = %s"
        cursor.execute(consulta, (self.nombre,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"El cliente {self.nombre} ya existe.")
            self.id = resultado[0]
        else:
            consulta = "INSERT INTO clientes (nombre) VALUES (%s)"
            cursor.execute(consulta, (self.nombre,))
            conexion.commit()
            self.id = cursor.lastrowid
            print(f"Cliente {self.nombre} registrado correctamente")

    def asignarMesa(self, mesa):
        self.mesaAsignada = mesa
        consulta = "UPDATE clientes SET mesaAsignada = %s WHERE nombre = %s"
        cursor.execute(consulta, (mesa.numero, self.nombre))
        conexion.commit()

    def realizarPedido (self, items):
        self.pedidoActual = Pedido(self.id)
        for itemId, cantidad in items:
            self.pedidoActual.agregarItem(itemId,cantidad)
        self.pedidoActual.guardarPedido()

    def verPedido(self):
        if self.pedidoActual:
            print("\n--- Detalles del Pedido ---")
            total = 0
            for itemId, cantidad in self.pedidoActual.items:
                consulta = "SELECT nombre, precio FROM menu WHERE id = %s"
                cursor.execute(consulta, (itemId,))
                resultado = cursor.fetchone()
                if resultado:
                    nombre, precio = resultado
                    subtotal = precio * cantidad
                    print(f"{nombre} - Cantidad: {cantidad} - Precio unitario: ${precio:.2f} MXN - Subtotal: ${subtotal:.2f} MXN")
                    total += subtotal
            print(f"Total a pagar: ${total:.2f} MXN")
            return total
        else:
            print("No hay pedidos registrados.")
            return 0
    
class Restaurante:
    def __init__(self):
        self.mesas = []
        self.menu = Menu()
        self.clientes = []
        self.cargarBD()

    def cargarBD(self):
        consulta = "SELECT numero, capacidad, estado FROM mesas"
        cursor.execute(consulta)
        for numero, capacidad, estado in cursor.fetchall():
            mesa = Mesa(numero, capacidad)
            mesa.estado = estado
            self.mesas.append(mesa)

    def añadirMesa(self, numero, capacidad):
        consulta = "SELECT numero FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (numero,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Error: La mesa {numero} ya existe")
            return False
        
        consulta = "INSERT INTO mesas (numero, capacidad, estado) VALUES (%s,%s,'libre')"
        cursor.execute(consulta,(numero,capacidad))
        conexion.commit()

        mesa = Mesa(numero, capacidad)
        self.mesas.append(mesa)
        print(f"Mesa {numero} añadida correctamente")
        return True
    
    def eliminarMesa(self, numero):
        consulta = "DELETE FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (numero,))
        conexion.commit()

        self.mesas = [mesa for mesa in self.mesas if mesa.numero != numero]
        print (f"Mesa {numero} eliminada correctamente")
        return True
    
    def mostrarMesasDisponibles(self):
        consulta = "SELECT numero, capacidad FROM mesas WHERE estado = 'libre'"
        cursor.execute(consulta)
        for numero, capacidad in cursor.fetchall():
            print(f"Mesa {numero} (Capacidad: {capacidad}) está disponible")

    def hacerReservacion (self, cliente, numeroMesa):
        consulta = "SELECT estado FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (numeroMesa,))
        resultado = cursor.fetchone()

        if resultado and resultado[0] == 'libre':
            consulta = "UPDATE mesas SET estado = 'ocupada' WHERE numero = %s"
            cursor.execute(consulta, (numeroMesa,))

            mesa = next((mesa for mesa in self.mesas if mesa.numero == numeroMesa), None)

            if mesa:
                mesa.reservar()
                cliente.asignarMesa(mesa)
                self.clientes.append(cliente)
                conexion.commit()
                print(f"Mesa {numeroMesa} reservada para {cliente.nombre}.")
                return True
            else:
                print(f"Error: La mesa {numeroMesa} no existe en la lista de mesas")
                return False
        else: 
            print(f"Mesa {numeroMesa} no disponible")
            return False
    
    def gestionarPedido(self, cliente, items):
        if cliente in self.clientes:
            cliente.realizarPedido(items)
            print(f"Pedido realizado para {cliente.nombre}.")
        else:
            print("Cliente no registrado.")

    def mostrarMenu(self):
        self.menu.mostrarMenu()

    def escogerItemsMenu(self,cliente):
        if cliente in self.clientes:
            self.mostrarMenu()
            itemsSeleccionados = []
            while True:
                try:
                    opcion = input("Ingrese el número del item que desea (o el número '0' para terminar): ")
                    if opcion == '0':
                        break

                    indice = int(opcion) - 1
                    if 0 <= indice < len(self.menu.items):
                        item = self.menu.items[indice]
                        cantidad = int(input(f"Ingrese la cantidad de '{item.nombre}' que desea: "))
                        itemsSeleccionados.append((item.id, cantidad))
                        print (f"Item '{item.nombre}' añadido al pedido")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Ingresa un número valido")
            if itemsSeleccionados:
                self.gestionarPedido(cliente, itemsSeleccionados)
            else:
                print("No se seleccionaron items.")
        else:
            print("Cliente no registrado")

    def mostrarCuenta(self, cliente):
        if cliente in self.clientes:
            cliente.verCuenta()
        else:
            print("Cliente no registrado")

class MenuCliente:
    def __init__(self, restaurante, cliente):
        self.restaurante = restaurante
        self.cliente = cliente

    def mostrarMenu(self):
        while True:
            print("\nMenú Comensal")
            print("1. Ver Menú")
            print("2. Escoger Items del Menú")
            print("3. Ver Pedido")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.restaurante.mostrarMenu()
            elif opcion == "2":
                self.restaurante.escogerItemsMenu(self.cliente)
            elif opcion == "3":
                self.cliente.verPedido()
            elif opcion == "4":
                if self.cliente.mesaAsignada:
                    if self.cliente.mesaAsignada.liberar():
                        print(f"Mesa {self.cliente.mesaAsignada.numero} liberada.")
                    else:
                        print(f"Error: No se pudo liberar la mesa {self.cliente.mesaAsignada.numero}.")
                consulta = "UPDATE clientes SET mesaAsignada = NULL WHERE nombre = %s"
                cursor.execute(consulta, (self.cliente.nombre,))
                conexion.commit()
                self.cliente.mesaAsignada = None
                print("Gracias por su visita. Vuelva pronto! :D")
                break
            else:
                print("Opción inválida :( Intente de nuevo.")

class MenuAdministrador:
    def __init__(self,restaurante):
        self.restaurante = restaurante

    def autenticar(self):
        usuario = input("Ingrese el nombre del usuario: ")
        contraseña = getpass("Ingrese la contraseña: ")
        if usuario == "admin" and contraseña == "password":
            return True
        else:
            print("Acceso denegado")
            return False
        
    def mostrarMenu(self):
        if not self.autenticar():
            return
        
        while True:
            print("\nMenú Administrador")
            print("1. Añadir Mesa")
            print("2. Eliminar Mesa")
            print("3. Mostrar Mesas Disponibles")
            print("4. Añadir Item al Menú")
            print("5. Eliminar Item del Menu")
            print("6. Mostrar Items del Menú")
            print("7. Ver Clientes")
            print("8. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                numero = int(input("Número de la mesa: "))
                capacidad = int(input("Capacidad de la mesa: "))
                self.restaurante.añadirMesa(numero,capacidad)
            elif opcion == "2":
                numero = int(input("Número de la mesa a eliminar: "))
                self.restaurante.eliminarMesa(numero)
            elif opcion == "3":
                self.restaurante.mostrarMesasDisponibles()
            elif opcion == "4":
                nombre = input("Nombre del item: ")
                descripcion = input("Descripción: ")
                precio = float(input("Precio: "))
                self.restaurante.menu.agregarItem(nombre, descripcion, precio)
            elif opcion == "5":
                nombre = input("Nombre del item a eliminar: ")
                self.restaurante.menu.eliminarItem(nombre)
            elif opcion == "6":
                self.restaurante.mostrarMenu()
            elif opcion == "7":
                consulta = "SELECT * FROM clientes"
                cursor.execute(consulta)
                for cliente in cursor.fetchall():
                    print(cliente)
            elif opcion == "8":
                print("Saliendo del menú de administrador.")
                break
            else:
                print("Opción inválida. Intentalo de nuevo.")

class Main:
    def __init__(self):
        self.restaurante = Restaurante()
    
    def mostrarMenuPrincipal(self):
        while True:
            print("\nMenú Principal")
            print("1. Menú Cliente")
            print("2. Menú Administrador")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                nombreCliente = input("Ingrese su nombre: ")
                cliente = Cliente(nombreCliente)

                if not cliente.mesaAsignada:
                    print("\nMesas disponibles: ")
                    self.restaurante.mostrarMesasDisponibles()
                    while True:
                            numeroMesa = int(input("Ingrese el número de la mesa que desea reservar: "))
                            mesaReservada = self.restaurante.hacerReservacion(cliente, numeroMesa)
                            if mesaReservada:
                                print(f"Mesa {numeroMesa} asignada exitosamente.")
                                break
                            else:
                                print("Esa mesa no esta disponible.")

                menuC = MenuCliente(self.restaurante, cliente)
                menuC.mostrarMenu()
            elif opcion == "2":
                menuA = MenuAdministrador(self.restaurante)
                menuA.mostrarMenu()
            elif opcion == "3":
                print("Gracias por usar el sistema de nuestro restaurantE. ¡Hasta pronto! :D")
                break
            else:
                print("Opción invalida.")

if __name__ == "__main__":
    principal = Main()
    principal.mostrarMenuPrincipal()
