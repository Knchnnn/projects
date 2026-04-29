import re

class CtoPythonTranslator:

    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def translate_line(self, line):
        line = line.strip()

        if not line or line.startswith("#"):
            return ""

        if line.endswith(";"):
            line = line[:-1]

        if "main(" in line:
            return ""

        # FUNCTION
        if "(" in line and ")" in line and any(t in line for t in ["int", "float", "char"]):
            has_brace = "{" in line
            line = re.sub(r'(int|float|char)\s+', '', line)

            name = line[:line.find("(")].strip()
            params = line[line.find("(")+1:line.find(")")]

            result = self.indent() + f"def {name}({params}):"

            if has_brace:
                self.indent_level += 1

            return result

        # ARRAY
        if "[" in line and "]" in line and "{" in line:
            name = line[:line.find("[")].split()[-1]
            values = line[line.find("{")+1:line.find("}")]
            return self.indent() + f"{name} = [{values}]"

        # REMOVE TYPES
        line = re.sub(r'\b(int|float|char)\s+', '', line)

        # FORMAT
        line = re.sub(r'\s*=\s*', ' = ', line)

        # PRINT
        if "printf" in line:
            content = line[line.find("(")+1:line.rfind(")")]
            return self.indent() + f"print({content})"

        # RETURN
        if line.startswith("return"):
            return self.indent() + line

        # IF
        if line.startswith("if"):
            cond = line[line.find("(")+1:line.find(")")]
            result = self.indent() + f"if {cond}:"
            if "{" in line:
                self.indent_level += 1
            return result

        # ELSE
        if line.startswith("else"):
            if "{" in line:
                self.indent_level += 1
            return self.indent() + "else:"

        # WHILE
        if line.startswith("while"):
            cond = line[line.find("(")+1:line.find(")")]
            result = self.indent() + f"while {cond}:"
            if "{" in line:
                self.indent_level += 1
            return result

        # FOR
        if line.startswith("for"):
            content = line[line.find("(")+1:line.find(")")]
            parts = content.split(";")

            if len(parts) == 3:
                init, cond, inc = parts
                var = init.split("=")[0].strip()
                start = init.split("=")[1].strip()
                end = re.split(r"[<>=]+", cond)[1].strip()

                result = self.indent() + f"for {var} in range({start}, {end}):"

                if "{" in line:
                    self.indent_level += 1

                return result

        # BRACES
        if "{" in line:
            self.indent_level += 1
            return ""

        if "}" in line:
            self.indent_level -= 1
            return ""

        return self.indent() + line

    def translate(self, code):
        result = []
        for line in code.split("\n"):
            out = self.translate_line(line)
            if out:
                result.append(out)
        return "\n".join(result)

    # ⭐ STEP VISUALIZATION
    def translate_with_steps(self, code):
        steps = []
        output = []

        for line in code.split("\n"):
            original = line.strip()
            translated = self.translate_line(line)

            if translated:
                output.append(translated)
                steps.append(f"{original}  →  {translated}")

        return "\n".join(output), "\n".join(steps)