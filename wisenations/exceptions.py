
class EvaluationError(Exception):
    pass

class InvalidExpression(Exception):
    pass

class NotFound(Exception):
    pass

class ParserError(Exception):
    pass

class SyntaxError(ParserError):
    pass