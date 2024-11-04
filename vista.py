#vista para mostrar los resultados: r^2, MAE, RMSE, Tiempo estimado
import flet as ft


def main(page: ft.Page):
    # Configuración de la página
    page.title = "Random Forest"
    page.window.width = 500
    page.window.height = 500

    # Texto para mostrar el resultado
    t = ft.Text()

    # Definir campos de entrada para la vista de "Ingresar Datos"
    profundidad = ft.TextField(label="Ingrese el diámetro del hueco (in)", value="")
    tipoNPT = ft.TextField(label="Ingrese el paso", value="")
    solucion = ft.TextField(label="Ingrese la operación aplicada", value="")
    tiempoIden = ft.TextField(label="Ingrese el tiempo planeado (hr)", value="")
    tiempoArr = ft.TextField(label="Ingrese el tiempo ejecutado (hr)", value="")

    # Botón para procesar los datos
    b = ft.ElevatedButton(text="Ingresar datos",
                          on_click=lambda e: button_clicked(e, t, profundidad, tipoNPT, solucion, tiempoIden,
                                                            tiempoArr))

    # Contenedor para la vista de "Ingresar Datos"
    ingresar_datos_view = ft.Column([profundidad, tipoNPT, solucion, tiempoIden, tiempoArr, b, t])

    # Contenedor para la vista de "Solución" (puedes agregar contenido específico aquí)
    solucion_text = ft.Text(value="Esta es la vista de Solución. Aquí se mostrarán los resultados.")
    #Aquí se deben poner los resultados pai
    solucion_view = ft.Column([solucion_text])

    # Crear contenedor para las vistas y establecer la vista predeterminada
    view_container = ft.Column([ingresar_datos_view])

    # Función para cambiar entre vistas
    def change_view(index):
        view_container.controls.clear()  # Limpiar contenedor de vista
        if index == 0:
            view_container.controls.append(ingresar_datos_view)
        elif index == 1:
            view_container.controls.append(solucion_view)
        page.update()

    # Barra de navegación
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.DATA_EXPLORATION_OUTLINED, label="Ingresar Datos"),
            ft.NavigationBarDestination(icon=ft.icons.SOLAR_POWER_OUTLINED, label="Solución")
        ],
        on_change=lambda e: change_view(e.control.selected_index)  # Cambiar vista al seleccionar opción
    )

    # Función de procesamiento de datos
    def button_clicked(e, t, profundidad, tipoNPT, solucion, tiempoIden, tiempoArr):
        try:
            # Convertir entradas a los tipos adecuados
            profundidad_value = float(profundidad.value)
            tipo_npt_value = tipoNPT.value
            tiempo_iden_value = float(tiempoIden.value)
            solucion_value = solucion.value
            tiempo_arr_value = float(tiempoArr.value)

            # Supongamos que `modelo_rf` es una instancia de RandomForestModel
            tiempo_estimado = modelo_rf.predecir_tiempo(profundidad_value, tipo_npt_value, tiempo_iden_value,
                                                        solucion_value)
            t.value = f"Tiempo estimado de arreglo: {tiempo_estimado:.2f} minutos"
        except ValueError as ve:
            t.value = f"Error en los datos ingresados: {ve}"
        except Exception as e:
            t.value = f"Ocurrió un error: {e}"
        page.update()

    # Agregar el contenedor de vistas a la página
    page.add(view_container)


ft.app(main)
