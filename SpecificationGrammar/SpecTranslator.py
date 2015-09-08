from antlr4 import *
from SpecificationGrammarLexer import SpecificationGrammarLexer
from SpecificationGrammarParser import SpecificationGrammarParser
from SpecificationGrammarVisitor import SpecificationGrammarVisitor

import settings

class SpecificationParsingException(Exception):
  
  def __init__(self,value):
    self.value = value
  
  def __str__(self):
    return repr(self.value)

class MyVisitor(SpecificationGrammarVisitor):

  def __init__(self, resources, services):
    """
    classes containing  a hash function mapping classes with scenarios
    resources and services are simple hash functions containing
    the name of resources and services
    """    
    SpecificationGrammarVisitor.__init__(self)
    self.resources = resources
    self.services = services

  def defaultResult(self):
    return ""
  
  def visitTerminal(self, node):
    return node.getText()
  
  def aggregateResult(self, aggregate, nextResult):
    return aggregate + " " + nextResult
  
  def visitErrorNode(self, node):
    raise SpecificationParsingException("Erroneous Node")
    
  # Visit a parse tree produced by SpecificationGrammarParser#AexprNoDCService.
  def visitAexprNoDCService(self, ctx):
    service_name = ctx.getChild(0).accept(self)
    if settings.DEFAULT_SERVICE_NAME + settings.SEPARATOR + service_name not in self.services:
      raise SpecificationParsingException("Service " + service_name + " is not a valid service name")
    return '#' + settings.DEFAULT_SERVICE_NAME + settings.SEPARATOR + service_name + ":On" 
   
  # Visit a parse tree produced by SpecificationGrammarParser#AresourceFilterOp.
  def visitAresourceFilterOp(self, ctx):
    resource_name = ctx.getChild(0).accept(self)
    if settings.RESOURCE_PREFIX + resource_name not in self.resources:
      raise SpecificationParsingException("Resource " + resource_name + " is not a valid resource name")
    return settings.RESOURCE_PREFIX + resource_name + " " + ctx.getChild(1).accept(self) + " " + ctx.getChild(2).accept(self)

  # Visit a parse tree produced by SpecificationGrammarParser#AexprDC.
  def visitAexprDC(self, ctx):
    res = ctx.getChild(1).accept(self)
    spec = ctx.getChild(3).accept(self)
    return "#(" + res + "){ _ : " + spec + "}"

  # Visit a parse tree produced by SpecificationGrammarParser#AexprDCNoFilter.
  def visitAexprDCNoFilter(self, ctx):
    spec = ctx.getChild(1).accept(self)
    return "#(_){ _ : " + spec + "}"
  
  # Visit a parse tree produced by SpecificationGrammarParser#bool2Op.
  def visitBool2Op(self, ctx):
    op = self.visitChildren(ctx)
    if op == "impl":
      return "=>"
    elif op == "iff":
      return "<=>"
    else:
      return op
  

def translate_specification(inFile, resources, services):
  lexer = SpecificationGrammarLexer(FileStream(inFile))
  stream = CommonTokenStream(lexer)
  parser = SpecificationGrammarParser(stream)
  tree = parser.spec()
  visitor = MyVisitor(resources, services)
  return visitor.visit(tree)