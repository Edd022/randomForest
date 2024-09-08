import flet as fl

def hoja1 (page:fl.Page):
    page.theme_mode = fl.ThemeMode.DARK
    page.window.width = 500
    page.window.height = 500
    texto = fl.TextField(
        label = "Escriba aquí el tamaño de su hoyo",
        value = "",
        border = fl.InputBorder.UNDERLINE
    )
    page.add(texto)
    page.title = 'Pana Shiny Wayú'
    page.update()

fl.app(target = hoja1)

