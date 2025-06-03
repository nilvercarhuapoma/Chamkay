from django.shortcuts import redirect
from functools import wraps

def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.tipo_usuario in roles_permitidos:
                    return view_func(request, *args, **kwargs)
            return redirect('usuarios:login')
        return _wrapped_view
    return decorador
