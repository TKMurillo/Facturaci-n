from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

import functools

def validar_cedula(func):
    @functools.wraps(func)
    
    def wrapper(*args, **kwargs):
        while True:
            cedula = func(*args, **kwargs)
            if len(cedula) != 10 or not cedula.isdigit():
                gotoxy(2,7);print(" "*50)
                gotoxy(2,8);print("La cédula debe tener 10 dígitos numéricos.")
                time.sleep(2)
                gotoxy(2,8);print(" "*50)
                continue
            
            codigo_provincia = cedula[:2]
            provincias_validas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
                                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                                  "21", "22", "23", "24"]
            if codigo_provincia not in provincias_validas:
                gotoxy(2,7);print(" "*50)
                gotoxy(2,8);print("Código inválido.")
                time.sleep(2)
                gotoxy(2,8);print(" "*50)
                continue
            
            return cedula
    
    return wrapper

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def list_clients():
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        print(purple_color+"Lista de Clientes:"+reset_color)
        for idx, client in enumerate(clients):
            print(f"{idx + 1}. {client['nombre']} {client['apellido']} - DNI: {client['dni']}")
        return clients
    def create(self):
        borrarPantalla()
        validar = Valida()

        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Registro de Cliente")
        gotoxy(17, 4); print(blue_color + Company.get_business_name() + reset_color)
        gotoxy(2, 6); print(green_color + "*" * 90 + reset_color)

        # Usar el DNI validado por el decorador

        def obtener_cedula(x, y):

            gotoxy(2,7);return input("Ingrese el número de cédula: ")
            

        validar_cedula_envuelto = validar_cedula(obtener_cedula)
        dni = validar_cedula_envuelto(2, 7)        
        
        json_file = JsonFile(path + '/archivos/clients.json')
        client = json_file.find("dni", dni)  # Buscar clientes con el mismo DNI

        if client:
            borrarPantalla()  # Limpiar pantalla para mostrar lista completa
            CrudClients.list_clients()  # Mostrar toda la lista de clientes
            gotoxy(35, 25); print(red_color + "Cliente ya existe" + reset_color)  # Mensaje de cliente existente
            time.sleep(5)
            return

        gotoxy(2, 10); print("Nombre: "); nombre = validar.sololetra(10, 10)
        gotoxy(2, 11); print("Apellido: "); apellido = validar.sololetra(13, 11)

        # Continuar con la creación del cliente según el tipo
        while True:
            gotoxy(2, 13); print("Tipo de cliente 1. Regular/ 2.Vip "); type_client = validar.solonumero(40, 13)
            gotoxy(40,13);print(" "*40)
            if type_client == '1':
                while True:
                    gotoxy(2, 14); print("El cliente tiene tarjeta (s/n):"); resp = validar.sololetra(40, 14).lower()
                    if resp == 's':
                        new_client = RegularClient(nombre, apellido, dni, card=True)
                        break
                    elif resp == 'n':
                        new_client = RegularClient(nombre, apellido, dni, card=False)
            
                        break
                    else:
                        print(" "*40)
                        gotoxy(2, 15); print("Valor no válido, ingrese 's' o 'n'")
                        time.sleep(2)
                        print(" "*60)-1
                break
            elif type_client == '2':
                while True:
                    gotoxy(2, 14); print("Ingresa el límite"); resp = validar.solonumero(30, 14)
                    if 10000 <= int(resp) <= 20000:
                        new_client = VipClient(nombre, apellido, dni)
                        new_client.limit = int(resp)
                        break
                    else:
                        new_client = VipClient(nombre, apellido, dni)
                        new_client.limit = 10000
                        break
                break
            else:
                gotoxy(40,13);print(" "*40)
                gotoxy(40,13);print("fuera de rango")
                time.sleep(2)
                gotoxy(40,13);print(" "*40)
        
        # Guardar el nuevo cliente
        clients = json_file.read()
        clients.append(new_client.getJson())
        json_file.save(clients)
        
        # Mostrar la lista de clientes después de crear
        gotoxy(30, 16); CrudClients.list_clients()
        
        gotoxy(35, 35); print(green_color + "Cliente ingresado con éxito" + reset_color)

        # Esperar para permitir que el usuario vea la salida
        time.sleep(4)

    @staticmethod
    def update():
        borrarPantalla()
        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Actualizar Cliente")
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)
        CrudClients.list_clients()  # Mostrar lista de clientes

        while True:
            gotoxy(2,20);print("Ingresa el cliente N. a actualizar: ");valor = validar.solonumero(38,20)
            try:
                cliente_a_actualizar = int(valor)-1
            except:
                gotoxy(2,22);print("Error")
                gotoxy(2,22);print(" "*20)
                continue
            
            json_file = JsonFile(path + '/archivos/clients.json')
            clients = json_file.read()

            if 0 <= cliente_a_actualizar < len(clients):
                client = clients[cliente_a_actualizar]

                # Solicitar nuevos datos
                gotoxy(2, 22);print("Nombre: "); client["nombre"]= nombre = validar.sololetra(10,22)
                gotoxy(2, 24);print("Apellido: "); client["apellido"]=apellido = validar.sololetra(13,24)
                gotoxy(2,26);print("Dni: "); nuevo_dni = validar.cedula(8,26)

                
                dni_existe = any(c["dni"] == nuevo_dni for i, c in enumerate(clients) if i != cliente_a_actualizar)

                if dni_existe:
                    gotoxy(2, 28); print(red_color + "Este DNI ya existe" + reset_color)
                    time.sleep(4)
                    return
                else:
                    client["dni"] = nuevo_dni  # Guardar el DNI solo si no existe
                    # Guardar cambios
                    json_file.save(clients)
                    gotoxy(35, 28); print(green_color + "Cliente actualizado con éxito" + reset_color)
                    
                    # Mostrar lista después de actualizar
                    CrudClients.list_clients()
                    time.sleep(4)
                break
            else:
                gotoxy(35, 4); print(red_color + "Índice no válido" + reset_color)
                time.sleep(4)

    @staticmethod
    def delete():
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Eliminar Cliente")
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)

        gotoxy(30,6);CrudClients.list_clients()  # Mostrar lista de clientes
        
        while True:
            gotoxy(2,20);print("Ingresa el  N. usuario a eliminar: ");valor = validar.solonumero(37,20)
            
            gotoxy(2,20);print(" "*60)
            try:
                cliente_a_eliminar = int(valor)-1
            except:
                gotoxy(2,22);print("Error")
                gotoxy(2,22);print(" "*20)
                continue
                    
            
            json_file = JsonFile(path + '/archivos/clients.json')
            clients = json_file.read()

            if 0 <= cliente_a_eliminar < len(clients):
                clients.pop(cliente_a_eliminar)
                json_file.save(clients)
                gotoxy(35, 25); print(green_color + "Cliente eliminado con éxito" + reset_color)

                # Mostrar lista después de eliminar
                CrudClients.list_clients()
                time.sleep(4)
                break
            else:
                gotoxy(35, 25); print(red_color + "Índice no válido" + reset_color)
                time.sleep(4)
                break

    @staticmethod
    def consult():
        borrarPantalla()
        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Consulta Cliente")
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)
        while True:
            gotoxy(3, 6);print("Ingresa el dni a consultar:"); gotoxy(30,6);dni = input().strip()
            gotoxy(30,6);print(" "*40)
            if dni.isdigit() and len(dni) == 10:
                break
            elif dni == "":
                break
            else:
                gotoxy(2,7);print("error");time.sleep(2);gotoxy(2,7);print(" "*20)
            

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        
        
        if dni:  # Si el usuario ingresa un DNI
            client = json_file.find("dni", dni)
        
            if not client:
                gotoxy(35, 10);print(red_color + "Cliente no encontrado" + reset_color)
                time.sleep(3)
                return
            
            # Mostrar detalles del cliente
            client = client[0]
            gotoxy(2, 8);print(f"Nombre: {client['nombre']} {client['apellido']}")
            gotoxy(2, 9);print(f"DNI   : {client['dni']}")
            if client['valor'] >= 10000:
                gotoxy(2, 10);print(f"Límite de crédito: {client['valor']}")
            else:
                gotoxy(2, 10);print(f"Descuento aplicado: {client['valor'] * 100}%")
        
        else:  # Si el usuario solo presiona "Enter", mostrar todos los clientes
            gotoxy(30,9);print("Lista de Clientes:")
            gotoxy(0,10);print("DNI        Nombre     Apellido     Valor")
            gotoxy(2,11);print((purple_color + "-" * 40) + reset_color)

            for client in clients:
                nombre_completo = f"{client['nombre']} {client['apellido']}"
                print(f"{client['dni']}   {nombre_completo: <20}  {client['valor']}")

            # Calcular estadísticas básicas
            total_valor = reduce(lambda acc, c: acc + c['valor'], clients, 0)
            max_valor = max(clients, key=lambda c: c['valor'])
            min_valor = min(clients, key=lambda c: c['valor'])

            print((purple_color + "-" * 40) + reset_color)
            print(f"Total valor de todos los clientes: {total_valor}")
            print(f"Cliente con mayor valor: {max_valor['nombre']} {max_valor['apellido']} ({max_valor['valor']})")
            print(f"Cliente con menor valor: {min_valor['nombre']} {min_valor['apellido']} ({min_valor['valor']})")
        
        input("Presione una tecla para continuar...")
        time.sleep(4)
        
class CrudProducts(ICrud):
    @staticmethod
    def list_products():
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()  # Leer el archivo actual

        print("Lista de Productos:")
        if not products:  # Verificar si está vacío
            print("No hay productos registrados.")
        else:
            for idx, product in enumerate(products):
                print(f"{idx + 1}. Id: {product['id']} - {product['descripcion']} - Precio: {product['precio']} - Stock: {product['stock']}")

    @staticmethod
    def create():
        borrarPantalla()
        validar = Valida()


        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(purple_color + "Registro de Producto"+reset_color)
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)
        
        
        gotoxy(2, 7);print("Descripcion: "); descripcion  = validar.sololetra(15,7)
        gotoxy(2, 8);print("Precio: "); precio  = validar.solodecimal(10,8)
        gotoxy(2, 9);print("Stock: "); stock = validar.solonumero(9,9)
        
        # Mostrar lista de productos antes de crear uno nuevo
        gotoxy(30,6);CrudProducts.list_products()
        # Obtener el ID más alto y agregar 1 para el nuevo producto
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()
        print("El producto ingresado se añadira a la siguiente lista")
        # Verifica si la lista de productos está vacía
        
        if any(product["descripcion"].lower() == descripcion.lower() for product in products):
            # Producto ya existe, mostrar mensaje de error
            gotoxy(35, 30);print(red_color + "Error: El producto ya existe" + reset_color)
            time.sleep(4)
            return
    
        if not products:
            new_product_id = 1  # Primer ID si la lista está vacía
        else:
            new_product_id = max(product["id"] for product in products) + 1  # Siguiente ID
        

        new_product = {
            "id": new_product_id,  # Usar el ID generado automáticamente
            "descripcion": descripcion,
            "precio": precio,
            "stock": stock
        }

        products.append(new_product)
        json_file.save(products)

        gotoxy(35,32); print(green_color + "Producto ingresado con éxito" + reset_color)
        time.sleep(4)

    @staticmethod
    def update():
        borrarPantalla()
        validar = Valida() 
        
        # Mostrar lista de productos antes de actualizar}

        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)  # Comienzo de nueva sección
        gotoxy(30, 3); print(blue_color + "Actualizar Producto")  # Título de la sección
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)  # Comienzo de nueva sección

        gotoxy(30,6);CrudProducts.list_products()  # Llamar a la función para listar productos
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()
        while True:
            gotoxy(0,20);print("Ingresa la linea del producto a actualizar: ");valor = validar.solonumero(45,20)
    
            try:
                productup = int(valor)-1
            except:
                gotoxy(2,22);print("Error")
                gotoxy(2,22);print(" "*20)
                continue
            
            if 0 <= productup < len(products):
                product = products[productup]
                # Obtener nueva descripción, precio y stock
                
                gotoxy(2, 22);print("Descripcion: "); product["descripcion"]= nombre = validar.sololetra(15,22)
                gotoxy(2, 24);print("Precio "); product["precio"]=apellido = validar.solodecimal(9,24)
                gotoxy(2, 26);print("Stock: "); product["stock"] = dni = validar.solonumero(9,26)

                # Guardar los cambios
                json_file.save(products)

                # Imprimir un mensaje por separado al final del proceso
                gotoxy(35,30); print(green_color + "Producto actualizado con éxito" + reset_color)  # Mensaje final
                time.sleep(4)
                break
            else:
                gotoxy(35, 30); print(red_color + "Índice no válido" + reset_color)  # Mensaje de error
                time.sleep(4)
                gotoxy(35, 30); print(" "*40)
                break

    @staticmethod
    def delete():
        borrarPantalla()
        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Eliminar Producto")
        gotoxy(2, 5); print(green_color + "*" * 90 + reset_color)
        # Mostrar lista de productos antes de eliminar
        gotoxy(30,7);CrudProducts.list_products()

        json_file = JsonFile(path +"/archivos/products.json")
        products = json_file.read()
        while True:
            gotoxy(2,20);print("Ingresa la linea del producto a eliminar: ");valor = validar.solonumero(45,20)
            
            if valor.strip() == "":
                continue
            
            try:
                borrad = int(valor) -1
            except ValueError:
                # Si la entrada no es un número entero, mostrar mensaje de error
                print("Por favor, ingrese un número inválido.")
                continue
                
        
            if borrad == '':
                # Si la entrada es un espacio vacío, continuar solicitando entrada
                continue
            
            if 0 <= borrad < len(products):
                # Índice válido, eliminar el producto
                products.pop(borrad)
                json_file.save(products)

                # Mostrar mensaje de éxito
                gotoxy(35, 25); print(green_color + "Producto eliminado con éxito" + reset_color)
                time.sleep(2)  # Reducir el tiempo de espera
                break  # Salir del bucle
            else:
                # Índice fuera de rango, mostrar mensaje de error
                gotoxy(35, 25); print(red_color + "Índice no válido. Intente nuevamente." + reset_color)
                time.sleep(2)  # Reducir el tiempo de espera
                gotoxy(45,20); print(" "*60)
                gotoxy(35, 25); print(" "*40)
            
    @staticmethod
    def consult():
        borrarPantalla()


        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 3); print(blue_color + "Consulta Producto")
        gotoxy(17, 4); print(blue_color + Company.get_business_name())
        gotoxy(2, 6); print(green_color + "*" * 90 + reset_color)

        while True:
            gotoxy(3, 7);print("Ingresa el ID del producto a consultar:"); gotoxy(42,7);product_id = input().strip()
            gotoxy(42,7);print(" "*40)
            if product_id.isdigit():
                break
            elif product_id == "":
                break
            else:
                gotoxy(2,8);print("error");time.sleep(2);gotoxy(2,8);print(" "*20)
        
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()
        
        if product_id:  # Si el usuario ingresa un ID
            product_id = int(product_id)  # Convertir a entero
            product = json_file.find("id", product_id)  # Buscar el producto por ID
            
            
            if not product:
                gotoxy(35, 10)
                print(red_color + "Producto no encontrado" + reset_color)  # Mensaje si no se encuentra
                time.sleep(3)
                return
            
            # Mostrar detalles del producto
            product = product[0]
            gotoxy(2, 12)
            print(f"Descripción: {product['descripcion']}")
            gotoxy(2, 13)
            print(f"Precio: {product['precio']}")
            gotoxy(2, 14)
            print(f"Stock: {product['stock']}")
    
        else:  # Si el usuario solo presiona "Enter", mostrar todos los productos
            print("Lista de Productos:")
            print("ID     Descripción       Precio     Stock")
            print((purple_color + "-" * 40) + reset_color)
            
            for product in products:
                print(f"{product['id']}   {product['descripcion'][:20]: <20}   {product['precio']}   {product['stock']}")  # Descripción truncada para ajuste
            total_stock = 0
            for product in products:
                try:
                    stock = int(product['stock'])  # Convertir a entero
                    total_stock += stock  # Sumar al total de stock
                except ValueError:  # Capturar errores si el valor no es válido
                    gotoxy(2, 14)
                    print(f"Error en 'stock' para {product['descripcion']}")
            total_price = sum(p['precio'] for p in products)  
            total_productos = len(products)  

            
            print((purple_color + "-" * 40) + reset_color)
            
            print(f"Total de stock: {total_stock}")  # Total de stock
            print(f"Total de precios: {total_price}")  # Precio total
            print(f"Precio promedio: {total_price / total_productos}")
            time.sleep(4)
        input("Presione una tecla para continuar...")

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name()+reset_color)
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.cedula(23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        print("\n")
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,8);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solonumero(15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(2)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solonumero(49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        borrarPantalla()
        # Leer todas las facturas
        json_file = JsonFile(path + "/archivos/invoices.json")
        valida = Valida()
        # Pedir número de factura al usuario
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,3);print(blue_color+"Modificar cliente"+ reset_color)
        gotoxy(2,5);print(green_color+"*"*90+reset_color)
        
        gotoxy(2,7);print("Ingresa la factura a cambiar:");invoice_id = valida.solonumero(35,7)
        
        if not str(invoice_id).isdigit():
            gotoxy(2,9);print("ID de factura no válido.")
            time.sleep(3)
            return
        invoice_id = int(invoice_id)
        # Buscar la factura por número
        factura = json_file.find("factura",invoice_id)

        if not factura:
            gotoxy(2,9);print("Factura no encontrada.")
            time.sleep(3)
            return
        
        def clear_block(start_col, start_fil, num_lines, width=80):
            for i in range(num_lines):
                # Mover el cursor a la posición correcta
                gotoxy(start_col, start_fil + i)
                # Imprimir espacios para limpiar la línea
                print(" " * width)
                
        facturas = json_file.read()
        # Mostrar detalles de la factura
        gotoxy(30,12);print(purple_color+"Detalles de la Factura:"+reset_color)
        # Mostrar detalles de la factura encontrada
        factura = factura[0]
        gotoxy(2,15);print("Detalles de la Factura:")
        gotoxy(2,16);print(f"Factura #: {factura['factura']}")
        gotoxy(2,17);print(f"Fecha   : {factura['Fecha']}")
        gotoxy(2,18);print(f"Cliente : {factura['cliente']}")

        gotoxy(2,19);print("Detalle:")
        
        fil = 20
        for item in factura["detalle"]:
            gotoxy(2,fil);print(f"  Producto: {item['producto']}, Precio: {item['precio']}, Cantidad: {item['cantidad']}")
            fil+=1
        # Menú para elegir qué campo modificar
        while True:
            print("Seleccione el campo a modificar:")
            print("1. Cliente")
            print("2. Productos")
            print("3. Salir")

            while True:
                    opc = input("Opcion: ").strip()
                    try:
                        if opc.isdigit():
                            if opc == "1":
                                break
                            elif opc == "2":
                                break
                            elif opc == "3":
                                break
                        else:
                            print("error valor no valido")
                    except:
                        print("Ocurrio un error")
            if opc == "1":
                # Modificar el nombre del cliente
                
                while True:
                    new_client = input("Nuevo nombre del cliente: ").strip()
                    if new_client:
                        break
                    else:
                        print("error valor no valido")
                    
            
                if new_client:
                    factura["cliente"] = new_client

            elif opc == "2":
                # Modificar detalles de productos
                print("Productos en la factura:")

                for idx, item in enumerate(factura["detalle"]):
                    print(f"{idx + 1}. Producto: {item['producto']}, Precio: {item['precio']}, Cantidad: {item['cantidad']}")
                    fil += 1
                while True:
                    producto_idx = input("Ingresa el numero de producto: ").strip()
                    try:
                        if producto_idx.isdigit():
                            producto_idx = int(producto_idx)
                            break
                        else:
                            print("error valor no valido")
                    except:
                        print("Ocurrio un error")
                            
                producto_idx = (int(producto_idx)-1)
                if 0 <= producto_idx < len(factura["detalle"]):
                    while True:
                        product_id = input("Ingresa el Id del producto: ").strip()
                        try:
                            if product_id.isdigit():
                                break
                            else:
                                print("error valor no valido")
                        except:
                            print("Ocurrio un error")
                    if product_id.isdigit():  # Verificar si es un número
                        product_id = int(product_id)
                        json_file_productos = JsonFile(path+"/archivos/products.json")  # Ruta al archivo de productos
                        productos = json_file_productos.read()
                        producto = next((p for p in productos if p["id"] == product_id), None)
                    
                    
                        if producto:
                            factura["detalle"][producto_idx]["producto"] = producto["descripcion"]
                            factura["detalle"][producto_idx]["precio"] = producto["precio"]
                            while True:
                                nueva_cantidad = input("Ingresa la cantidad: ").strip()
                                try:
                                    if nueva_cantidad.isdigit():
                                        nueva_cantidad = nueva_cantidad
                                        break
                                    else:
                                        print("error valor no valido")
                                except:
                                    print("Ocurrio un error")
                            factura["detalle"][producto_idx]["cantidad"] =int(nueva_cantidad)
                            
                            # Recalcular el subtotal general
                            subtotal = sum(
                                item["precio"] * item["cantidad"]
                                for item in factura["detalle"]
                            )
                            factura["subtotal"] = subtotal
                            time.sleep(3)



            elif opc == "3":
                break
            else:
                print("Opción no válida. Elija entre 1 y 4.")
                time.sleep(3)
        while True:
            print("Desea guardar la informacion (s/n): ");confirm = input().strip()
            if confirm.lower() == "s":
                break
            elif confirm.lower() == "n":
                time.sleep(2)
                return
            else:
                print("error")
            
        if confirm.lower() == "s":
            # Reemplazar la factura modificada en la lista de facturas
            for idx, f in enumerate(facturas):
                if f["factura"] == invoice_id:
                    facturas[idx] = factura  # Reemplazar con la factura modificada
                    break

            json_file.save(facturas)  # Guardar todas las facturas
            gotoxy(30,70);print(green_color+"Factura actualizada con éxito."+reset_color)
            time.sleep(3)
        else:
            gotoxy(30,70);print("Cambios cancelados.")
            time.sleep(3)

        time.sleep(2)


    
    def delete(self):
        borrarPantalla()
    
        # Encabezado
        gotoxy(2, 1); print(green_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 35 + "Eliminar Venta" + " " * 35 + "██")
        gotoxy(2, 5); print(green_color+"█" * 90 + reset_color)
        
        json_file = JsonFile(path + '/archivos/invoices.json')
        facturas = json_file.read()
        
        # Mostrar todas las facturas para ayudar a la selección
        print(purple_color+"Lista de Facturas:"+reset_color)
        print("Factura  Fecha       Cliente")
        print("-" * 30)
        for fac in facturas:
            print(f"{fac['factura']}  {fac['Fecha']}  {fac['cliente']}")

        # Pedir ID de factura para eliminar
        gotoxy(2, 30); invoice_id = input("Ingrese el número de factura a eliminar: ")
        if invoice_id.isdigit():
            invoice_id = int(invoice_id)
            
            # Leer facturas desde el archivo JSON
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice_id)
            
            if not invoices:
                gotoxy(2, 31); print(red_color + "Factura no encontrada." + reset_color)
                return
            
            # Confirmación para eliminar
            gotoxy(2, 34); confirmar = input("¿Está seguro de que desea eliminar esta factura? (s/n): ").lower()
            
            if confirmar == 's':
                # Eliminar factura
                invoices = list(filter(lambda inv: inv["factura"] != invoice_id, json_file.read()))
                json_file.save(invoices)
                
                gotoxy(2, 36); print(green_color + "Factura eliminada con éxito." + reset_color)
            else:
                gotoxy(2, 36); print(yellow_color + "Eliminación cancelada." + reset_color)
        else:
            gotoxy(2, 33); print(red_color + "ID de factura no válido." + reset_color)

        # Esperar un momento antes de continuar
        time.sleep(2)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2, 5); print("█" * 90)
        gotoxy(2,7);invoice= input("Ingrese Factura: "+reset_color)
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            if invoices:
                invoice = invoices[0]
                print("\nDetalles de la Factura:")
                print(f"Factura #: {invoice['factura']}")
                print(f"Fecha   : {invoice['Fecha']}")
                print(f"Cliente : {invoice['cliente']}")

                # Mostrar detalle de productos de manera organizada
                print("Detalle de Productos:")
                for item in invoice["detalle"]:
                    print(f"  Producto: {item['producto']}")
                    print(f"  Precio  : {item['precio']}")
                    print(f"  Cantidad: {item['cantidad']}")
                    print(f"  Total   : {item['precio'] * item['cantidad']}")
                    print((purple_color+"-" * 40) + reset_color) 
            else:
                print("Factura no encontrada.")
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            print("Factura  Fecha        Cliente         Total")
            print((purple_color+"-" * 40) + reset_color)
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))
            print((purple_color+"-" * 40) + reset_color) 
            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"Cliente 'Dayanna Vera': {len(total_client)} facturas")
            print(f"map Facturas:{totales_map}")
            print(f"max Factura:{max_invoice}")
            print(f"min Factura:{min_invoice}")
            print(f"sum Factura:{tot_invoices}")
            print(f"reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            client = CrudClients()
            if opc1 == "1":
                client.create()
            elif opc1 == "2":
                client.update()
            elif opc1 == "3":
                client.delete()
            elif opc1 == "4":
                client.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            product = CrudProducts()
            if opc2 == "1":
                product.create()
            elif opc2 == "2":
                product.update()
            elif opc2 == "3":
                product.delete()
            elif opc2 == "4":
                product.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            venta = CrudSales()
            if opc3 == "1":
                venta.create() #Crear una nueva venta
            elif opc3 == "2":
                venta.consult()  # Consultar ventas existentes
            elif opc3 == "3":
                venta.update()  # Modificar una venta existente
            elif opc3 == "4":
                venta.delete()  # Eliminar una venta existente
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

