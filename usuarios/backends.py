from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Empresa
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
    from .models import Empresa

class EmpresaBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # En este caso, username será el email o el RUC, según prefieras
        try:
            # Aquí uso email_empresa como ejemplo para login por email
            empresa = Empresa.objects.get(email_empresa=username)
        except Empresa.DoesNotExist:
            return None
        
        # Verificas la contraseña, aquí asumiendo que usas un campo 'clave' (ojo: debería estar hasheado)
        # Mejor si la clave se guarda hasheada como en Usuario, entonces usar check_password de Django
        if empresa.clave == password:  # <-- Esto es inseguro si no está hasheado
            return empresa.usuario  # Retornas el usuario asociado para que django autentique con el user model
        
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
