import mysql.connector

conexion = mysql.connector.connect(
    host='localhost',
    user='empleado',
    password='Cortana33',
    database='restaurante'
)

cursor = conexion.cursor()

class Mesa:
    def __init__(self, numero, capacidad):
        self.numero = numero
        self.capacidad = capacidad
        self.estado = 'libre'

        consulta = "INSERT INTO mesas (numero, capacidad, estado) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (self.numero, self.capacidad, self.estado))
        conexion.commit()

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
    def __init__(self):
        self.items = []
        self.estado = 'preparando'

    def agregarItem(self, item):
        self.items.append(item)

    def eliminarItem(self, item):
        if item in self.items:
            self.items.remove(item)

    def calcularTotal(self):
        return sum(item.precio for item in self.items)
    
    def cambiarEstado(self, nuevoEstado):
        self.estado = nuevoEstado

class Menu:
    def __init__(self):
        self.items = []

    def agregarItem(self, nombre, descripcion, precio):
        self.items.append(ItemMenu(nombre, descripcion, precio))

        consulta = "INSERT INTO menu (nombre, descripcion, precio) VALUES (%s,%s,%s)"
        cursor.execute(consulta,(nombre,descripcion,precio))
        conexion.commit()

    def eliminarItem(self, nombre):
        self.items = [item for item in self.items if item.nombre != nombre]

        consulta = "DELETE FROM menu WHERE nombre = %s"
        cursor.execute(consulta, (nombre,))
        conexion.commit()

    def mostrarMenu(self):
        consulta = "SELECT nombre, descripcion, precio FROM menu"
        cursor.execute(consulta)
        for nombre, descripcion, precio in cursor.fetchall():
            print(f"{nombre}: {descripcion} - ${precio}")

        #for item in self.items:
        #   print(f"{item.nombre}: {item.descripcion} - ${item.precio}")

class ItemMenu:
    def __init__(self, nombre, descripcion, precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mesaAsignada = None
        self.pedidoActual = Pedido()

        consulta = "INSERT INTO clientes (nombre) VALUES (%s)"
        cursor.execute(consulta, (self.nombre,))
        conexion.commit()

    def asignarMesa(self, mesa):
        self.mesaAsignada = mesa
        consulta = "UPDATE clientes SET mesaAsignada = %s WHERE nombre = %s"
        cursor.execute(consulta, (mesa.numero, self.nombre))
        conexion.commit()

    def realizarPedido (self, items):
        for item in items:
            self.pedidoActual.agregarItem(item)

    def verCuenta(self):
        total = self.pedidoActual.calcularTotal()
        print(f"Total a pagar: ${total}")
        return total
    
class Restaurante:
    def __init__(self):
        self.mesas = []
        self.menu = Menu()
        self.clientes = []

    def añadirMesa(self, numero, capacidad):
        self.mesas.append(Mesa(numero, capacidad))

    def eliminarMesa(self, numero):
        self.mesas = [mesa for mesa in self.mesas if mesa.numero != numero]

        consulta = "DELETE FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (numero,))
        conexion.commit()

    def mostrarMesasDisponibles(self):
        consulta = "SELECT numero, capacidad FROM mesas WHERE estado = 'libre'"
        cursor.execute(consulta)
        for numero, capacidad in cursor.fetchall():
            print(f"Mesa {numero} (Capacidad: {capacidad}) está disponible")
        #for mesa in self.mesas:
        #    if mesa.verificarEstado() == 'libre':
        #        print(f"Mesa {mesa.numero} (Capacidad: {mesa.capacidad}) esta disponible.")

    def hacerReservacion (self, cliente, numeroMesa):
        consulta = "SELECT estado FROM mesas WHERE numero = %s"
        cursor.execute(consulta, (numeroMesa,))
        resultado = cursor.fetchone()

        if resultado and resultado[0] == 'libre':
            consulta = "UPDATE mesas SET estado = 'ocupada' WHERE numero = %s"
            cursor.execute(consulta, (numeroMesa,))
            cliente.asignarMesa(Mesa(numeroMesa, 0))
            self.clientes.append(cliente)
            print(f"Mesa {numeroMesa} reservada para {cliente.nombre}")
            conexion.commit()
        #for mesa in self.mesas:
        #    if mesa.numero == numeroMesa and mesa.reservar():
        #        cliente.asignarMesa(mesa)
        #        self.clientes.append(cliente)
        #        print(f"Mesa {numeroMesa} reservada para {cliente.nombre}")
            return True
        print(f"Mesa {numeroMesa} no esta disponible.")
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
                itemNombre = input("Ingrese el nombre del item que desea (o 'x' para terminar): ")
                if itemNombre.lower() == 'x':
                    break
                itemEncontrado = next((item for item in self.menu.items if item.nombre.lower() == itemNombre), None)
                if itemEncontrado:
                    itemsSeleccionados.append(itemEncontrado)
                else:
                    print("Item no encontrado. Intente de nuevo.")
            self.gestionarPedido(cliente, itemsSeleccionados)
        else:
            print("Cliente no registrado")

    def mostrarCuenta(self, cliente):
        if cliente in self.clientes:
            cliente.verCuenta()
        else:
            print("Cliente no registrado")

restaurante = Restaurante()
restaurante.añadirMesa(1,4)
restaurante.añadirMesa(2,2)
restaurante.menu.agregarItem('Tacos','Tacos de pastor con todo',10.0)
restaurante.menu.agregarItem('Torta','Torta de pastor con todo',50.0)
restaurante.mostrarMesasDisponibles()

cliente = Cliente('Adrián Rodríguez')
cliente2 = Cliente("Pablo Molina")

restaurante.hacerReservacion(cliente,1)
restaurante.mostrarMesasDisponibles()

restaurante.hacerReservacion(cliente2,2)

restaurante.escogerItemsMenu(cliente)
restaurante.mostrarCuenta(cliente)