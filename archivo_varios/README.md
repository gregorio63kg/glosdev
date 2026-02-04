# GlosDEV

Aplicación de escritorio para gestionar un glosario personal de funciones de programación.

## 🚀 Características

- 🔍 Búsqueda en tiempo real de funciones por nombre o lenguaje
- ➕ Agregar nuevas funciones con descripción, código de ejemplo y etiquetas
- 🤖 Auto-detección de lenguaje al pegar código (Python, JavaScript, SQL)
- 👻 Ventana flotante con transparencia ajustable
- 💾 Base de datos SQLite local

## 📋 Requisitos

- Python 3.14+ (o 3.8+)
- Entorno virtual `.env-glosdev` (ya incluido)

## 🔧 Instalación

Las dependencias ya están instaladas en el entorno virtual. Si necesitas reinstalarlas:

```bash
.\.env-glosdev\Scripts\python.exe -m pip install -r requirements.txt
```

## ▶️ Ejecución

### Opción 1: Script batch (Recomendado)
```bash
run.bat
```

### Opción 2: Comando directo
```bash
.\.env-glosdev\Scripts\python.exe main.py
```

### Opción 3: Activar entorno virtual
```bash
.\.env-glosdev\Scripts\activate
python main.py
```

## 📁 Estructura del Proyecto

```
GlosDev/
├── main.py              # Aplicación principal
├── core/
│   ├── database.py     # Gestión de SQLite
│   ├── parser.py       # Detección de lenguaje
│   └── sync.py         # Sincronización
├── gui/
│   ├── components.py   # Componentes UI
│   └── styles.py       # Estilos y colores
├── data/
│   └── glosdev.db     # Base de datos (se crea automáticamente)
└── requirements.txt    # Dependencias
```

## 🎨 Uso

1. Ejecuta la aplicación con `run.bat`
2. Busca funciones escribiendo en el campo de búsqueda
3. Haz clic en `+` para agregar nuevas funciones
4. Ajusta la transparencia con el slider inferior

## 📝 Notas

- La base de datos se crea automáticamente en `data/glosdev.db`
- La ventana permanece siempre visible (topmost)
- Los comentarios en el código están en español venezolano 🇻🇪
