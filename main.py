import customtkinter as ctk
import sqlite3
from core.database import init_db
from core.parser import CodeParser
from gui.components import SearchBar, ResultCard
from gui.styles import COLORS

class GlosDEVApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("GlosDEV")
        self.geometry("400x120")
        self.attributes('-topmost', True)
        self.overrideredirect(True) 
        
        # Color clave para invisibilidad (solo el fondo desaparece)
        self.transparent_color = "#000001"
        self.config(bg=self.transparent_color) 
        self.attributes("-transparentcolor", self.transparent_color)
        
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Variables para arrastre
        self._offsetx = 0
        self._offsety = 0

        # Inicializar base de datos
        init_db()

        # UI State Variables
        self.current_state = "compact" # compact, list, detail, add

        # Main Layout (Configurado con el color transparente)
        self.main_container = ctk.CTkFrame(self, fg_color=self.transparent_color, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Habilitar arrastre en el contenedor principal
        self.main_container.bind("<Button-1>", self.start_move)
        self.main_container.bind("<B1-Motion>", self.do_move)

        # Search Bar Component
        self.search_bar = SearchBar(
            self.main_container, 
            on_search_callback=self.on_search,
            on_add_callback=self.toggle_add_form,
            on_sync_callback=self.sync_data,
            on_opacity_callback=self.change_opacity
        )
        self.search_bar.pack(fill="x", side="top")

        # Results Container (Scrollable)
        self.results_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", height=0)
        
        # Form Container (Hidden by default)
        self.form_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_light"])

    def on_search(self, query):
        if len(query) > 0:
            self.goto_state("list")
            self.update_results(query)
        else:
            self.goto_state("compact")

    def update_results(self, query):
        # Limpiar resultados previos
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Buscar en DB
        conn = sqlite3.connect('data/glosdev.db')
        cursor = conn.cursor()
        query_str = f'%{query}%'
        cursor.execute("SELECT name, language, description FROM functions WHERE name LIKE ? OR language LIKE ?", (query_str, query_str))
        rows = cursor.fetchall()
        
        for row in rows:
            # Las tarjetas mantienen su fondo para legibilidad, o pueden ser transparentes también
            card = ResultCard(self.results_frame, name=row[0], language=row[1], description=row[2])
            card.pack(fill="x", pady=5)
        
        conn.close()

    def goto_state(self, state):
        if state == "compact":
            self.geometry("400x100")
            self.results_frame.pack_forget()
            self.form_frame.pack_forget()
        elif state == "list":
            self.geometry("400x500")
            self.results_frame.configure(height=400)
            self.results_frame.pack(fill="both", expand=True, pady=(10, 0))
            self.form_frame.pack_forget()
        elif state == "add":
            self.geometry("400x600")
            self.results_frame.pack_forget()
            self.show_add_form()

    def toggle_add_form(self):
        if self.current_state == "add":
            self.goto_state("compact")
            self.current_state = "compact"
        else:
            self.goto_state("add")
            self.current_state = "add"

    def show_add_form(self):
        # Limpiar form previo
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        self.form_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(self.form_frame, text="Nueva Función", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.fn_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre de la función")
        self.fn_name.pack(fill="x", padx=20, pady=5)
        
        self.fn_lang = ctk.CTkEntry(self.form_frame, placeholder_text="Lenguaje")
        self.fn_lang.pack(fill="x", padx=20, pady=5)
        
        self.fn_code = ctk.CTkTextbox(self.form_frame, height=150)
        self.fn_code.pack(fill="x", padx=20, pady=5)
        self.fn_code.bind("<KeyRelease>", self.auto_detect)

        ctk.CTkButton(self.form_frame, text="Guardar", command=self.save_function, fg_color=COLORS["success"]).pack(pady=20)

    def auto_detect(self, event=None):
        code = self.fn_code.get("1.0", "end-1c")
        if len(code) > 10: # Detectar cuando hay suficiente texto
            detected = CodeParser.detect(code)
            if detected['name'] and not self.fn_name.get():
                self.fn_name.delete(0, 'end')
                self.fn_name.insert(0, detected['name'])
            if detected['language'] != 'Desconocido' and not self.fn_lang.get():
                self.fn_lang.delete(0, 'end')
                self.fn_lang.insert(0, detected['language'])

    def save_function(self):
        name = self.fn_name.get()
        lang = self.fn_lang.get()
        code = self.fn_code.get("1.0", "end-1c")
        
        if name and lang:
            conn = sqlite3.connect('data/glosdev.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO functions (name, language, syntax_example) VALUES (?, ?, ?)", (name, lang, code))
            conn.commit()
            conn.close()
            self.goto_state("compact")
            self.current_state = "compact"

    def sync_data(self):
        print("Sincronizando...")

    def change_opacity(self, value):
        self.attributes('-alpha', float(value))

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self._offsetx
        y = self.winfo_y() + event.y - self._offsety
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = GlosDEVApp()
    app.mainloop()
