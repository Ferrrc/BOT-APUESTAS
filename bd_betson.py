import sqlite3

#SI POR ALGUNA RAZÓN QUIERES BORRAR LA BASE DE DATOS
#EJECUTA

# Conectar a la base de datos SQLite
conn = sqlite3.connect('resultados.db')
c = conn.cursor()

# Eliminar todos los registros de la tabla 'resultados'
c.execute('DELETE FROM resultados')

# Confirmar los cambios
conn.commit()

print("Todos los registros han sido eliminados.")

# Cerrar la conexión a la base de datos
conn.close()