"""Recursive-descent parser for ANVI Part 5."""
from lexer import lex
from ast_nodes import (ProgramNode, NumberNode, VariableNode, BooleanNode, StringNode,
 UnaryOpNode, BinaryOpNode, AssignmentNode, PrintNode, ExpressionStatementNode,
 BlockNode, IfNode, WhileNode, FunctionDefNode, FunctionCallNode, ReturnNode)
class ParserError(Exception):
    def __init__(self,message,token=None):
        if token is not None: message=f"Parser error at line {token.line}, column {token.column}: {message} (found {token.type}"+(f", value={token.value!r}" if token.value else "")+")"
        super().__init__(message); self.token=token
class Parser:
    def __init__(self,tokens): self.tokens,self.current=tokens,0
    def peek(self): return self.tokens[self.current]
    def is_at_end(self): return self.peek().type=="EOF"
    def advance(self):
        token=self.peek()
        if not self.is_at_end(): self.current+=1
        return token
    def check(self,*types): return self.peek().type in types
    def match(self,*types): return self.advance() if self.check(*types) else None
    def consume(self,typ,message):
        if self.check(typ): return self.advance()
        raise ParserError(message,self.peek())
    def parse(self):
        statements=[]
        while not self.is_at_end(): statements.append(self.parse_statement())
        return ProgramNode(statements)
    def parse_statement(self):
        if self.check("FUNC"): return self.parse_function()
        if self.check("RETURN"): return self.parse_return()
        if self.check("LET"): return self.parse_assignment(True)
        if self.check("ID") and self.current+1<len(self.tokens) and self.tokens[self.current+1].type=="ASSIGN": return self.parse_assignment(False)
        if self.check("DISPLAY"): return self.parse_print()
        if self.check("IF"): return self.parse_if()
        if self.check("WLOOP"): return self.parse_while()
        if self.check("LBRACE"): return self.parse_block()
        if self.check("SEMICOLON"): raise ParserError("empty statements are not allowed",self.peek())
        expr=self.parse_expression()
        if not self.is_at_end(): self.consume("SEMICOLON","expected ';' after expression")
        return ExpressionStatementNode(expr)
    def parse_function(self):
        self.consume("FUNC","expected 'func'"); name=self.consume("ID","expected function name").value
        self.consume("LPAREN","expected '(' after function name"); params=[]
        if not self.check("RPAREN"):
            params.append(self.consume("ID","expected parameter name").value)
            while self.match("COMMA"): params.append(self.consume("ID","expected parameter name after ','").value)
        self.consume("RPAREN","expected ')' after parameters")
        if len(set(params))!=len(params): raise ParserError("duplicate parameter name",self.peek())
        return FunctionDefNode(name,params,self.parse_block())
    def parse_return(self):
        self.consume("RETURN","expected 'return'"); expr=None
        if not self.check("SEMICOLON"): expr=self.parse_expression()
        self.consume("SEMICOLON","expected ';' after return")
        return ReturnNode(expr)
    def parse_assignment(self,declaration):
        if declaration: self.consume("LET","expected 'let'")
        name=self.consume("ID","expected variable name"); self.consume("ASSIGN","expected '=' after variable name")
        if self.check("SEMICOLON"): raise ParserError("expected expression after '='",self.peek())
        expr=self.parse_expression(); self.consume("SEMICOLON","expected ';' after assignment")
        return AssignmentNode(VariableNode(name.value),expr,declaration)
    def parse_print(self):
        self.consume("DISPLAY", "expected 'display'")
        # Parenthesized expressions are parsed by parse_primary(), so this
        # supports both display(expr); and display (expr) * value;.
        expr = self.parse_expression()
        self.consume("SEMICOLON", "expected ';' after display")
        return PrintNode(expr)
    def parse_if(self):
        self.consume("IF","expected 'if'"); self.consume("LPAREN","expected '(' after if"); cond=self.parse_expression(); self.consume("RPAREN","expected ')' after condition")
        then=self.parse_block(); other=self.parse_block() if self.match("ELSE") else None
        return IfNode(cond,then,other)
    def parse_while(self):
        self.consume("WLOOP","expected 'wloop'"); self.consume("LPAREN","expected '(' after wloop"); cond=self.parse_expression(); self.consume("RPAREN","expected ')' after condition")
        return WhileNode(cond,self.parse_block())
    def parse_block(self):
        self.consume("LBRACE","expected '{' to begin block"); stmts=[]
        while not self.check("RBRACE") and not self.is_at_end(): stmts.append(self.parse_statement())
        self.consume("RBRACE","expected '}' after block"); return BlockNode(stmts)
    def parse_expression(self): return self.parse_comparison()
    def parse_comparison(self):
        e=self.parse_addition()
        while self.check("EQUAL","NOT_EQUAL","LESS","GREATER","LESS_EQUAL","GREATER_EQUAL"):
            op=self.advance(); e=BinaryOpNode(op.value,e,self.parse_addition())
        return e
    def parse_addition(self):
        e=self.parse_multiplication()
        while self.check("PLUS","MINUS"):
            op=self.advance(); e=BinaryOpNode(op.value,e,self.parse_multiplication())
        return e
    def parse_multiplication(self):
        e=self.parse_unary()
        while self.check("MULTIPLY","DIVIDE","MODULO"):
            op=self.advance(); e=BinaryOpNode(op.value,e,self.parse_unary())
        return e
    def parse_unary(self):
        if self.match("PLUS"): return UnaryOpNode("+",self.parse_unary())
        if self.match("MINUS"): return UnaryOpNode("-",self.parse_unary())
        return self.parse_primary()
    def parse_primary(self):
        t=self.peek()
        if self.match("NUMBER"): return NumberNode(float(t.value) if "." in t.value else int(t.value))
        if self.match("TRUE"): return BooleanNode(True)
        if self.match("FALSE"): return BooleanNode(False)
        if self.match("STRING"): return StringNode(t.value)
        if self.match("ID"):
            if self.match("LPAREN"):
                args=[]
                if not self.check("RPAREN"):
                    args.append(self.parse_expression())
                    while self.match("COMMA"): args.append(self.parse_expression())
                self.consume("RPAREN","expected ')' after arguments")
                return FunctionCallNode(t.value,args)
            return VariableNode(t.value)
        if self.match("LPAREN"):
            e=self.parse_expression(); self.consume("RPAREN","expected ')' after expression"); return e
        raise ParserError("expected expression",t)
def parse_source(source): return Parser(lex(source)).parse()
def parse_tokens(tokens): return Parser(tokens).parse()
