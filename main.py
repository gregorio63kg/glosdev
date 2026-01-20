import customtkinter as ctk
import sqlite3
from core.database import init_db
from core.parser import CodeParser
from gui.components import SearchBar, ResultCard
from gui.styles import COLORS

# Esta es la aplicación principal, el mero mero.
class GlosDEVApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana (pa' que se vea bien pavito)
        self.title("GlosDEV")
        self.geometry("400x120")
        self.attributes('-topmost', True) # Que esté siempre arriba, sin falta.
        self.overrideredirect(False)      # Por ahora con bordes pa' que no te pierdas.
        
        # Color clave para invisibilidad del fondo (truco de magia)
        self.transparent_color = "#000001"
        self.config(bg=self.transparent_color) 
        self.attributes("-transparentcolor", self.transparent_color)
        
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Variables para poder rodar la ventana a mano
        self._offsetx = 0
        self._offsety = 0

        # Prendemos la base de datos
        init_db()

        # ¿En qué estado anda la app? (Compacta, lista, detalle o cargando)
        self.current_state = "compact" 

        # El contenedor principal donde va todo el corotero
        self.main_container = ctk.CTkFrame(self, fg_color=self.transparent_color, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Le pegamos el evento para poder mover la ventana sin bordes (si hiciera falta)
        self.main_container.bind("<Button-1>", self.start_move)
        self.main_container.bind("<B1-Motion>", self.do_move)

        # El buscador con sus callbacks (la gente que avisa cuando pasa algo)
        self.search_bar = SearchBar(
            self.main_container, 
            on_search_callback=self.on_search,
            on_add_callback=self.toggle_add_form,
            on_sync_callback=self.sync_data,
            on_opacity_callback=self.change_opacity
        )
        self.search_bar.pack(fill="x", side="top")

        # El cuadro donde aparecen los resultados con scroll
        self.results_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", height=0)
        
        # El formulario para meter datos nuevos (empieza escondido)
        self.form_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_light"])

    # Función que se activa cuando escribes en el buscador
    def on_search(self, query):
        if len(query) > 0:
            self.goto_state("list") # Vamos a ver la lista
            self.update_results(query)
        else:
            self.goto_state("compact") # Volvemos a lo chiquitico

    # Aquí es donde ocurre la magia de buscar los bichos en la base de datos
    def update_results(self, query):
        # Primero limpiamos el tarantín para que no se amontone la información vieja
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Nos metemos en la base de datos a ver qué pillamos
        conn = sqlite3.connect('data/glosdev.db')
        cursor = conn.cursor()
        query_str = f'%{query}%'
        # Buscamos por nombre o por lenguaje, a ver qué sale
        cursor.execute("SELECT name, language, description FROM functions WHERE name LIKE ? OR language LIKE ?", (query_str, query_str))
        rows = cursor.fetchall()
        
        for row in rows:
            # Por cada resultado, armamos una tarjetica bien pava
            card = ResultCard(self.results_frame, name=row[0], language=row[1], description=row[2])
            card.pack(fill="x", pady=5)
        
        # Cerramos el boliche para que no se quede la conexión abierta
        conn.close()

    # Esta función mueve la ventana de un estado a otro (la pone flaca o gorda)
    def goto_state(self, state):
        if state == "compact":
            self.geometry("400x120") # El tamaño mínimo pa' que no estorbe
            self.results_frame.pack_forget()
            self.form_frame.pack_forget()
        elif state == "list":
            self.geometry("400x500") # Se expande pa' mostrar la lista de corotos
            self.results_frame.configure(height=400)
            self.results_frame.pack(fill="both", expand=True, pady=(10, 0))
            self.form_frame.pack_forget()
        elif state == "add":
            self.geometry("400x600") # El tamaño máximo pa' meter toda la data
            self.results_frame.pack_forget()
            self.show_add_form()

    # Este es el switch para abrir o cerrar el formulario de carga
    def toggle_add_form(self):
        if self.current_state == "add":
            self.goto_state("compact") # Si estaba abierto, lo cerramos
            self.current_state = "compact"
        else:
            self.goto_state("add")     # Si estaba cerrado, lo abrimos de una
            self.current_state = "add"

    # Aquí montamos todo el aparataje para meter una función nueva
    def show_add_form(self):
        # Limpiamos lo que había antes para resetear el mandado
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        self.form_frame.pack(fill="both", expand=True, pady=10)
        
        # Usamos un scrollview porque son burda de campos y no caben todos
        container = ctk.CTkScrollableFrame(self.form_frame, fg_color="transparent", height=450)
        container.pack(fill="both", expand=True, padx=5)

        ctk.CTkLabel(container, text="Nueva Función", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Los campitos para llenar la información del beta
        self.fn_name = ctk.CTkEntry(container, placeholder_text="Nombre de la función")
        self.fn_name.pack(fill="x", padx=20, pady=5)
        
        self.fn_lang = ctk.CTkEntry(container, placeholder_text="Lenguaje")
        self.fn_lang.pack(fill="x", padx=20, pady=5)

        self.fn_module = ctk.CTkEntry(container, placeholder_text="Librería / Módulo")
        self.fn_module.pack(fill="x", padx=20, pady=5)
        
        self.fn_tags = ctk.CTkEntry(container, placeholder_text="Etiquetas (separadas por coma)")
        self.fn_tags.pack(fill="x", padx=20, pady=5)

        self.fn_desc = ctk.CTkEntry(container, placeholder_text="Descripción breve")
        self.fn_desc.pack(fill="x", padx=20, pady=5)

        # Un campito para el historial de uso, pa' que no se te olvide el beta
        self.fn_history = ctk.CTkTextbox(container, height=60, border_width=1, border_color="#333")
        self.fn_history.insert("1.0", "Historial de uso...")
        self.fn_history.pack(fill="x", padx=20, pady=5)
        
        # El área principal para el código
        self.fn_code = ctk.CTkTextbox(container, height=150)
        self.fn_code.pack(fill="x", padx=20, pady=5)
        # Cada vez que sueltas una tecla, el parser intenta pillar qué lenguaje es
        self.fn_code.bind("<KeyRelease>", self.auto_detect)

        # Checkbox por si la palabra es de las intocables del lenguaje
        self.fn_reserved = ctk.CTkCheckBox(container, text="Es palabra reservada")
        self.fn_reserved.pack(pady=5)

        # El botón final para guardar todo el mandado
        ctk.CTkButton(container, text="Guardar en GlosDEV", command=self.save_function, fg_color=COLORS["success"]).pack(pady=20)

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
        module = self.fn_module.get()
        tags = self.fn_tags.get()
        desc = self.fn_desc.get()
        history = self.fn_history.get("1.0", "end-1c")
        reserved = 1 if self.fn_reserved.get() else 0
        
        if name and lang:
            conn = sqlite3.connect('data/glosdev.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO functions 
                (name, language, syntax_example, library_module, project_tags, description, usage_history, is_reserved) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, lang, code, module, tags, desc, history, reserved))
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
