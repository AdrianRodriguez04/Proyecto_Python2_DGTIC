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

    