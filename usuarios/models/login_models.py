from django.db import models
import uuid


class Login(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    token = models.TextField()
    force = models.BooleanField(default=False)

    class Meta:
        db_table = 'usuarios_login'
