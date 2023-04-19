# Generated from funx.g4 by ANTLR 4.7.2
from flask import Flask, request, render_template, jsonify
from antlr4 import *
from funxLexer import funxLexer
from funxParser import funxParser
from funxVisitor import funxVisitor
import sys
if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
else:
    from funxParser import funxParser

#Funcions d'operacions aritmètiques o condicionals
def suma (a, b):
    return a + b
def resta (a,b):
    return a-b
def mult (a,b):
    return a*b
def div (a,b):
    if(b==0):
        raise ZeroDivisionError
    return a//b
def pot (a,b):  #Elevar a a la potència de b
    return a**b
def mod (a,b):
    return a % b
def igual (a,b):
    if a==b: return 1
    return 0
def diferent (a,b):
    if a!=b :return 1
    return 0
def mgranq (a,b):
     if a>b: return 1
     return 0
def mpetitq (a,b):
    if a<b: return 1
    return 0
def mgranigual (a,b):
    if a>=b : return 1
    return 0
def mpetitigual (a,b):
    if a<=b: return 1
    return 0

operadors = {'+': suma, '-': resta,
               '*': mult, '/': div, '^': pot, '%':mod}
comparacions = {'=': igual, '<': mpetitq,
                 '>': mgranq, '<=': mpetitigual, '>=': mgranigual, '!=':diferent}

class funxVisitor(ParseTreeVisitor):
    def __init__(self):
        self.variables=[{}]
        self.funcions={}


    def getFuncs (self): return self.funcions

    #visitors
    # Visit a parse tree produced by funxParser#root.
    def visitRoot(self, ctx:funxParser.RootContext):
        l= list(ctx.getChildren())
        return self.visit(l[0])

    # Visit a parse tree produced by funxParser#bloc.
    def visitBloc(self, ctx:funxParser.BlocContext):
        l=list(ctx.getChildren())
        for i in l:
           res= self.visit(i)
           if(res is not None): return res


    # Visit a parse tree produced by funxParser#instru.
    def visitInstru(self, ctx:funxParser.InstruContext):
        l=list(ctx.getChildren())
        return self.visit(l[0])


    # Visit a parse tree produced by funxParser#func.
    def visitFunc(self, ctx:funxParser.FuncContext):
        l=list(ctx.getChildren())
        nomFuncio=l[0].getText()
        if(self.funcions.get(nomFuncio) is not None) : raise Exception("ERROR: This function already exists")
        listVars=self.visit(l[1])
        bloc=l[3]
        self.funcions[nomFuncio]=[listVars,bloc]
        return None


    # Visit a parse tree produced by funxParser#assignacioVars.
    def visitAssignacioVars(self, ctx:funxParser.AssignacioVarsContext):
        l=list(ctx.getChildren())
        listReturn=[]
        for i in l:
          if len(listReturn)>0:
              if (i.getText()==listReturn[-1]) : raise Exception("ERROR: The parameters have to be different")
          listReturn.append(i.getText())
        return listReturn


    # Visit a parse tree produced by funxParser#funcCall.
    def visitFuncCall(self, ctx:funxParser.FuncCallContext):
        l=list(ctx.getChildren())
        nom=l[0].getText()
        if(self.funcions.get(nom) is None) : raise Exception("ERROR: This function doesn't exist")
        listVars= self.visit(l[1])
        context= self.funcions[nom] #recupera context i variables al diccionari mitjançant el nom
        var= context[0]
        cosFunc= context[1]

        self.variables.append({})
        if (len(listVars)!=len(var)): raise Exception ("ERROR: Incorrect number of parameters")
        for index, variable in enumerate(var):
            self.variables[-1][variable] = listVars[index]

        res = self.visit(cosFunc)

        self.variables.pop()
        print('Out :', res)
        return res

    def visitBlocFunc(self, ctx):
        l = list(ctx.getChildren())
        for i in l:
            res = self.visit(i)
            if type(res) is int:
                return res

        return None

    # Visit a parse tree produced by funxParser#crearParams.
    def visitCrearParams(self, ctx:funxParser.CrearParamsContext):
        l=list(ctx.getChildren())

        listReturn=[]
        for i in l:
            listReturn.append(self.visit(i))
        return listReturn

    # Visit a parse tree produced by funxParser#expr.
    def visitExpr(self, ctx:funxParser.ExprContext):
        l=list(ctx.getChildren())
        if (len(l)==1):
            cont=l[0].getText()
            if(cont.isnumeric()) :
                return int(cont)
            elif cont[0].isupper():
                return self.visit(l[0])
            else:
                return self.variables[-1][cont]
        if (len(l)==2) : return -int(l[1].getText()) #num negatiu
        else:
            if l[0].getText()=='(':
                return self.visit(l[1])
            else:
                num1=self.visit(l[0])
                operador=l[1].getText()
                num2=self.visit(l[2])

                return operadors[operador](num1,num2)


    # Visit a parse tree produced by funxParser#cond.
    def visitCond(self, ctx:funxParser.CondContext):
        l=list(ctx.getChildren())
        v1=self.visit(l[0])
        c=l[1].getText()
        v2=self.visit(l[2])
        return comparacions[c](v1,v2)

    # Visit a parse tree produced by funxParser#assignacio.
    def visitAssignacio(self, ctx:funxParser.AssignacioContext):
        l=list(ctx.getChildren())
        var=l[0].getText()
        valor=self.visit(l[2])
        self.variables[-1][var]=valor
        return None


    # Visit a parse tree produced by funxParser#writeClause.
    def visitWriteClause(self, ctx:funxParser.WriteClauseContext): #extensió: permet imprimir per pantalla mitjançant print(instrucció)
        l=list(ctx.getChildren())
        print("Out: ",self.visit(l[1]))
        return None

    # Visit a parse tree produced by funxParser#ifClause.
    def visitIfClause(self, ctx:funxParser.IfClauseContext):
        l=list(ctx.getChildren())
        if (self.visit(l[1])):
            return self.visit(l[3])
        else:
            if(len(l)==6):
                return self.visit(l[5])


    # Visit a parse tree produced by funxParser#elseClause.
    def visitElseClause(self, ctx:funxParser.ElseClauseContext):
        l = list(ctx.getChildren())
        return self.visit(l[2])


    # Visit a parse tree produced by funxParser#whileLoop.
    def visitWhileLoop(self, ctx:funxParser.WhileLoopContext):
        l = list(ctx.getChildren())
        while (self.visit(l[1])):
            self.visit(l[3])
    def getFuncions(self): return self.funcions
    def getLast(self): return self.last

#PART VISUAL INTÈRPRET:

class funxInterp:
    def __init__(self):
        self.variables = [{}]
        self.funcions = {}
        self.last=[]
        self.visitor=funxVisitor()
        self.num=0
        self.enum=[]
    def executar(self,code):
        input_stream= InputStream(code)
        lexer= funxLexer(input_stream)
        token_stream= CommonTokenStream(lexer)
        parser= funxParser(token_stream)
        tree= parser.root()

        try:
            res=self.visitor.visit(tree)
        except ZeroDivisionError:
            res= "ERROR: You are trying to divide by zero"
        except Exception as e:
            res= str(e)
        self.last.append(res)
        self.num = self.num + 1
        self.enum.append((self.num)) #per l'html per imprimir els 5 últims inputs amb número



app = Flask(__name__)
visual= funxInterp()
inputs=[]

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        code= request.form ["input"]
        visual.executar(code)
        lastresults=visual.last
        last5= lastresults[-5:]
        nums=visual.enum
        nums=nums[-5:]
        inputs.append(code)
        inputs5=inputs[-5:]
        return render_template('base.html',funcs= visual.visitor.getFuncions(),last5=last5,num=nums,inputs=inputs5) #crida al template
    else:
        lastresults = visual.last
        last5 = lastresults[-5:]
        return render_template('base.html',funcs = visual.visitor.getFuncions(),last5=last5) #crida el template

