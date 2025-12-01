from django.db import models

# NOTA: Agregué este modelo porque aparece en las relaciones de Producto_Mascota
# pero no estaba definido en tu lista de entidades.
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class CategoriaMascota(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.TextField(blank=True, null=True)
    es_comida = models.BooleanField(default=False)
    es_juguete = models.BooleanField(default=False)
    aplica_para_especie = models.CharField(max_length=100, help_text="Ej: Perro, Gato, General")

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría de Mascota"
        verbose_name_plural = "Categorías de Mascotas"


class AnimalTienda(models.Model):
    GENERO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    id_animal = models.AutoField(primary_key=True)
    nombre_animal = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado_salud = models.CharField(max_length=50)
    fecha_ingreso = models.DateField(auto_now_add=True)
    chip_identificacion = models.CharField(max_length=50, unique=True, blank=True, null=True)
    vacunas_aplicadas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_animal} ({self.raza})"

    class Meta:
        verbose_name = "Animal en Tienda"
        verbose_name_plural = "Animales en Tienda"


class ProductoMascota(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    # Relaciones
    categoria = models.ForeignKey(CategoriaMascota, on_delete=models.PROTECT, db_column='id_categoria')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, db_column='id_proveedor')
    
    para_especie = models.CharField(max_length=50)
    tamano_animal = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre_producto

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class ClienteMascota(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    num_mascotas = models.IntegerField(default=0)
    tipo_mascota_preferido = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class EmpleadoTiendaMascota(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    turno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"


class VentaTiendaMascota(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    
    # Relaciones
    cliente = models.ForeignKey(ClienteMascota, on_delete=models.PROTECT, db_column='id_cliente')
    empleado = models.ForeignKey(EmpleadoTiendaMascota, on_delete=models.PROTECT, db_column='id_empleado')
    
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50)
    descuento_aplicado = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    numero_ticket = models.CharField(max_length=50, unique=True)
    estado_venta = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Ticket #{self.numero_ticket}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class DetalleVentaTiendaMascota(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    
    # Relacion principal con Venta
    venta = models.ForeignKey(VentaTiendaMascota, on_delete=models.CASCADE, related_name='detalles', db_column='id_venta')
    
    # Puede ser producto O animal (por eso null=True)
    producto = models.ForeignKey(ProductoMascota, on_delete=models.PROTECT, null=True, blank=True, db_column='id_producto')
    animal_vendido = models.ForeignKey(AnimalTienda, on_delete=models.PROTECT, null=True, blank=True, db_column='id_animal_vendido')
    
    cantidad = models.IntegerField(default=1)
    precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva_aplicado = models.DecimalField(max_digits=5, decimal_places=2, default=0.16)  # Ejemplo IVA

    def save(self, *args, **kwargs):
        # Opcional: Calcular subtotal automaticamente antes de guardar
        self.subtotal = self.cantidad * self.precio_unitario_venta
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Venta {self.venta.id_venta}"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"