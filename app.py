"""
Launcher Principal con Interfaz Gráfica
Sistema de Reservas de Canchas Deportivas
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import DatabaseConnection
from ui.main_window import MainWindow


def main():
    """
    Función principal de la aplicación
    """
    try:
        # Inicializar base de datos
        print("Inicializando sistema...")
        db = DatabaseConnection()
        print("✓ Base de datos inicializada")
        
        # Iniciar interfaz gráfica
        print("✓ Iniciando interfaz gráfica...")
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresione Enter para salir...")


if __name__ == "__main__":
    main()