from django.db import models
class PersonaSeleccionada(models.Model):
    habitacion = models.CharField(max_length=10)
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    alimentacion = models.CharField(max_length=100)
    nom_plan = models.CharField(max_length=100)
    fecha_actual = models.DateField()

    def __str__(self):
        return f"{self.cedula} - {self.nombre}"

    class Meta:
        verbose_name_plural = "Personas Seleccionadas"








