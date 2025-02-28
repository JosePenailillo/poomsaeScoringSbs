from django.db import models
from django.contrib.auth.models import User

class Nota(models.Model):
    COMPETIDORES_CHOICES = [
        ("rojo", "Rojo"),
        ("azul", "Azul"),
    ]

    juez = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con un usuario (juez)
    competidor = models.CharField(max_length=10, choices=COMPETIDORES_CHOICES)
    acc = models.FloatField()  # Nota de 'Acc'
    pre = models.FloatField()  # Nota de 'Pre'
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Guarda la fecha en que se creó la nota

    def __str__(self):
        return f"{self.competidor} - Acc: {self.acc}, Pre: {self.pre} (Juez: {self.juez})"
