from django.core.exceptions import PermissionDenied
from teacher.models import Teacher

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                teacher = Teacher.objects.get(user=request.user)
                user_role = teacher.role.role_type
                if user_role != required_role:
                    raise PermissionDenied  # 🔥 Esto activa el error 403
            except Teacher.DoesNotExist:
                raise PermissionDenied  # 🔥 También aquí
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
