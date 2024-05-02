from utilities import borrarPantalla, gotoxy

import time

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    #Comprobar solo numero entero
    def solonumero(self,col,fil):
        while True:
            gotoxy(col,fil);valor = input().strip()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print("Error")
                time.sleep(3)
                gotoxy(col,fil);print(" "*40)
        return valor
    
    #Comprobar letra
    def sololetra(self,col,fil):
        while True:
            gotoxy(col,fil);valor=input().strip()
            try:
                if valor.isalpha():
                    break
                else:
                    gotoxy(col,fil);print("No es una cadena")
                    time.sleep(3)
                    gotoxy(col,fil);print(" "*40)
            except:
                gotoxy(col,fil);print("Error")
                time.sleep(3)
                gotoxy(col,fil);print(" "*40)
        return valor
        
    #Comprobar decimal
    def solodecimal(self,col,fil):
        while True:
            gotoxy(col,fil);valor=input().strip()
            try:
                valor = float(valor)
                if valor > 0:
                    break
            except:
                gotoxy(col,fil);print("Error")
                time.sleep(3)
                gotoxy(col,fil);print(" "*40)
        return valor
    
    #Comprobar Cedula
    def cedula(self,col,fil):
        
        while True:
            gotoxy(col,fil);valor = input().strip()
            try:
                if valor.isdigit():
                    if len(valor) == 10:
                        break
                    else:
                        gotoxy(col,fil);print(" "*40)
                        gotoxy(col,fil);print("Error")
                        time.sleep(3)
                        gotoxy(col,fil);print(" "*40)
                else:
                    gotoxy(col,fil);print("No es un cedula valida")
                    time.sleep(3)
                    gotoxy(col,fil);print(" "*40)
            except:
                gotoxy(col,fil);print("Error")
                time.sleep(3)
                gotoxy(col,fil);print(" "*40)
        return valor
    
   


class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)