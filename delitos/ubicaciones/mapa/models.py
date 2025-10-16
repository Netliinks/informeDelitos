from django.db import models

class Detalle(models.Model):
    id = models.BigAutoField(primary_key=True)  # autoincremental único
    id_orden = models.BigIntegerField(null=True, blank=True)  # puede repetirse
    fecha_registro = models.DateField(null=True, blank=True)
    hora_registro = models.TimeField(null=True, blank=True, db_index=True)
    direccion = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True, db_index=True)
    longitud = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True, db_index=True)
    zona = models.CharField(max_length=20, null=True, blank=True)
    provincia = models.CharField(max_length=100, null=True, blank=True)
    canton = models.CharField(max_length=100, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    circuito = models.CharField(max_length=100, null=True, blank=True)
    subcircuito = models.CharField(max_length=100, null=True, blank=True)
    parroquia = models.CharField(max_length=100, null=True, blank=True)
    tipo_delito = models.TextField(null=True, blank=True)
    subtipo_delito = models.TextField(null=True, blank=True)
    delito_dnpj = models.TextField(null=True, blank=True)
    codigo_penal = models.TextField(null=True, blank=True)
    modalidad = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'detalle'  # coincide con la tabla en PostgreSQL

    def __str__(self):
        return f"ID {self.id} | Orden: {self.id_orden}"