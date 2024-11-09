import flet as ft


def main(page: ft.Page):
    # Configuración de la página
    page.title = "Random Forest"
    page.window.width = 500
    page.window.height = 500

    # Texto para mostrar el resultado en la sección de "Solución"
    solucion_text = ft.Text(value="Esta es la vista de Solución. Aquí se mostrarán los resultados.")

    # Definir campos de entrada para la vista de "Ingresar Datos"
    profundidad = ft.TextField(label="Ingrese el diámetro del hueco (in)", value="")
    tipoNPT = ft.TextField(label="Ingrese el paso", value="")
    solucion = ft.TextField(label="Ingrese la operación aplicada", value="")
    tiempoIden = ft.TextField(label="Ingrese el tiempo planeado (hr)", value="")
    tiempoArr = ft.TextField(label="Ingrese el tiempo ejecutado (hr)", value="")

    # Botón para procesar los datos
    b = ft.ElevatedButton(
        text="Ingresar datos",
        on_click=lambda e: button_clicked(e, solucion_text, profundidad, tipoNPT, solucion, tiempoIden, tiempoArr)
    )

    # Contenedor para la vista de "Ingresar Datos"
    ingresar_datos_view = ft.Column([profundidad, tipoNPT, solucion, tiempoIden, tiempoArr, b])

    # Contenedor para la vista de "Solución"
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
    def button_clicked(e, solucion_text, profundidad, tipoNPT, solucion, tiempoIden, tiempoArr):
        try:
            # Convertir entradas a los tipos adecuados
            profundidad_value = float(profundidad.value)
            tipo_npt_value = tipoNPT.value
            tiempo_iden_value = float(tiempoIden.value)
            solucion_value = solucion.value

            # Llamar a la predicción
            tiempo_estimado = modelo_rf.predecir_tiempo(profundidad_value, tipo_npt_value, tiempo_iden_value, solucion_value)

            # Obtener métricas de evaluación del modelo
            métricas = modelo_rf.obtener_métricas()

            # Actualizar el texto en la vista de "Solución"
            solucion_text.value = (
                f"Tiempo estimado de arreglo: {tiempo_estimado:.2f} minutos\n"
                f"R² del modelo: {métricas['R2']:.2f}\n"
                f"MAE: {métricas['MAE']:.2f} horas\n"
                f"RMSE: {métricas['RMSE']:.2f} horas"
            )

            # Cambiar automáticamente a la vista de "Solución" para mostrar el resultado
            change_view(1)

        except ValueError as ve:
            solucion_text.value = f"Error en los datos ingresados: {ve}"
            change_view(1)
        except Exception as e:
            solucion_text.value = f"Ocurrió un error: {e}"
            change_view(1)

        page.update()

    # Agregar el contenedor de vistas a la página
    page.add(view_container)

ft.app(main)