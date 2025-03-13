class Mesa:
    def __init__(self, numero, capacidad):
        self.numero = numero
        self.capacidad = capacidad
        self.estado = 'libre'

    def reservar(self):
        if self.estado == 'libre':
            self.estado = 'ocupada'
            return True
        return False
    
    def liberar(self):
        if self.estado == 'ocupada':
            self.estado = 'libre'
            return True
        return False
    
    def verificarEstado (self):
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

    def eliminarItem(self, nombre):
        self.items = [item for item in self.items if item.nombre != nombre]

    def mostrarMenu(self):
        for item in self.items:
            print(f"{item.nombre}: {item.descripcion} - ${item.precio}")

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

    def asignarMesa(self, mesa):
        self.mesaAsignada = mesa

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

    def mostrarMesasDisponibles(self):
        for mesa in self.mesas:
            if mesa.verificarEstado() == 'Libre':
                print(f"Mesa {mesa.numero} (Capacidad: {mesa.capacidad}) esta disponible.")

    def hacerReservacion (self, cliente, numeroMesa):
        for mesa in self.mesas:
            if mesa.numero == numeroMesa and mesa.reservar():
                cliente.asignarMesa(mesa)
                self.clientes.append(cliente)
                print(f"Mesa {numeroMesa} reservada para {cliente.nombre}")
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

restaurante.hacerReservacion(cliente2,2)

restaurante.escogerItemsMenu(cliente)
restaurante.mostrarCuenta(cliente)