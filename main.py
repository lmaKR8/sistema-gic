"""
Acceso al Sistema GIC (Gestor Inteligente de Clientes)
======================================================
"""
from test.paso_1_test import test_paso_1

def mostrar_encabezado():
    """
    Muestra el encabezado del sistema.
    """
    print("\n" + "=" * 60)
    print(" " * 8 + "SISTEMA GIC - GESTOR INTELIGENTE DE CLIENTES")
    print(" " * 23 + "SolutionTech")
    print("=" * 60)


def main(): 
    """
    Coordina la ejecución del sistema mostrando el encabezado y ejecutando las pruebas del Paso 1.
    """
    mostrar_encabezado()
    test_paso_1()
    
    print("=" * 60)
    print(" " * 20 + "FIN DEL PROGRAMA")
    print("=" * 60 + "\n")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
