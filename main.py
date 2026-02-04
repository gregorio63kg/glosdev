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
        self.overrideredirect(True)      # Sin bordes pa' que se vea más limpio
        
        # Color clave para invisibilidad del fondo (truco de magia)
        self.transparent_color = "#000001"
        self.config(bg=self.transparent_color) 
        self.attributes("-transparentcolor", self.transparent_color)
        
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Variables para poder rodar la ventana a mano
        self._offsetx = 0
        self._offsety = 0
        self._is_dragging = False  # Para saber si estamos arrastrando
        self._original_alpha = 1.0  # Guardar la opacidad original

        # Prendemos la base de datos
        init_db()

        # ¿En qué estado anda la app? (Compacta, lista, detalle o cargando)
        self.current_state = "compact" 

        # El contenedor principal donde va todo el corotero
        # Restauramos transparent_color para que se vea como quieres
        self.main_container = ctk.CTkFrame(self, fg_color=self.transparent_color, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)

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
        
        # Configurar eventos de arrastre y menú contextual
        self.setup_drag_and_menu()
        
        # Configurar feedback visual del cursor
        self.setup_cursor_feedback()

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

    def setup_drag_and_menu(self):
        """Configura el arrastre de ventana y el menú contextual"""
        # Vincular arrastre a la ventana principal
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<ButtonRelease-1>", self.stop_move)

        # También al contenedor principal porque ahora cubre toda la ventana
        self.main_container.bind("<Button-1>", self.start_move)
        self.main_container.bind("<B1-Motion>", self.do_move)
        self.main_container.bind("<ButtonRelease-1>", self.stop_move)

        # Vincular al nuevo "manubrio" de movimiento en la barra de búsqueda
        self.search_bar.move_handle.bind("<Button-1>", self.start_move)
        self.search_bar.move_handle.bind("<B1-Motion>", self.do_move)
        self.search_bar.move_handle.bind("<ButtonRelease-1>", self.stop_move)
        
        # Vincular menú contextual (clic derecho)
        self.bind("<Button-3>", self.show_context_menu)
        self.main_container.bind("<Button-3>", self.show_context_menu)

    def setup_cursor_feedback(self):
        """Configura el feedback visual del cursor en áreas arrastrables"""
        # Lista de widgets que deben mostrar cursor de arrastre
        draggable_widgets = [self, self.main_container]
        
        for widget in draggable_widgets:
            widget.bind("<Enter>", self.on_enter_draggable)
            widget.bind("<Leave>", self.on_leave_draggable)

    def on_enter_draggable(self, event):
        """Cambia el cursor cuando entra en un área arrastrable"""
        widget = event.widget
        # Solo cambiar cursor si no es un widget interactivo
        if not isinstance(widget, (ctk.CTkEntry, ctk.CTkTextbox, ctk.CTkButton, ctk.CTkSlider, ctk.CTkCheckBox)):
            self.config(cursor="fleur")  # Cursor de mover (cruz con flechas)

    def on_leave_draggable(self, event):
        """Restaura el cursor cuando sale del área arrastrable"""
        self.config(cursor="")

    def show_context_menu(self, event):
        """Muestra el menú contextual con opciones"""
        menu = ctk.CTkToplevel(self)
        menu.overrideredirect(True)
        menu.attributes('-topmost', True)
        
        # Posicionar el menú donde hicieron clic
        menu.geometry(f"+{event.x_root}+{event.y_root}")
        
        # Frame contenedor del menú
        menu_frame = ctk.CTkFrame(menu, fg_color=COLORS["bg_light"], corner_radius=8, border_width=1, border_color=COLORS["accent"])
        menu_frame.pack(padx=2, pady=2)
        
        # Opciones del menú
        menu_options = [
            ("⚙️ Configuración", self.show_settings),
            ("🎨 Cambiar Tema", self.toggle_theme),
            ("ℹ️ Acerca de...", self.show_about),
            ("separator", None),
            ("❌ Salir", self.quit_app)
        ]
        
        for option_text, command in menu_options:
            if option_text == "separator":
                # Separador visual
                sep = ctk.CTkFrame(menu_frame, height=1, fg_color=COLORS["text_dim"])
                sep.pack(fill="x", padx=10, pady=5)
            else:
                btn = ctk.CTkButton(
                    menu_frame,
                    text=option_text,
                    command=lambda cmd=command, m=menu: self.execute_menu_option(cmd, m),
                    fg_color="transparent",
                    hover_color=COLORS["accent"],
                    anchor="w",
                    height=30
                )
                btn.pack(fill="x", padx=5, pady=2)
        
        # Cerrar menú al hacer clic fuera
        menu.bind("<FocusOut>", lambda e: menu.destroy())
        menu.focus_set()

    def execute_menu_option(self, command, menu):
        """Ejecuta una opción del menú y cierra el menú"""
        menu.destroy()
        if command:
            command()

    def show_settings(self):
        """Muestra ventana de configuración"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Configuración")
        settings_window.geometry("300x200")
        settings_window.attributes('-topmost', True)
        
        ctk.CTkLabel(settings_window, text="⚙️ Configuración", font=("Inter", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(settings_window, text="Próximamente...", text_color=COLORS["text_dim"]).pack(pady=10)
        
        ctk.CTkButton(settings_window, text="Cerrar", command=settings_window.destroy).pack(pady=20)

    def toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)

    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_window = ctk.CTkToplevel(self)
        about_window.title("Acerca de GlosDEV")
        about_window.geometry("350x250")
        about_window.attributes('-topmost', True)
        
        ctk.CTkLabel(about_window, text="GlosDEV", font=("Inter", 24, "bold"), text_color=COLORS["accent"]).pack(pady=20)
        ctk.CTkLabel(about_window, text="Glosario de Funciones de Desarrollo", font=("Inter", 12)).pack(pady=5)
        ctk.CTkLabel(about_window, text="Versión 1.0", text_color=COLORS["text_dim"]).pack(pady=5)
        ctk.CTkLabel(about_window, text="\n📚 Tu biblioteca personal de código\n🔍 Busca, guarda y organiza funciones", 
                    text_color=COLORS["text_dim"], justify="center").pack(pady=10)
        
        ctk.CTkButton(about_window, text="Cerrar", command=about_window.destroy, fg_color=COLORS["accent"]).pack(pady=20)

    def quit_app(self):
        """Cierra la aplicación"""
        self.quit()
        self.destroy()

    def is_interactive_widget(self, widget):
        """Verifica si un widget o alguno de sus padres es interactivo"""
        # Tipos de widgets que no deben permitir arrastre
        interactive_types = (ctk.CTkEntry, ctk.CTkTextbox, ctk.CTkButton, 
                           ctk.CTkSlider, ctk.CTkCheckBox, ctk.CTkScrollableFrame)
        
        # Verificar el widget actual
        if isinstance(widget, interactive_types):
            return True
        
        # Verificar los padres hasta llegar a la ventana principal
        current = widget
        while current and current != self:
            if isinstance(current, interactive_types):
                return True
            try:
                current = current.master
            except:
                break
        
        return False

    def start_move(self, event):
        # Solo permitir arrastre si no es un widget interactivo
        if self.is_interactive_widget(event.widget):
            return
        
        # Guardamos la posición inicial del mouse en la pantalla (absoluta)
        self._start_x = event.x_root
        self._start_y = event.y_root
        # Guardamos la posición inicial de la ventana
        self._win_x = self.winfo_x()
        self._win_y = self.winfo_y()
        
        self._is_dragging = True
        
        # Guardar opacidad original y hacer la ventana semi-transparente mientras se arrastra
        self._original_alpha = self.attributes('-alpha')
        self.attributes('-alpha', 0.8)  # Un pelín transparente
        self.config(cursor="fleur")

    def do_move(self, event):
        if not self._is_dragging:
            return
            
        # Calculamos cuánto se ha movido el mouse desde el inicio del clic
        dx = event.x_root - self._start_x
        dy = event.y_root - self._start_y
        
        # Aplicamos ese desplazamiento a la posición inicial de la ventana
        new_x = self._win_x + dx
        new_y = self._win_y + dy
        
        self.geometry(f"+{new_x}+{new_y}")

    def stop_move(self, event):
        """Se llama cuando se suelta el botón del ratón"""
        if self._is_dragging:
            self._is_dragging = False
            # Restaurar la opacidad original
            self.attributes('-alpha', self._original_alpha)
            self.config(cursor="")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = GlosDEVApp()
    app.mainloop()
