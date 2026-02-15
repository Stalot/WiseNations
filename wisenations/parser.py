from pyparsing import Word, Suppress, CharsNotIn, Group, OneOrMore, alphas, pythonStyleComment, ParseException, ParseResults
from .exceptions import SyntaxError
from pprint import pprint

# --- SYNTAX ---
# To declare a stat and it's
# mathematical expression:
# variable_name = { ... }
# 
# --- CENSUSES ---
# [0-88]: brackets with a
# integer inside.

class SyntaxParser:
    def __init__(self):
        pass
    
    def _grammar_rules(self) -> OneOrMore:
        variable = Word(alphas+"_")
        expression_content = CharsNotIn("}\n")("expr")      
        l_brace = Suppress("{")
        r_brace = Suppress("}")
        assignment = Suppress("=")
        
        expression = l_brace + expression_content + r_brace
        line_grammar = Group(variable("var") + assignment + expression)
        top_grammar = OneOrMore(line_grammar)
        top_grammar.ignore(pythonStyleComment)
        return top_grammar
    def parse(self,
              src_type: str,
              src: str) -> dict[str, str]:
        grammar = self._grammar_rules()
        try:
            matches: None | ParseResults = None
            match src_type:
                case "string":
                    matches = grammar.parse_string(src,
                                                   parse_all=True)
                case "file":
                    matches = grammar.parse_file(src,
                                                 parse_all=True)
                case _:
                    raise ValueError(f"'{src_type}' is not a valid src_type")
            result: dict[str, str] = {m["var"]: m["expr"] for m in matches}
            return result
        except ParseException as e:
            raise SyntaxError(f"Couldn't parse stats sheet. {e}")

if __name__ == "__main__":
    sp = SyntaxParser()
    parsed = sp.parse("samples/sheet1.txt")
    pprint(parsed)