from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Perfil  # Importamos el modelo para la foto

# --- 1. Registro de Usuario ---
@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not password or not email:
                 return JsonResponse({'error': 'Faltan datos'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'status': 'ok', 'message': 'Usuario creado'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Solo POST'}, status=405)

# --- 2. Iniciar Sesión ---
@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Faltan datos'}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'ok', 'username': user.username})
            else:
                return JsonResponse({'error': 'Credenciales incorrectas'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    return JsonResponse({'error': 'Solo POST'}, status=405)

# --- 3. Crear Pedido (Simulado) ---
@csrf_exempt
def crear_pedido(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'ok', 'pedido_id': 12345})
    return JsonResponse({'error': 'Solo POST'}, status=405)

# --- 4. Actualizar Perfil (MODIFICADA PARA ARREGLAR EL ERROR 302) ---
@csrf_exempt
# @login_required  <-- ¡IMPORTANTE! COMENTAMOS O QUITAMOS ESTA LÍNEA
def actualizar_perfil(request):
    if request.method == 'POST':
        
        # 1. Recuperamos el nombre de usuario del formulario
        nombre_usuario = request.POST.get('username')
        
        # Si no escribiste el usuario, no sabemos a quién subirle la foto
        if not nombre_usuario:
            return JsonResponse({'error': 'Por seguridad, escribe tu nombre de usuario para confirmar.'}, status=400)

        try:
            # 2. Buscamos al usuario manualmente
            user = User.objects.get(username=nombre_usuario)
            
            # Buscamos o creamos su perfil
            perfil, created = Perfil.objects.get_or_create(usuario=user)

            # 3. Guardamos los datos
            nuevo_email = request.POST.get('email')
            nueva_imagen = request.FILES.get('imagen')

            if nuevo_email:
                user.email = nuevo_email
                user.save()

            if nueva_imagen:
                perfil.imagen = nueva_imagen
                perfil.save()

            # Preparamos la URL
            imagen_url = ""
            if perfil.imagen:
                imagen_url = "http://127.0.0.1:8000" + perfil.imagen.url

            return JsonResponse({
                'status': 'ok', 
                'message': 'Perfil actualizado',
                'username': user.username,
                'imagen_url': imagen_url
            })
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado. Revisa que el nombre esté bien escrito.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Solo POST'}, status=405)

# --- 5. Cambiar Contraseña ---
@csrf_exempt
@login_required
def cambiar_password(request):
    if request.method == 'POST':
        user = request.user
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not user.check_password(old_password):
                return JsonResponse({'error': 'Contraseña actual incorrecta'}, status=401)
            
            user.set_password(new_password)
            user.save()
            login(request, user) # Mantiene la sesión activa
            
            return JsonResponse({'status': 'ok', 'message': 'Contraseña cambiada'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Solo POST'}, status=405)
from django.shortcuts import render

# ... (tus otras funciones) ...

def pagina_inicio(request):
    return render(request, 'OpticaReyes.html')