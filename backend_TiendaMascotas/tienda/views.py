from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
# IMPORTA TODOS LOS MODELOS
from .models import Proveedor, CategoriaMascota, AnimalTienda, ProductoMascota, ClienteMascota, EmpleadoTiendaMascota, VentaTiendaMascota, DetalleVentaTiendaMascota

def index(request):
    return render(request, 'tienda/index.html')

# --- VISTA: VER LISTA ---
def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'tienda/proveedores/ver_proveedores.html', {'proveedores': proveedores})

# --- VISTA: CREAR (MANUAL) ---
def crear_proveedor(request):
    if request.method == 'POST':
        # Capturamos los datos manualmente del HTML por el atributo 'name'
        nombre_empresa = request.POST.get('nombre_empresa')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        # Creamos el objeto en la base de datos
        Proveedor.objects.create(
            nombre_empresa=nombre_empresa,
            contacto=contacto,
            telefono=telefono,
            email=email
        )
        return redirect('ver_proveedores')
    
    return render(request, 'tienda/proveedores/crear_proveedor.html')

# --- VISTA: ACTUALIZAR (MANUAL) ---
def actualizar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)

    if request.method == 'POST':
        # Actualizamos los campos del objeto con los nuevos datos
        proveedor.nombre_empresa = request.POST.get('nombre_empresa')
        proveedor.contacto = request.POST.get('contacto')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.email = request.POST.get('email')
        
        proveedor.save() # Guardamos cambios
        return redirect('ver_proveedores')

    return render(request, 'tienda/proveedores/actualizar_proveedor.html', {'proveedor': proveedor})

# --- VISTA: BORRAR ---
def borrar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
        
    return render(request, 'tienda/proveedores/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# SECCIÓN: CATEGORÍAS DE MASCOTA
# ==========================================

def ver_categorias(request):
    categorias = CategoriaMascota.objects.all()
    return render(request, 'tienda/categorias/ver_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        CategoriaMascota.objects.create(
            nombre_categoria=request.POST.get('nombre_categoria'),
            descripcion_categoria=request.POST.get('descripcion_categoria'),
            es_comida=(request.POST.get('es_comida') == 'on'),   # Lógica checkbox
            es_juguete=(request.POST.get('es_juguete') == 'on'), # Lógica checkbox
            aplica_para_especie=request.POST.get('aplica_para_especie')
        )
        return redirect('ver_categorias')
    return render(request, 'tienda/categorias/crear_categoria.html')

def actualizar_categoria(request, id_categoria):
    categoria = get_object_or_404(CategoriaMascota, id_categoria=id_categoria)
    if request.method == 'POST':
        categoria.nombre_categoria = request.POST.get('nombre_categoria')
        categoria.descripcion_categoria = request.POST.get('descripcion_categoria')
        categoria.es_comida = (request.POST.get('es_comida') == 'on')
        categoria.es_juguete = (request.POST.get('es_juguete') == 'on')
        categoria.aplica_para_especie = request.POST.get('aplica_para_especie')
        categoria.save()
        return redirect('ver_categorias')
    return render(request, 'tienda/categorias/actualizar_categoria.html', {'categoria': categoria})

def borrar_categoria(request, id_categoria):
    categoria = get_object_or_404(CategoriaMascota, id_categoria=id_categoria)
    if request.method == 'POST':
        categoria.delete()
        return redirect('ver_categorias')
    return render(request, 'tienda/categorias/borrar_categoria.html', {'categoria': categoria})


# ==========================================
# SECCIÓN: ANIMALES EN TIENDA
# ==========================================

def ver_animales(request):
    animales = AnimalTienda.objects.all()
    return render(request, 'tienda/animales/ver_animales.html', {'animales': animales})

def crear_animal(request):
    if request.method == 'POST':
        AnimalTienda.objects.create(
            nombre_animal=request.POST.get('nombre_animal'),
            especie=request.POST.get('especie'),
            raza=request.POST.get('raza'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            genero=request.POST.get('genero'),
            precio_venta=request.POST.get('precio_venta'),
            estado_salud=request.POST.get('estado_salud'),
            chip_identificacion=request.POST.get('chip_identificacion'),
            vacunas_aplicadas=request.POST.get('vacunas_aplicadas')
        )
        return redirect('ver_animales')
    return render(request, 'tienda/animales/crear_animal.html')

def actualizar_animal(request, id_animal):
    animal = get_object_or_404(AnimalTienda, id_animal=id_animal)
    if request.method == 'POST':
        animal.nombre_animal = request.POST.get('nombre_animal')
        animal.especie = request.POST.get('especie')
        animal.raza = request.POST.get('raza')
        animal.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        animal.genero = request.POST.get('genero')
        animal.precio_venta = request.POST.get('precio_venta')
        animal.estado_salud = request.POST.get('estado_salud')
        animal.chip_identificacion = request.POST.get('chip_identificacion')
        animal.vacunas_aplicadas = request.POST.get('vacunas_aplicadas')
        animal.save()
        return redirect('ver_animales')
    return render(request, 'tienda/animales/actualizar_animal.html', {'animal': animal})

def borrar_animal(request, id_animal):
    animal = get_object_or_404(AnimalTienda, id_animal=id_animal)
    if request.method == 'POST':
        animal.delete()
        return redirect('ver_animales')
    return render(request, 'tienda/animales/borrar_animal.html', {'animal': animal})

# ==========================================
# SECCIÓN: PRODUCTOS
# ==========================================

def ver_productos(request):
    # Traemos los productos incluyendo sus relaciones para optimizar (select_related)
    productos = ProductoMascota.objects.select_related('categoria', 'proveedor').all()
    return render(request, 'tienda/productos/ver_productos.html', {'productos': productos})

def crear_producto(request):
    # Necesitamos enviar las categorías y proveedores para llenar los <select> del HTML
    categorias = CategoriaMascota.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        # Obtenemos las instancias de las relaciones basadas en el ID enviado por el select
        cat_obj = get_object_or_404(CategoriaMascota, pk=request.POST.get('categoria'))
        prov_obj = get_object_or_404(Proveedor, pk=request.POST.get('proveedor'))

        ProductoMascota.objects.create(
            nombre_producto=request.POST.get('nombre_producto'),
            descripcion=request.POST.get('descripcion'),
            precio_venta=request.POST.get('precio_venta'),
            stock=request.POST.get('stock'),
            categoria=cat_obj,   # Asignamos el objeto categoría
            proveedor=prov_obj,  # Asignamos el objeto proveedor
            para_especie=request.POST.get('para_especie'),
            tamano_animal=request.POST.get('tamano_animal'),
            marca=request.POST.get('marca'),
            fecha_vencimiento=request.POST.get('fecha_vencimiento') or None # Manejo de fecha vacía
        )
        return redirect('ver_productos')

    return render(request, 'tienda/productos/crear_producto.html', {
        'categorias': categorias,
        'proveedores': proveedores
    })

def actualizar_producto(request, id_producto):
    producto = get_object_or_404(ProductoMascota, id_producto=id_producto)
    categorias = CategoriaMascota.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio_venta = request.POST.get('precio_venta')
        producto.stock = request.POST.get('stock')
        
        # Actualizar Relaciones
        producto.categoria = get_object_or_404(CategoriaMascota, pk=request.POST.get('categoria'))
        producto.proveedor = get_object_or_404(Proveedor, pk=request.POST.get('proveedor'))
        
        producto.para_especie = request.POST.get('para_especie')
        producto.tamano_animal = request.POST.get('tamano_animal')
        producto.marca = request.POST.get('marca')
        
        fecha_venc = request.POST.get('fecha_vencimiento')
        if fecha_venc:
            producto.fecha_vencimiento = fecha_venc
            
        producto.save()
        return redirect('ver_productos')

    return render(request, 'tienda/productos/actualizar_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores
    })

def borrar_producto(request, id_producto):
    producto = get_object_or_404(ProductoMascota, id_producto=id_producto)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'tienda/productos/borrar_producto.html', {'producto': producto})


# ==========================================
# SECCIÓN: CLIENTES
# ==========================================

def ver_clientes(request):
    clientes = ClienteMascota.objects.all()
    return render(request, 'tienda/clientes/ver_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        ClienteMascota.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            direccion=request.POST.get('direccion'),
            num_mascotas=request.POST.get('num_mascotas'),
            tipo_mascota_preferido=request.POST.get('tipo_mascota_preferido')
        )
        return redirect('ver_clientes')
    return render(request, 'tienda/clientes/crear_cliente.html')

def actualizar_cliente(request, id_cliente):
    cliente = get_object_or_404(ClienteMascota, id_cliente=id_cliente)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.telefono = request.POST.get('telefono')
        cliente.email = request.POST.get('email')
        cliente.direccion = request.POST.get('direccion')
        cliente.num_mascotas = request.POST.get('num_mascotas')
        cliente.tipo_mascota_preferido = request.POST.get('tipo_mascota_preferido')
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'tienda/clientes/actualizar_cliente.html', {'cliente': cliente})

def borrar_cliente(request, id_cliente):
    cliente = get_object_or_404(ClienteMascota, id_cliente=id_cliente)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'tienda/clientes/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# SECCIÓN: EMPLEADOS
# ==========================================

def ver_empleados(request):
    empleados = EmpleadoTiendaMascota.objects.all()
    return render(request, 'tienda/empleados/ver_empleados.html', {'empleados': empleados})

def crear_empleado(request):
    if request.method == 'POST':
        EmpleadoTiendaMascota.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            cargo=request.POST.get('cargo'),
            dni=request.POST.get('dni'),
            fecha_contratacion=request.POST.get('fecha_contratacion'),
            salario=request.POST.get('salario'),
            turno=request.POST.get('turno'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email')
        )
        return redirect('ver_empleados')
    return render(request, 'tienda/empleados/crear_empleado.html')

def actualizar_empleado(request, id_empleado):
    empleado = get_object_or_404(EmpleadoTiendaMascota, id_empleado=id_empleado)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.cargo = request.POST.get('cargo')
        empleado.dni = request.POST.get('dni')
        empleado.fecha_contratacion = request.POST.get('fecha_contratacion')
        empleado.salario = request.POST.get('salario')
        empleado.turno = request.POST.get('turno')
        empleado.telefono = request.POST.get('telefono')
        empleado.email = request.POST.get('email')
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'tienda/empleados/actualizar_empleado.html', {'empleado': empleado})

def borrar_empleado(request, id_empleado):
    empleado = get_object_or_404(EmpleadoTiendaMascota, id_empleado=id_empleado)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'tienda/empleados/borrar_empleado.html', {'empleado': empleado})


# ==========================================
# SECCIÓN: VENTAS (MAESTRO)
# ==========================================

def ver_ventas(request):
    ventas = VentaTiendaMascota.objects.select_related('cliente', 'empleado').all().order_by('-fecha_venta')
    return render(request, 'tienda/ventas/ver_ventas.html', {'ventas': ventas})

def crear_venta(request):
    clientes = ClienteMascota.objects.all()
    empleados = EmpleadoTiendaMascota.objects.all()
    
    if request.method == 'POST':
        cliente = get_object_or_404(ClienteMascota, pk=request.POST.get('cliente'))
        empleado = get_object_or_404(EmpleadoTiendaMascota, pk=request.POST.get('empleado'))
        
        nueva_venta = VentaTiendaMascota.objects.create(
            cliente=cliente,
            empleado=empleado,
            metodo_pago=request.POST.get('metodo_pago'),
            numero_ticket=request.POST.get('numero_ticket'),
            estado_venta='pendiente',
            total_venta=0  # Se calcula al agregar detalles
        )
        # Redirigir a gestionar la venta para agregar productos
        return redirect('gestionar_venta', id_venta=nueva_venta.id_venta)

    return render(request, 'tienda/ventas/crear_venta.html', {
        'clientes': clientes, 
        'empleados': empleados
    })

def gestionar_venta(request, id_venta):
    """ Vista para ver el detalle de una venta y agregar productos/animales """
    venta = get_object_or_404(VentaTiendaMascota, id_venta=id_venta)
    detalles = DetalleVentaTiendaMascota.objects.filter(venta=venta)
    productos = ProductoMascota.objects.filter(stock__gt=0) # Solo productos con stock
    animales = AnimalTienda.objects.filter(estado_salud='Saludable') # Filtro ejemplo

    # Calcular total actual sumando subtotales
    total_calculado = detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    venta.total_venta = total_calculado
    venta.save()

    if request.method == 'POST':
        # Lógica para agregar un detalle
        tipo_item = request.POST.get('tipo_item') # 'producto' o 'animal'
        id_item = request.POST.get('id_item')
        cantidad = int(request.POST.get('cantidad', 1))
        
        producto_obj = None
        animal_obj = None
        precio_unitario = 0

        if tipo_item == 'producto':
            producto_obj = get_object_or_404(ProductoMascota, pk=id_item)
            precio_unitario = producto_obj.precio_venta
            # (Opcional) Aquí deberías restar stock
            producto_obj.stock -= cantidad
            producto_obj.save()
            
        elif tipo_item == 'animal':
            animal_obj = get_object_or_404(AnimalTienda, pk=id_item)
            precio_unitario = animal_obj.precio_venta
            cantidad = 1 # Animales son únicos generalmente

        # Crear el detalle
        DetalleVentaTiendaMascota.objects.create(
            venta=venta,
            producto=producto_obj,
            animal_vendido=animal_obj,
            cantidad=cantidad,
            precio_unitario_venta=precio_unitario,
            subtotal=cantidad * precio_unitario,
            iva_aplicado=0.16 # IVA Fijo o dinámico
        )
        return redirect('gestionar_venta', id_venta=id_venta)

    return render(request, 'tienda/ventas/gestionar_venta.html', {
        'venta': venta,
        'detalles': detalles,
        'productos': productos,
        'animales': animales
    })

def borrar_venta(request, id_venta):
    venta = get_object_or_404(VentaTiendaMascota, id_venta=id_venta)
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    return render(request, 'tienda/ventas/borrar_venta.html', {'venta': venta})

# --- VISTAS DE DETALLES (Agrega esto en views.py) ---

def detalle_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id_proveedor)
    return render(request, 'tienda/proveedores/detalle_proveedor.html', {'proveedor': proveedor})

def detalle_categoria(request, id_categoria):
    categoria = get_object_or_404(CategoriaMascota, id_categoria=id_categoria)
    return render(request, 'tienda/categorias/detalle_categoria.html', {'categoria': categoria})

def detalle_animal(request, id_animal):
    animal = get_object_or_404(AnimalTienda, id_animal=id_animal)
    return render(request, 'tienda/animales/detalle_animal.html', {'animal': animal})

def detalle_producto(request, id_producto):
    producto = get_object_or_404(ProductoMascota, id_producto=id_producto)
    return render(request, 'tienda/productos/detalle_producto.html', {'producto': producto})

def detalle_cliente(request, id_cliente):
    cliente = get_object_or_404(ClienteMascota, id_cliente=id_cliente)
    return render(request, 'tienda/clientes/detalle_cliente.html', {'cliente': cliente})

def detalle_empleado(request, id_empleado):
    empleado = get_object_or_404(EmpleadoTiendaMascota, id_empleado=id_empleado)
    return render(request, 'tienda/empleados/detalle_empleado.html', {'empleado': empleado})