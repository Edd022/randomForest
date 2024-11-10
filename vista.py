import flet as ft

import forest as RF

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Random Forest"
    page.window.width = 500
    page.window.height = 500

    # Texto para mostrar el resultado en la sección de "Solución"
    solucion_text = ft.Text(value="Para visualizar los resultados ingrese los campos necesarios en ingresar datos.")

    # Definir campos de entrada para la vista de "Ingresar Datos"
    profundidad = ft.TextField(label="Ingrese el diámetro del hueco (in).", value="")
    paso = ft.TextField(label="Ingrese el paso.", value="")
    tiempoIden = ft.TextField(label="Ingrese el tiempo planeado o tiempo de identificación (hr).", value="")


    # Botón para procesar los datos
    b = ft.ElevatedButton(
        text="Ingresar datos",
        on_click=lambda e: button_clicked(e, solucion_text, profundidad, paso, tiempoIden)
    )

    # Contenedor para la vista de "Ingresar Datos"
    ingresar_datos_view = ft.Column([profundidad, paso, tiempoIden, b])

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
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.DATA_EXPLORATION_OUTLINED, label="Ingresar Datos"),
            ft.NavigationBarDestination(icon=ft.icons.SOLAR_POWER_OUTLINED, label="Solución")
        ],
        on_change=lambda e: change_view(e.control.selected_index)  # Cambiar vista al seleccionar opción
    )

    # Función de procesamiento de datos
    def button_clicked(e, solucion_text, profundidad, paso, tiempoIden):
        try:
            # Convertir entradas a los tipos adecuados
            profundidad_value = float(profundidad.value)
            tiempo_iden_value = float(tiempoIden.value)
            paso_value = paso.value

            # Llamar a la predicción
            tiempo_estimado = RF.modelo_rf.predecir_tiempo(profundidad_value, tiempo_iden_value)

            # Obtener métricas de evaluación del modelo
            métricas = RF.modelo_rf.obtener_métricas()
            horas = int(tiempo_estimado)
            minutos = int((tiempo_estimado - horas) * 60)

            # Actualizar el texto en la vista de "Solución"
            solucion_text.value = (
                f"MSE: {métricas['MSE']:.2f} minutos\n"
                f"MAE del modelo: {métricas['MAE']:.2f}\n"
                f"R²: {métricas['R2']:.2f} \n"
                f"RMSE: {métricas['RMSE']:.2f} horas"
                f"Tiempo estimado de arreglo: {horas} hora(s) y {minutos} minutos"
            )

            # Cambiar automáticamente a la vista de "Solución" para mostrar el resultado
            change_view(1)
            navigation_bar.selected_index = 1
            page.update()

        except ValueError as ve:
            solucion_text.value = f"Error en los datos ingresados: {ve}"
            change_view(1)
            navigation_bar.selected_index = 1
            page.update()

        except Exception as e:
            solucion_text.value = f"Ocurrió un error: {e}"
            change_view(1)
            navigation_bar.selected_index = 1
            page.update()

        page.update()

    # Agregar el contenedor de vistas a la página
    page.add(view_container, navigation_bar)

ft.app(main)