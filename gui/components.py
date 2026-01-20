import customtkinter as ctk
from gui.styles import COLORS, FONTS

class ResultCard(ctk.CTkFrame):
    def __init__(self, master, name, language, description, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_light"], corner_radius=10, **kwargs)
        
        self.name_label = ctk.CTkLabel(self, text=name, font=("Inter", 14, "bold"), text_color=COLORS["accent"])
        self.name_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        self.lang_label = ctk.CTkLabel(self, text=language, font=("Inter", 10), text_color=COLORS["secondary"])
        self.lang_label.pack(anchor="w", padx=10)
        
        self.desc_label = ctk.CTkLabel(self, text=description, font=("Inter", 11), text_color=COLORS["text_dim"], wraplength=350)
        self.desc_label.pack(anchor="w", padx=10, pady=(0, 5))

class SearchBar(ctk.CTkFrame):
    def __init__(self, master, on_search_callback, on_add_callback, on_sync_callback, on_opacity_callback, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Fila Superior: Búsqueda y Botones
        self.top_row = ctk.CTkFrame(self, fg_color="transparent")
        self.top_row.pack(fill="x")

        self.entry = ctk.CTkEntry(self.top_row, placeholder_text="Buscar...", height=35, corner_radius=20)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<KeyRelease>", lambda e: on_search_callback(self.entry.get()))
        
        self.add_btn = ctk.CTkButton(self.top_row, text="+", width=20, height=20, corner_radius=17, 
                                     command=on_add_callback, fg_color=COLORS["accent"])
        self.add_btn.pack(side="left", padx=2)
        
        self.sync_btn = ctk.CTkButton(self.top_row, text="↻", width=20, height=20, corner_radius=10, 
                                      command=on_sync_callback, fg_color=COLORS["bg_light"])
        self.sync_btn.pack(side="left", padx=2)

        # Fila Inferior: Slider de Transparencia (Minimalista)
        self.opacity_slider = ctk.CTkSlider(self, from_=0.2, to=1.0, height=15, 
                                            command=on_opacity_callback, button_color=COLORS["secondary"],
                                            button_hover_color=COLORS["accent"])
        self.opacity_slider.set(1.0)
        self.opacity_slider.pack(fill="x", pady=(5, 0))
