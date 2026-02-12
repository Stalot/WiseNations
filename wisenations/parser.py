from pyparsing import Word, Suppress, CharsNotIn, Group, OneOrMore, alphas, pythonStyleComment, ParseException
from .exceptions import SyntaxError
from pprint import pprint

class SyntaxParser:
    def __init__(self):
        pass
    
    def _source(self, src: str) -> str:
        """
        Tries to open and read the
        text of a file if src
        is a file path, otherwise,
        returns src as a normal
        string object.
        """
        content: str = src
        if not isinstance(src, str):
            raise TypeError(f"src must be of type str, not {type(src).__name__}")
        try:
            with open(src,
                      "r",
                      encoding="utf-8") as f:
                content = f.read()
        except (FileNotFoundError, OSError):
            pass
        return content.strip()
    def parse(self,
              src: str) -> dict[str, str]:
        # --- SYNTAX ---
        # To declare a stat and it's
        # mathematical expression:
        # variable_name = { ... }
        # 
        # --- CENSUSES ---
        # [0-88]: brackets with a
        # integer inside.
        
        variable = Word(alphas+"_")
        expression_content = CharsNotIn("}\n")("expr")
        l_brace = Suppress("{")
        r_brace = Suppress("}")
        assignment = Suppress("=")
        
        expression = l_brace + expression_content + r_brace
        line_grammar = Group(variable("var") + assignment + expression)
        top_grammar = OneOrMore(line_grammar)
        top_grammar.ignore(pythonStyleComment)
        
        text = self._source(src)
        try:
            matches = top_grammar.parse_string(text,
                                               parse_all=True)
        except ParseException as e:
            raise SyntaxError(f"Couldn't parse stats sheet. {e}")
        result: dict[str, str] = {m["var"]: m["expr"] for m in matches}
        return result

if __name__ == "__main__":
    sp = SyntaxParser()
    parsed = sp.parse("samples/sheet1.txt")
    pprint(parsed)