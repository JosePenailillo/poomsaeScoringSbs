from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Nota
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # Asegura que el usuario esté autenticado
from django.contrib.auth import logout
from django.contrib import messages

@login_required  # Restringe la vista a usuarios autenticados
def evaluar_view(request):
    """Renderiza la página para ingresar evaluaciones"""
    return render(request, "scoring/evaluar.html")

@login_required  # Restringe la vista a usuarios autenticados
def ver_notas(request):
    """Renderiza la página para ver las notas en tiempo real"""
    return render(request, "scoring/ver_notas.html")

@login_required  # Restringe la vista a usuarios autenticados
def ver_notas3_1(request):
    """Renderiza la página para ver las notas en tiempo real"""
    return render(request, "scoring/ver_notas_3_1.html")

@login_required  # Restringe la vista a usuarios autenticados
def ver_notas3_2(request):
    """Renderiza la página para ver las notas en tiempo real"""
    return render(request, "scoring/ver_notas_3_2.html")

@csrf_exempt
@login_required  # Restringe la vista a usuarios autenticados
def evaluar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            red_acc = data["red"]["acc"]
            red_pre = data["red"]["pre"]
            blue_acc = data["blue"]["acc"]
            blue_pre = data["blue"]["pre"]

            # Obtener al juez con el nombre de usuario 'juez1'
            try:
                 juez = request.user  # Obtener el usuario autenticado
            except User.DoesNotExist:
                return JsonResponse({"error": "El usuario no existe"}, status=400)

            # Crear una instancia de Nota para el competidor rojo
            nota_rojo = Nota(
                juez=juez,
                competidor="rojo",
                acc=red_acc,
                pre=red_pre
            )
            # Guardar la instancia en la base de datos
            nota_rojo.save()

            # Crear una instancia de Nota para el competidor azul
            nota_azul = Nota(
                juez=juez,
                competidor="azul",
                acc=blue_acc,
                pre=blue_pre
            )
            # Guardar la instancia en la base de datos
            nota_azul.save()

            # Enviar datos a través de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "evaluaciones",  # Nombre del grupo de WebSocket
                {
                    "type": "send_evaluation",
                    "message": {
                        "juez": juez.username,
                        "red": {
                            "acc": red_acc,
                            "pre": red_pre
                        },
                        "blue": {
                            "acc": blue_acc,
                            "pre": blue_pre
                        }
                    }
                }
            )

            return JsonResponse({"message": "Notas recibidas con éxito"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
@login_required  # Restringe la vista a usuarios autenticados
def enviar_notas(request):
    print(request.method)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            red_acc = data["red"]["acc"]
            red_pre = data["red"]["pre"]
            blue_acc = data["blue"]["acc"]
            blue_pre = data["blue"]["pre"]

            juez = request.user  # Obtener el usuario autenticado

            if not juez:
                return JsonResponse({"error": "No se encontró un juez válido"}, status=400)

            # Crear notas asociadas al juez
            Nota.objects.create(juez=juez, competidor="rojo", acc=red_acc, pre=red_pre)
            Nota.objects.create(juez=juez, competidor="azul", acc=blue_acc, pre=blue_pre)

            return JsonResponse({"message": "Notas guardadas exitosamente"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def obtener_notas(request):
    # Simulación de obtención de datos, ajusta según tu modelo real
    try:
        # Obtener las notas más recientes para el competidor "rojo"
        notas_rojo = Nota.objects.filter(competidor="rojo").latest('id')
        # Obtener las notas más recientes para el competidor "azul"
        notas_azul = Nota.objects.filter(competidor="azul").latest('id')

        # Preparar los datos para la respuesta JSON
        data = {
            "red": {
                "acc": notas_rojo.acc,
                "pre": notas_rojo.pre
            },
            "blue": {
                "acc": notas_azul.acc,
                "pre": notas_azul.pre
            }
        }

        # Devolver los datos en formato JSON
        return JsonResponse(data)

    except Nota.DoesNotExist:
        # Manejar el caso en que no haya notas registradas
        return JsonResponse({"error": "No hay notas registradas"}, status=404)
    except Exception as e:
        # Manejar cualquier otro error
        return JsonResponse({"error": str(e)}, status=500)
    

def custom_logout(request):
    logout(request)  # Cierra la sesión
    messages.success(request, "Has cerrado sesión exitosamente.")  # Mensaje de éxito
    return redirect('login')  # Redirige al login