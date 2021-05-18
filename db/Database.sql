SET FOREIGN_KEY_CHECKS = 1;
drop database cuentasGranero;
create database cuentasGranero;
use cuentasgranero;

create table cliente(
	id_cliente int auto_increment,
    nombre varchar(255),
    telefono varchar(255),
    primary key (id_cliente)
);


create table venta(
	id_venta int auto_increment,
    id_cliente int,
    concepto varchar(255),
    cantidad int,
    valor_unitario float,
    total float,
    fecha date,
    primary key (id_venta),
    foreign key (id_cliente) references cliente(id_cliente)
);

create table abonoVenta(
	id_abono_venta int auto_increment,
    id_cliente int,
    valor_abono float,
    descripcion varchar(255),
    fecha date,
    primary key (id_abono_venta),
    foreign key (id_cliente) references cliente(id_cliente)
);


create table saldoVentaTotal (
    id_cliente int,
    saldo float,
    primary key (id_cliente)
);

delimiter $$
create trigger saldo_inicial after insert on cliente
for each row
begin
	insert into saldoVentaTotal values (New.id_cliente, 0);
end
$$
delimiter ;

delimiter $$
create trigger nuevo_saldo after insert on venta
for each row 
begin
	update saldoVentaTotal set saldo = saldo + New.total
    where id_cliente = new.id_cliente;
end
$$
delimiter ;

delimiter $$
create trigger actualizar_saldo after insert on abonoVenta
for each row 
begin
	update saldoVentaTotal set saldo = saldo - New.valor_abono 
    where id_cliente = new.id_cliente;
end
$$
delimiter ;

delimiter $$
create trigger saldo_eliminar before delete on venta
for each row
begin
	update saldoVentaTotal set saldo = saldo - old.total where id_cliente = old.id_cliente;
end
$$
delimiter ;

select * from cliente;
select * from saldoVentaTotal;
select * from abonoVenta;

select * from venta;


create table proveedor(
	id_proveedor int auto_increment,
    nombre varchar(255),
    telefono varchar(255),
    primary key (id_proveedor)
);


create table compra(
	id_compra int auto_increment,
    id_proveedor int,
    concepto varchar(255),
    cantidad int,
    valor_unitario float,
    total float,
    fecha date,
    primary key (id_compra),
    foreign key (id_proveedor) references proveedor(id_proveedor)
);

create table abonoCompra(
	id_abono_compra int auto_increment,
    id_proveedor int,
    valor_abono float,
    descripcion varchar(255),
    fecha date,
    primary key (id_abono_compra),
    foreign key (id_proveedor) references compra(id_proveedor)
);

create table saldoCompraTotal (
    id_proveedor int,
    saldo float,
    primary key (id_proveedor)
);

delimiter $$
create trigger saldo_inicial_compra after insert on proveedor
for each row
begin
	insert into saldoCompraTotal values (New.id_proveedor, 0);
end
$$
delimiter ;

delimiter $$
create trigger nuevo_saldo_compra after insert on compra
for each row 
begin
	update saldoCompraTotal set saldo = saldo + New.total
    where id_proveedor = new.id_proveedor;
end
$$
delimiter ;

delimiter $$
create trigger actualizar_saldo_compra after insert on abonoCompra
for each row 
begin
	update saldoCompraTotal set saldo = saldo - New.valor_abono 
    where id_proveedor = new.id_proveedor;
end
$$
delimiter ;

use cuentasgranero;
show tables;


