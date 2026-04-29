from translator import CtoPythonTranslator

def translate_c_to_python(code):
    t = CtoPythonTranslator()
    return t.translate(code)

def translate_with_steps(code):
    t = CtoPythonTranslator()
    return t.translate_with_steps(code)