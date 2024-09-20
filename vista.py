import flet as ft

def main (page: ft.Page):
    #Método para darle acción al botón.
    def button_clicked(e):
        t.value = (f"Los valores ingresados son: '{profundidad.value}','{tipoNPT.value}, '{tiempoIden.value},"
                   f"'{solucion.value}', '{tiempoArr.value}")
        page.update()
    page.window.width = 500
    page.window.height = 500
    t = ft.Text()
    profundidad = ft.TextField(
        label = "Ingrese la profundidad (m)",
        value=""
    )

    def handle_changed(e):
        tipoNPT.value = e.data
        print (tipoNPT)
        print("on_change data: "+ str(e.data))

    tipoNPT = ft.TextField(
        value="",
    )
    page.add(profundidad,
        ft.SegmentedButton(
            on_change=handle_changed,
            selected_icon=ft.Icon(ft.icons.ONETWOTHREE),
            selected = {"NPT común"},
            segments=[
                ft.Segment(
                    value="Común",
                    label=ft.Text("NPT Común"),
                    icon=ft.Icon(ft.icons.FLIGHT),
                ),
                ft.Segment(
                    value="No común",
                    label=ft.Text("NPT no común"),
                    icon=ft.Icon(ft.icons.WARNING),
                )
            ],
        )
    )
    tiempoIden = ft.TextField(
        label="Ingrese el tiempo de identificación del NPT (min)",
        value=""
    )
    solucion = ft.TextField(
        label="Ingrese la solución aplicada",
        value=""
    )
    tiempoArr = ft.TextField(
        label="Ingrese el tiempo de arrelgo del NPT (min)",
        value=""
    )
    b = ft.ElevatedButton(text="Ingresar datos", on_click=button_clicked)
    page.add(tiempoIden, solucion, tiempoArr, b, t)

ft.app(main)