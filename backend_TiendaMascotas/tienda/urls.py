from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id_proveedor>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/borrar/<int:id_proveedor>/', views.borrar_proveedor, name='borrar_proveedor'),

    path('categorias/', views.ver_categorias, name='ver_categorias'),
    path('categorias/agregar/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id_categoria>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categorias/borrar/<int:id_categoria>/', views.borrar_categoria, name='borrar_categoria'),

    path('animales/', views.ver_animales, name='ver_animales'),
    path('animales/agregar/', views.crear_animal, name='crear_animal'),
    path('animales/editar/<int:id_animal>/', views.actualizar_animal, name='actualizar_animal'),
    path('animales/borrar/<int:id_animal>/', views.borrar_animal, name='borrar_animal'),

    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id_producto>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/borrar/<int:id_producto>/', views.borrar_producto, name='borrar_producto'),

    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id_cliente>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:id_cliente>/', views.borrar_cliente, name='borrar_cliente'),

    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('empleados/agregar/', views.crear_empleado, name='crear_empleado'),
    path('empleados/editar/<int:id_empleado>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:id_empleado>/', views.borrar_empleado, name='borrar_empleado'),

    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),
    path('ventas/gestionar/<int:id_venta>/', views.gestionar_venta, name='gestionar_venta'),
    path('ventas/borrar/<int:id_venta>/', views.borrar_venta, name='borrar_venta'),

    path('proveedores/detalle/<int:id_proveedor>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('categorias/detalle/<int:id_categoria>/', views.detalle_categoria, name='detalle_categoria'),
    path('animales/detalle/<int:id_animal>/', views.detalle_animal, name='detalle_animal'),
    path('productos/detalle/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('clientes/detalle/<int:id_cliente>/', views.detalle_cliente, name='detalle_cliente'),
    path('empleados/detalle/<int:id_empleado>/', views.detalle_empleado, name='detalle_empleado'),
]