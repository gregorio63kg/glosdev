import re

# Esta clase es el "ojo de garza" que detecta qué código pegaste
class CodeParser:
    # Estos son los patrones para pillar el lenguaje y el nombre
    PATTERNS = {
        'python': [
            r'def\s+(\w+)\s*\(',     # Pilla las funciones def
            r'class\s+(\w+):?',     # Pilla las clases
        ],
        'javascript': [
            r'function\s+(\w+)\s*\(', # Pilla el function de toda la vida
            r'(?:const|let|var)\s+(\w+)\s*=', # Pilla variables que guardan funciones
        ],
        'sql': [
            r'CREATE\s+TABLE\s+(\w+)', # Pilla cuando creas una tabla
            r'INSERT\s+INTO\s+(\w+)',  # Pilla los inserts
        ]
    }

    @staticmethod
    def detect(code_text):
        # Recorremos cada lenguaje a ver si alguno cuadra con el código
        for lang, patterns in CodeParser.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, code_text)
                if match:
                    # Si pillamos algo, mandamos el nombre y el lenguaje de una
                    return {
                        'name': match.group(1),
                        'language': lang
                    }
        # Si no entiende ni pío, mandamos esto
        return {
            'name': '',
            'language': 'Desconocido'
        }
