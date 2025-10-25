from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para flash messages

def get_db_connection():
    """Cria uma nova conexão com o banco para cada requisição"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            database="rack_management"
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar com MySQL: {e}")
        return None

@app.route('/')
def index():
    connection = get_db_connection()
    if not connection:
        flash('Erro ao conectar com o banco de dados', 'error')
        return render_template('index.html', devices=[])
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM devices")
        devices = cursor.fetchall()
        return render_template('index.html', devices=devices)
    except Error as e:
        flash(f'Erro ao carregar dispositivos: {e}', 'error')
        return render_template('index.html', devices=[])
    finally:
        cursor.close()
        connection.close()

@app.route('/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        # Validação básica
        if not all([request.form['device_name'], request.form['device_type'], request.form['ip_address']]):
            flash('Preencha todos os campos obrigatórios', 'error')
            return render_template('add_device.html')
        
        device = {
            'device_name': request.form['device_name'],
            'device_type': request.form['device_type'],
            'ip_address': request.form['ip_address'],
            'vlan': request.form['vlan'],
            'configuration': request.form['configuration'],
            'notes': request.form['notes']
        }
        
        connection = get_db_connection()
        if not connection:
            flash('Erro ao conectar com o banco de dados', 'error')
            return render_template('add_device.html')
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO devices (device_name, device_type, ip_address, vlan, configuration, notes) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (device['device_name'], device['device_type'], device['ip_address'], 
                  device['vlan'], device['configuration'], device['notes']))
            connection.commit()
            flash('Dispositivo adicionado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Error as e:
            connection.rollback()
            flash(f'Erro ao adicionar dispositivo: {e}', 'error')
            return render_template('add_device.html')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('add_device.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    connection = get_db_connection()
    if not connection:
        flash('Erro ao conectar com o banco de dados', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if request.method == 'POST':
            if not all([request.form['device_name'], request.form['device_type'], request.form['ip_address']]):
                flash('Preencha todos os campos obrigatórios', 'error')
                return redirect(url_for('edit_device', id=id))
            
            device = {
                'device_name': request.form['device_name'],
                'device_type': request.form['device_type'],
                'ip_address': request.form['ip_address'],
                'vlan': request.form['vlan'],
                'configuration': request.form['configuration'],
                'notes': request.form['notes']
            }
            
            cursor.execute("""
                UPDATE devices 
                SET device_name = %s, device_type = %s, ip_address = %s, 
                    vlan = %s, configuration = %s, notes = %s 
                WHERE id = %s
            """, (device['device_name'], device['device_type'], device['ip_address'], 
                  device['vlan'], device['configuration'], device['notes'], id))
            connection.commit()
            flash('Dispositivo atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
        
        cursor.execute("SELECT * FROM devices WHERE id = %s", (id,))
        device = cursor.fetchone()
        
        if not device:
            flash('Dispositivo não encontrado', 'error')
            return redirect(url_for('index'))
            
        return render_template('edit_device.html', device=device)
    
    except Error as e:
        flash(f'Erro ao editar dispositivo: {e}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        connection.close()

@app.route('/delete/<int:id>', methods=['POST'])
def delete_device(id):
    connection = get_db_connection()
    if not connection:
        flash('Erro ao conectar com o banco de dados', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM devices WHERE id = %s", (id,))
        connection.commit()
        flash('Dispositivo deletado com sucesso!', 'success')
    except Error as e:
        connection.rollback()
        flash(f'Erro ao deletar dispositivo: {e}', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)