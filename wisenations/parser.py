from pyparsing import Word, Suppress, CharsNotIn, alphas, pythonStyleComment
from typing import Final
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
                #return f.read()
        except (FileNotFoundError, OSError):
            pass
        return content.strip()
    def parse(self,
              src: str) -> dict[str, str]:
        text: str = self._source(src)

        variable = Word(alphas+"_")("var")
        expression_content = CharsNotIn("}")("expr")
        l_brace = Suppress("{")
        r_brace = Suppress("}")
        assignment = Suppress("=")
        
        expression = l_brace + expression_content + r_brace
        line_grammar = variable + assignment + expression
        line_grammar.ignore(pythonStyleComment)
        matches = line_grammar.search_string(text)
        
        result: dict[str, str] = {m.var: m.expr.strip() for m in matches}
        return result

if __name__ == "__main__":
    sp = SyntaxParser()
    parsed = sp.parse("samples/sheet1.txt")
    pprint(parsed)