from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'cuentasgranero'
app.config['MYSQL_PORT'] = 3310
mysql = MySQL(app)

#Settings

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html')

## Section VENTAS

@app.route('/ventas')
def ventas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT v.fecha, c.nombre, v.concepto, v.cantidad, v.valor_unitario, v.total, s.saldo, v.id_venta FROM venta v, cliente c, saldoVenta s WHERE c.id_cliente = v.id_cliente AND s.id_venta = v.id_venta')
    data = cur.fetchall()
    print(data)    
    return render_template('ventas.html', ventas = data)

@app.route('/add_venta')
def add_venta():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
    return render_template('add_venta.html', clientes=data)

@app.route('/ingresar_venta', methods=['POST'])
def ingresar_venta():
    if request.method == 'POST':
        fecha = request.form['fecha']
        cliente = request.form['id_cliente']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        valor_unitario = request.form['valor_unitario']
        costo = request.form['total']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO venta (id_cliente, concepto, cantidad, valor_unitario, total, fecha) VALUES (%s, %s, %s, %s, %s, %s)',(cliente, concepto, cantidad, valor_unitario, costo, fecha))
        mysql.connection.commit()
        return redirect(url_for('ventas'))


##SECTION ABONO VENTAS

@app.route('/abono_ventas/<string:id>')
def abono(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM abonoVenta WHERE id_venta = %s',(id,))
    data = cur.fetchall()
    return render_template('abono.html', abonos = data)

@app.route('/add_abono/<string:id>')
def add_abono(id):
    return render_template('add_abono.html', id_venta = id)

@app.route('/insertar_abono/<string:id>', methods=['POST'])
def insertar_abono(id):
    if request.method == 'POST':
        fecha = request.form['fecha']
        valor_abono = request.form['valor_abono']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO abonoVenta (id_venta, valor_abono, descripcion, fecha) VALUES (%s, %s, %s, %s)',(id, valor_abono, descripcion, fecha))
        mysql.connection.commit()
        return redirect(url_for('ventas'))

##PROVEEDORES
@app.route('/proveedor')
def proveedor():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedor')
    data = cur.fetchall()
    return render_template('proveedor.html', proveedores = data)

@app.route('/add_proveedor', methods=['POST'])
def add_proveedor():
    if request.method == 'POST':
        proveedor = request.form['proveedor']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proveedor (nombre, telefono) VALUES (%s, %s)',(proveedor, telefono))
        mysql.connection.commit()
        flash('Cliente Agregado')
        return redirect(url_for('proveedor'))

##CLIENTES
@app.route('/cliente')
def cliente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
    return render_template('cliente.html', clientes = data)


@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        cliente = request.form['cliente']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cliente (nombre, telefono) VALUES (%s, %s)',(cliente, telefono))
        mysql.connection.commit()
        flash('Cliente Agregado')
        return redirect(url_for('cliente'))


@app.route('/compras')
def compras():
    cur = mysql.connection.cursor()
    cur.execute('SELECT c.fecha, p.nombre, c.concepto, c.cantidad, c.valor_unitario, c.total, s.saldo, c.id_compra FROM compra c, proveedor p, saldoCompra s WHERE p.id_proveedor = c.id_proveedor AND s.id_compra = c.id_compra')
    data = cur.fetchall()
    print(data)    
    return render_template('compras.html', compras = data)

@app.route('/add_compra')
def add_compra():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedor')
    data = cur.fetchall()
    return render_template('add_compra.html', proveedores=data)

@app.route('/ingresar_compra', methods=['POST'])
def ingresar_compra():
    if request.method == 'POST':
        fecha = request.form['fecha']
        proveedor = request.form['id_proveedor']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        valor_unitario = request.form['valor_unitario']
        costo = request.form['total']
        print(fecha)
        print(proveedor)
        print(concepto)
        print(cantidad)
        print(valor_unitario)
        print(costo)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO compra (id_proveedor, concepto, cantidad, valor_unitario, total, fecha) VALUES (%s, %s, %s, %s, %s, %s)',(proveedor, concepto, cantidad, valor_unitario, costo, fecha))
        mysql.connection.commit()
        return redirect(url_for('compras'))

## SECTION ABONOS COMPRAS
@app.route('/abono_compra/<string:id>')
def abono_compra(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM abonoCompra WHERE id_compra = %s',(id,))
    data = cur.fetchall()
    return render_template('abono_compra.html', abonos = data)

@app.route('/add_abono_compra/<string:id>')
def add_abono_compra(id):
    return render_template('add_abono_compra.html', id_compra = id)

@app.route('/insertar_abono_compra/<string:id>', methods=['POST'])
def insertar_abono_compra(id):
    if request.method == 'POST':
        fecha = request.form['fecha']
        valor_abono = request.form['valor_abono']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO abonoCompra (id_compra, valor_abono, descripcion, fecha) VALUES (%s, %s, %s, %s)',(id, valor_abono, descripcion, fecha))
        mysql.connection.commit()
        return redirect(url_for('compras'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)

