# gui/styles.py
# Aquí es donde definimos la pinta de la aplicación para que se vea bien chévere

COLORS = {
    "bg_dark": "#1A1B26",   # Fondo oscuro, como noche en el Ávila
    "bg_light": "#24283B",  # Un pelín más claro pa' resaltar los corotos
    "accent": "#7AA2F7",    # El color que manda, el azulito pavo
    "secondary": "#BB9AF7", # El color de respaldo, moradito fino
    "text": "#C0CAF5",      # El color de las letras pa' que no cansen la vista
    "text_dim": "#565F89",  # Letras opacas pa' lo que no es tan importante
    "success": "#9ECE6A",   # Verdecito cuando todo sale bien
    "warning": "#E0AF68",   # Amarillito cuando hay que estar ojo 'e garza
    "danger": "#F7768E",    # Rojito cuando algo se escaracha
}

FONTS = {
    "title": ("Inter", 18, "bold"), # Letras grandes pa' los títulos
    "body": ("Inter", 13),           # Letras normales pa' echar el cuento
    "code": ("JetBrains Mono", 12),  # Letras de programador de verdad
}

STYLE_CONFIG = {
    "border_width": 1,
    "corner_radius": 5,      # Bordes un pelín redondeados, con estilo
}
