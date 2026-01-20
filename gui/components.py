import customtkinter as ctk
from gui.styles import COLORS, FONTS

# La tarjetica donde se ven los resultados bien presentados
class ResultCard(ctk.CTkFrame):
    def __init__(self, master, name, language, description, **kwargs):
        # Creamos el cuadrito con sus bordes
        super().__init__(master, fg_color=COLORS["bg_light"], corner_radius=2, **kwargs)
        
        # El nombre resaltado para que se vea clarito
        self.name_label = ctk.CTkLabel(self, text=name, font=("Inter", 14, "bold"), text_color=COLORS["accent"])
        self.name_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        # El lenguaje en chiquito
        self.lang_label = ctk.CTkLabel(self, text=language, font=("Inter", 10), text_color=COLORS["secondary"])
        self.lang_label.pack(anchor="w", padx=10)
        
        # La descripción por si se te olvida para qué sirve el bicho
        self.desc_label = ctk.CTkLabel(self, text=description, font=("Inter", 11), text_color=COLORS["text_dim"], wraplength=350)
        self.desc_label.pack(anchor="w", padx=10, pady=(0, 5))

# El buscador que está siempre arriba mandando
class SearchBar(ctk.CTkFrame):
    def __init__(self, master, on_search_callback, on_add_callback, on_sync_callback, on_opacity_callback, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Fila Superior: Donde escribes y los botones de acción
        self.top_row = ctk.CTkFrame(self, fg_color="transparent")
        self.top_row.pack(fill="x")

        # El campo donde escribes la búsqueda. Se activa con cada tecla que sueltas.
        self.entry = ctk.CTkEntry(self.top_row, placeholder_text="Buscar...", height=20, corner_radius=36)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<KeyRelease>", lambda e: on_search_callback(self.entry.get()))
        
        # El botón de (+) para meter funciones nuevas al tarantín
        self.add_btn = ctk.CTkButton(self.top_row, text="+", width=20, height=20, corner_radius=10, 
                                     command=on_add_callback, fg_color=COLORS["accent"])
        self.add_btn.pack(side="left", padx=2)
        
        # El botón de actualizar (el refresco)
        self.sync_btn = ctk.CTkButton(self.top_row, text="↻", width=20, height=20, corner_radius=10, 
                                      command=on_sync_callback, fg_color=COLORS["bg_light"])
        self.sync_btn.pack(side="left", padx=2)

        # La barrita para poner la ventana transparente por si estorba
        self.opacity_slider = ctk.CTkSlider(self, from_=0.2, to=1.0, height=1, 
                                            command=on_opacity_callback, button_color=COLORS["secondary"],
                                            button_hover_color=COLORS["accent"])
        self.opacity_slider.set(1.0)
        self.opacity_slider.pack(fill="x", pady=(5, 0))
