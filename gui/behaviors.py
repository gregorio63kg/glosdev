import customtkinter as ctk
from gui.styles import COLORS

class DraggableResizableMixin:
    """
    Mixin para dotar a una ventana de capacidades de arrastre sin bordes,
    redimensionamiento horizontal y menú contextual.
    Maneja la lógica de interacción con el mouse y cursores.
    """

    def setup_behaviors(self):
        """Inicializa las variables y bindings necesarios"""
        self._offsetx = 0
        self._offsety = 0
        self._is_dragging = False
        self._is_resizing = False
        self._resize_dir = None
        self._resize_margin = 8  # Píxeles del borde para activar resize
        self._original_alpha = 1.0

        # Configurar bindings generales de la ventana
        self.bind("<Button-1>", self.start_action)
        self.bind("<B1-Motion>", self.do_action)
        self.bind("<ButtonRelease-1>", self.stop_action)
        self.bind("<Motion>", self.check_cursor_area)
        self.bind("<Button-3>", self.show_context_menu)

        # Configurar cursor de arrastre
        self.setup_cursor_feedback()

    def register_draggable_container(self, container):
        """Registra un contenedor para que también responda al arrastre/resize"""
        container.bind("<Button-1>", self.start_action)
        container.bind("<B1-Motion>", self.do_action)
        container.bind("<ButtonRelease-1>", self.stop_action)
        container.bind("<Motion>", self.check_cursor_area)
        container.bind("<Button-3>", self.show_context_menu)

    def register_move_handle(self, handle):
        """Registra un widget específico que solo sirve para mover (no resize)"""
        handle.bind("<Button-1>", self.start_move_only)
        handle.bind("<B1-Motion>", self.do_move)
        handle.bind("<ButtonRelease-1>", self.stop_move)

    def check_cursor_area(self, event):
        """Cambia el cursor y define la dirección si está en los bordes"""
        if self._is_dragging or self._is_resizing:
            return

        width = self.winfo_width()
        x = event.x

        # Detectar bordes laterales para resize
        if x < self._resize_margin:
            self.configure(cursor="sb_h_double_arrow")
            self._resize_dir = "left"
        elif x > width - self._resize_margin:
            self.configure(cursor="sb_h_double_arrow")
            self._resize_dir = "right"
        else:
            self._resize_dir = None
            if not self.is_interactive_widget(event.widget):
                 self.configure(cursor="fleur")
            else:
                 self.configure(cursor="")

    def start_action(self, event):
        """Decide si empezamos a mover o a redimensionar"""
        if self.is_interactive_widget(event.widget) and not self._resize_dir:
            return

        # Resize tiene prioridad si estamos en el borde
        if self._resize_dir:
            self._is_resizing = True
            self._start_x = event.x_root
            self._start_width = self.winfo_width()
            self._start_win_x = self.winfo_x()
            self._original_alpha = self.attributes('-alpha')
            self.attributes('-alpha', 0.8)
        else:
            self.start_move_only(event)

    def start_move_only(self, event):
        """Inicia solo el movimiento (usado por handles o zona central)"""
        if self.is_interactive_widget(event.widget) and not self._is_dragging:
            return

        self._start_x = event.x_root
        self._start_y = event.y_root
        self._win_x = self.winfo_x()
        self._win_y = self.winfo_y()
        
        self._is_dragging = True
        self._original_alpha = self.attributes('-alpha')
        self.attributes('-alpha', 0.8)
        self.configure(cursor="fleur")

    def do_action(self, event):
        """Ejecuta mover o resize según el estado actual"""
        if self._is_resizing:
            self.do_resize(event)
        elif self._is_dragging:
            self.do_move(event)

    def do_resize(self, event):
        dx = event.x_root - self._start_x
        new_width = self._start_width
        new_x = self._start_win_x
        min_width = 300

        if self._resize_dir == "right":
            new_width = self._start_width + dx
        elif self._resize_dir == "left":
            new_width = self._start_width - dx
            if new_width >= min_width:
                new_x = self._start_win_x + dx
        
        if new_width >= min_width:
            current_height = self.winfo_height()
            self.geometry(f"{new_width}x{current_height}+{new_x}+{self.winfo_y()}")

    def do_move(self, event):
        if not self._is_dragging:
            return
        
        dx = event.x_root - self._start_x
        dy = event.y_root - self._start_y
        new_x = self._win_x + dx
        new_y = self._win_y + dy
        self.geometry(f"+{new_x}+{new_y}")

    def stop_action(self, event):
        """Detiene cualquier acción activa"""
        self.stop_move(event)
        if self._is_resizing:
            self._is_resizing = False
            self.attributes('-alpha', self._original_alpha)
            self.check_cursor_area(event)

    def stop_move(self, event):
        if self._is_dragging:
            self._is_dragging = False
            self.attributes('-alpha', self._original_alpha)
            self.check_cursor_area(event)

    def setup_cursor_feedback(self):
        """Configura el feedback visual en widgets propios"""
        self.bind("<Enter>", self.on_enter_draggable)
        self.bind("<Leave>", self.on_leave_draggable)

    def on_enter_draggable(self, event):
        if not self.is_interactive_widget(event.widget):
            self.configure(cursor="fleur")

    def on_leave_draggable(self, event):
        self.configure(cursor="")

    def is_interactive_widget(self, widget):
        """Verifica si un widget es interactivo para no arrastrarlo"""
        interactive_types = (ctk.CTkEntry, ctk.CTkTextbox, ctk.CTkButton, 
                           ctk.CTkSlider, ctk.CTkCheckBox, ctk.CTkScrollableFrame)
        
        if isinstance(widget, interactive_types):
            return True
        
        current = widget
        while current and current != self:
            if isinstance(current, interactive_types):
                return True
            try:
                current = current.master
            except:
                break
        return False

    # --- Menú Contextual y Opciones ---

    def show_context_menu(self, event):
        menu = ctk.CTkToplevel(self)
        menu.overrideredirect(True)
        menu.attributes('-topmost', True)
        menu.geometry(f"+{event.x_root}+{event.y_root}")
        
        menu_frame = ctk.CTkFrame(menu, fg_color=COLORS["bg_light"], corner_radius=8, border_width=1, border_color=COLORS["accent"])
        menu_frame.pack(padx=2, pady=2)
        
        menu_options = [
            ("⚙️ Configuración", self.show_settings),
            ("🎨 Cambiar Tema", self.toggle_theme),
            ("ℹ️ Acerca de...", self.show_about),
            ("separator", None),
            ("❌ Salir", self.quit_app)
        ]
        
        for option_text, command in menu_options:
            if option_text == "separator":
                ctk.CTkFrame(menu_frame, height=1, fg_color=COLORS["text_dim"]).pack(fill="x", padx=10, pady=5)
            else:
                ctk.CTkButton(
                    menu_frame, text=option_text, command=lambda cmd=command, m=menu: self.execute_menu_option(cmd, m),
                    fg_color="transparent", hover_color=COLORS["accent"], anchor="w", height=30
                ).pack(fill="x", padx=5, pady=2)
        
        menu.bind("<FocusOut>", lambda e: menu.destroy())
        menu.focus_set()

    def execute_menu_option(self, command, menu):
        menu.destroy()
        if command: command()

    def show_settings(self):
        w = ctk.CTkToplevel(self)
        w.title("Configuración")
        w.geometry("300x200")
        w.attributes('-topmost', True)
        ctk.CTkLabel(w, text="⚙️ Configuración", font=("Inter", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(w, text="Próximamente...", text_color=COLORS["text_dim"]).pack(pady=10)
        ctk.CTkButton(w, text="Cerrar", command=w.destroy).pack(pady=20)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "Dark" else "dark")

    def show_about(self):
        w = ctk.CTkToplevel(self)
        w.title("Acerca de GlosDEV")
        w.geometry("350x250")
        w.attributes('-topmost', True)
        ctk.CTkLabel(w, text="GlosDEV", font=("Inter", 24, "bold"), text_color=COLORS["accent"]).pack(pady=20)
        ctk.CTkLabel(w, text="Glosario de Funciones de Desarrollo", font=("Inter", 12)).pack(pady=5)
        ctk.CTkLabel(w, text="Versión 1.0", text_color=COLORS["text_dim"]).pack(pady=5)
        ctk.CTkLabel(w, text="\n📚 Tu biblioteca personal de código\n🔍 Busca, guarda y organiza funciones", text_color=COLORS["text_dim"]).pack(pady=10)
        ctk.CTkButton(w, text="Cerrar", command=w.destroy, fg_color=COLORS["accent"]).pack(pady=20)

    def quit_app(self):
        self.quit()
        self.destroy()
