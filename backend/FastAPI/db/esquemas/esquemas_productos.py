### Esquema para los productos ###

def esquema_producto(producto) -> dict:
    return {
        "id": str(producto["_id"]), # Convierte el '_id' del producto en una cadena.
        "nombre": producto["nombre"], # Extrae el 'nombre' del producto.
        "precio": producto["precio"], # Extrae el 'precio' del producto.
        "cantidad": producto["cantidad"]
    }  # Extrae el 'precio' del producto.


def esquema_productos(productos) -> list:
    # Itera sobre cada producto en la lista "productos" y aplica la función "esquema_producto()" a cada uno.
    return [esquema_producto(producto) for producto in productos]
