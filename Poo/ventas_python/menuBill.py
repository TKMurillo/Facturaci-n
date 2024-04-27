from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce


path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def list_clients():
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        print("Lista de Clientes:")
        for idx, client in enumerate(clients):
            print(f"{idx + 1}. {client['nombre']} {client['apellido']} - DNI: {client['dni']}")
        return clients

    @staticmethod
    def create():
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Registro de Cliente")
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        gotoxy(5, 4); print("Cedula: ")
        dni = validar.solo_numeros("","Error: Solo números", 12, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        client = json_file.find("dni", dni)

        if client:
            borrarPantalla()  # Limpiar pantalla para mostrar lista completa
            CrudClients.list_clients()  # Mostrar toda la lista de clientes
            gotoxy(35, 4); print(red_color + "Cliente ya existe" + reset_color)  # Mensaje de cliente existente
            return

        gotoxy(2, 6); nombre = input("Nombre :").strip()
        gotoxy(2, 7); apellido = input("\nApellido :").strip()

        new_client = {
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni
        }

        # Guardar nuevo cliente
        clients = json_file.read()
        clients.append(new_client)
        json_file.save(clients)

        gotoxy(35, 9); print(green_color + "Cliente ingresado con éxito" + reset_color)

        # Mostrar lista después de crear
        CrudClients.list_clients()
        time.sleep(2)

    @staticmethod
    def update():
        borrarPantalla()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Actualizar Cliente")
        CrudClients.list_clients()  # Mostrar lista de clientes

        cliente_a_actualizar = int(input("Ingrese el número del cliente a actualizar: ")) - 1
        borrarPantalla()
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        if 0 <= cliente_a_actualizar < len(clients):
            client = clients[cliente_a_actualizar]

            # Solicitar nuevos datos
            gotoxy(2, 4); client['nombre'] = input("Nuevo nombre: ")
            gotoxy(2, 5); client['apellido'] = input("Nuevo apellido: ")
            gotoxy(2, 6); client['dni'] = input("Nuevo DNI: ")

            # Guardar cambios
            json_file.save(clients)
            gotoxy(35, 9); print(green_color + "Cliente actualizado con éxito" + reset_color)

            # Mostrar lista después de actualizar
            CrudClients.list_clients()
        else:
            gotoxy(35, 4); print(red_color + "Índice no válido" + reset_color)
            time.sleep(2)

    @staticmethod
    def delete():
        borrarPantalla()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Eliminar Cliente")

        CrudClients.list_clients()  # Mostrar lista de clientes
        
        cliente_a_eliminar = int(input("Ingrese el número del cliente a eliminar: ")) - 1

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        if 0 <= cliente_a_eliminar < len(clients):
            clients.pop(cliente_a_eliminar)
            json_file.save(clients)
            gotoxy(35, 9); print(green_color + "Cliente eliminado con éxito" + reset_color)

            # Mostrar lista después de eliminar
            CrudClients.list_clients()
        else:
            gotoxy(35, 4); print(red_color + "Índice no válido" + reset_color)
            time.sleep(2)

    @staticmethod
    def consult():
        borrarPantalla()
        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Consulta Cliente")
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        gotoxy(5, 4); print("Cedula:")
        dni = validar.solo_numeros("","Error: Solo números", 12, 4)

        json_file = JsonFile(path + '/archivos/clients.json')
        client = json_file.find("dni", dni)

        if not client:
            gotoxy(35, 4); print(red_color + "Cliente no existe" + reset_color)
            return
        
        client = client[0]
        gotoxy(2, 6); print(f"Nombre: {client['nombre']}")
        gotoxy(2, 7); print(f"\nApellido: {client['apellido']}")
        time.sleep(2)
        
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
        gotoxy(30, 2); print(blue_color + "Registro de Producto")
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        
        gotoxy(2, 6); descripcion = input("Descripción: ").strip()
        gotoxy(2, 7); precio = float(input("Precio: ").strip())
        gotoxy(2, 8); stock = int(validar.solo_numeros("Stock: ","Error: Solo números", 0, 8))
        
        # Mostrar lista de productos antes de crear uno nuevo
        CrudProducts.list_products()
        # Obtener el ID más alto y agregar 1 para el nuevo producto
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()
        # Verifica si la lista de productos está vacía
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

        gotoxy(35, 9); print(green_color + "Producto ingresado con éxito" + reset_color)
        time.sleep(2)

    @staticmethod
    def update():
        borrarPantalla()
        validar = Valida() 
        
        # Mostrar lista de productos antes de actualizar}

        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)  # Comienzo de nueva sección
        gotoxy(30, 2); print(blue_color + "Actualizar Producto")  # Título de la sección

        CrudProducts.list_products()  # Llamar a la función para listar productos
        json_file = JsonFile(path + "/archivos/products.json")
        products = json_file.read()
        product_to_update = int(input("Ingrese el número del producto a actualizar: ")) - 1
        borrarPantalla()
        if 0 <= product_to_update < len(products):
            product = products[product_to_update]
            # Obtener nueva descripción, precio y stock
            gotoxy(2, 4); product["descripcion"] = input("Nueva descripción: ")
            gotoxy(2, 5); product["precio"] = float(input("Nuevo precio: "))
            gotoxy(2, 6); product["stock"] = int(validar.solo_numeros("","Stock: ","Error: Solo números", 15, 6))

            # Guardar los cambios
            json_file.save(products)

            # Imprimir un mensaje por separado al final del proceso
            print("\n")
            gotoxy(35, 9); print(green_color + "Producto actualizado con éxito" + reset_color)  # Mensaje final
            time.sleep(2)
        else:
            gotoxy(35, 4); print(red_color + "Índice no válido" + reset_color)  # Mensaje de error

            time.sleep(2)

    @staticmethod
    def delete():
        borrarPantalla()


        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Eliminar Producto")
        
        # Mostrar lista de productos antes de eliminar
        CrudProducts.list_products()

        json_file = JsonFile(path +"/archivos/products.json")
        products = json_file.read()

        product_to_delete = int(input("Ingrese el número del producto a eliminar: ")) - 1
        if 0 <= product_to_delete < len(products):
            products.pop(product_to_delete)
            json_file.save(products)

            gotoxy(35, 9); print(green_color + "Producto eliminado con éxito" + reset_color)
            time.sleep(2)
        else:
            gotoxy(35, 4); print(red_color + "Índice no válido" + reset_color)
            
    @staticmethod
    def consult():
        borrarPantalla()


        validar = Valida()
        gotoxy(2, 1); print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2); print(blue_color + "Consulta Producto")
        gotoxy(17, 3); print(blue_color + Company.get_business_name())
        gotoxy(5, 4); product_id = int(input("ID Producto: "))


        json_file = JsonFile(path + "/archivos/products.json")
        product = json_file.find("id", product_id)
        
        
        if not product:
            gotoxy(35, 4); print(red_color + "\nProducto no existe" + reset_color)
            time.sleep(2)
            return

        product = product[0]

        # Mostrar detalles del producto
        gotoxy(2, 6); print(f"Descripción: {product['descripcion']}")
        gotoxy(2, 7); print(f"Precio: {product['precio']}")
        gotoxy(2, 8); print(f"Stock: {product['stock']}")

        time.sleep(2)

class CrudSales(ICrud):
    def create():
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("","Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        print("\n")
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
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
            id=int(validar.solo_numeros("","Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("","Error:Solo numeros",49,9+line))
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
    
    def update():
        borrarPantalla()
        validar = Valida()
        
        # Encabezado
        gotoxy(2, 1); print(green_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 34 + "Actualizar Venta" + " " * 35 + "██")
        
        # Pedir ID de factura
        gotoxy(2, 4); invoice_id = input("Ingrese el número de factura a actualizar: ")
        if invoice_id.isdigit():
            invoice_id = int(invoice_id)
            
            # Leer facturas desde el archivo JSON
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice_id)
            
            if not invoices:
                gotoxy(2, 5); print(red_color + "Factura no encontrada." + reset_color)
                return
            
            # Factura a actualizar
            invoice = invoices[0]

            # Mostrar detalles de la factura y pedir datos nuevos
            gotoxy(2, 6); print(f"Cliente actual: {invoice['cliente']}")
            gotoxy(2, 7); new_client = input("Nuevo nombre del cliente (o presione Enter para no cambiar): ")
            if new_client:
                invoice["cliente"] = new_client
            
            # Cambios adicionales según sea necesario
            # Por ejemplo, podrías permitir modificar productos, cantidades, precios, etc.
            
            # Guardar cambios
            json_file.save(invoices)

            gotoxy(2, 8); print(green_color + "Factura actualizada con éxito." + reset_color)
        else:
            gotoxy(2, 5); print(red_color + "ID de factura no válido." + reset_color)

        # Esperar un momento antes de continuar
        time.sleep(2)
    
    def delete():
        borrarPantalla()
    
        # Encabezado
        gotoxy(2, 1); print(green_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 34 + "Eliminar Venta" + " " * 35 + "██")
        
        # Pedir ID de factura para eliminar
        gotoxy(2, 4); invoice_id = input("Ingrese el número de factura a eliminar: ")
        if invoice_id.isdigit():
            invoice_id = int(invoice_id)
            
            # Leer facturas desde el archivo JSON
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice_id)
            
            if not invoices:
                gotoxy(2, 5); print(red_color + "Factura no encontrada." + reset_color)
                return
            
            # Confirmación para eliminar
            gotoxy(2, 6); confirmar = input("¿Está seguro de que desea eliminar esta factura? (s/n): ").lower()
            
            if confirmar == 's':
                # Eliminar factura
                invoices = list(filter(lambda inv: inv["factura"] != invoice_id, json_file.read()))
                json_file.save(invoices)
                
                gotoxy(2, 7); print(green_color + "Factura eliminada con éxito." + reset_color)
            else:
                gotoxy(2, 7); print(yellow_color + "Eliminación cancelada." + reset_color)
        else:
            gotoxy(2, 5); print(red_color + "ID de factura no válido." + reset_color)

        # Esperar un momento antes de continuar
        time.sleep(2)
    
    def consult():
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
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
            if opc1 == "1":
                CrudClients.create()
            elif opc1 == "2":
                CrudClients.update()
            elif opc1 == "3":
                CrudClients.delete()
            elif opc1 == "4":
                CrudClients.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                CrudProducts.create()
            elif opc2 == "2":
                CrudProducts.update()
            elif opc2 == "3":
                CrudProducts.delete()
            elif opc2 == "4":
                CrudProducts.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                CrudSales.create()  # Crear una nueva venta
            elif opc3 == "2":
                CrudSales.consult()  # Consultar ventas existentes
            elif opc3 == "3":
                CrudSales.update()  # Modificar una venta existente
            elif opc3 == "4":
                CrudSales.delete()  # Eliminar una venta existente
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

