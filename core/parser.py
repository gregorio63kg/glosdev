import re

class CodeParser:
    PATTERNS = {
        'python': [
            r'def\s+(\w+)\s*\(',     # def function_name(
            r'class\s+(\w+):?',     # class ClassName:
        ],
        'javascript': [
            r'function\s+(\w+)\s*\(', # function name()
            r'(?:const|let|var)\s+(\w+)\s*=', # const name =
        ],
        'sql': [
            r'CREATE\s+TABLE\s+(\w+)', # CREATE TABLE name
            r'INSERT\s+INTO\s+(\w+)',  # INSERT INTO name
        ]
    }

    @staticmethod
    def detect(code_text):
        for lang, patterns in CodeParser.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, code_text)
                if match:
                    return {
                        'name': match.group(1),
                        'language': lang
                    }
        return {
            'name': '',
            'language': 'Desconocido'
        }
