import flet as ft
from forest import RandomForestModel
#Cambiar si es rezisable
#cambiar el tipo de solución a un combo box con la posibilidad de la muestra


# Inicializar el modelo
modelo_rf = RandomForestModel('datos_npt.csv')

def main(page: ft.Page):
    def button_clicked(e):
        # Intentar convertir las entradas a float y manejar errores
        try:
            profundidad_value = float(profundidad.value)
            tipo_npt_value = next(iter(tipoNPT.selected))  # Obtener el primer valor seleccionado
            tiempo_iden_value = float(tiempoIden.value)
            solucion_value = solucion.value
            tiempo_arr_value = float(tiempoArr.value)  # Valor del tiempo de arreglo

            # Usar el modelo para predecir el tiempo
            tiempo_estimado = modelo_rf.predecir_tiempo(profundidad_value, tipo_npt_value, tiempo_iden_value, solucion_value)
            t.value = f"Tiempo estimado de arreglo: {tiempo_estimado:.2f} minutos"
        except ValueError as ve:
            t.value = f"Error en los datos ingresados: {ve}"
        except Exception as e:
            t.value = f"Ocurrió un error: {e}"

        page.update()

    page.window.width = 500
    page.window.height = 500

    # Texto para mostrar el resultado
    t = ft.Text()

    # Campos de entrada
    profundidad = ft.TextField(label="Ingrese la profundidad (m)", value="")

    tipoNPT = ft.SegmentedButton(
        selected={"Común"},  # Selección predeterminada
        segments=[
            ft.Segment(value="Común", label=ft.Text("NPT Común")),
            ft.Segment(value="No común", label=ft.Text("NPT no común")),
        ],
    )

    tiempoIden = ft.TextField(label="Ingrese el tiempo de identificación del NPT (min)", value="")
    solucion = ft.TextField(label="Ingrese la solución aplicada", value="")
    tiempoArr = ft.TextField(label="Ingrese el tiempo de arreglo del NPT (min)", value="")

    b = ft.ElevatedButton(text="Ingresar datos", on_click=button_clicked)

    # Agregar los componentes a la página
    page.add(profundidad, tipoNPT, tiempoIden, solucion, tiempoArr, b, t)

ft.app(main)
