import pdb
import runtime
import traceback
from environment import *
from runtime_exceptions import *
from helper_functions import *
from offset import *
from datatype import *
from environment_stack import *

class Bytecode:
    
    def READ(self,scope,instr,curr_line_number):
        scope.push_stack(raw_input())
        
    def DECLI(self,scope,instr,curr_line_number):
        scope.declare_variable(instr.arg[0],'int')
        
    def DECLB(self,scope,instr,curr_line_number):
        scope.declare_variable(instr.arg[0],'bool')
        
    def STORE(self,scope,instr,curr_line_number):
        var_value = scope.pop_stack()
        if scope.symbol_exists(instr.arg[0]) == True:
            scope.store_variable(instr.arg[0],var_value)
        else:
            check_scope = self.retrieve_scope(scope,instr.arg[0],curr_line_number)
            check_scope.store_variable(instr.arg[0],var_value)
        
    def PUSH(self,scope,instr,curr_line_number):
        if isInt(instr.arg[0]) or isBool(instr.arg[0]):               # isInt is from helper_functions module
            scope.push_stack(instr.arg[0])
        else:
            if scope.symbol_exists(instr.arg[0]) == True:
                scope.push_stack(scope.retrieve_symbol(instr.arg[0]))
            else:
                check_scope = self.retrieve_scope(scope,instr.arg[0],curr_line_number)
                scope.push_stack(check_scope.retrieve_symbol(instr.arg[0]))
                
            
            
    def PRINTLN(self,scope,instr,curr_line_number):
        i=0
        while i<len(instr.arg):
            if instr.arg[i][0] == "'" and instr.arg[i][len(instr.arg[i])-1] == "'":
                print instr.arg[i].replace("'","").replace("%"," "),
            else:
                if scope.symbol_exists(instr.arg[i]) == True:
                    #pdb.set_trace()
                    print scope.retrieve_symbol(instr.arg[i].replace("'","")),
                else:
                    check_scope = self.retrieve_scope(scope,instr.arg[i],curr_line_number)
                    print check_scope.retrieve_symbol(instr.arg[i]),
            i+=1
        print ''
        
    def EQUAL(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if left_operand == right_operand:
            scope.push_stack(True)
        else:
            scope.push_stack(False)
                
        
    def GTR(self,scope,instr,curr_line_number):
        #pdb.set_trace()
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if left_operand > right_operand:
            #pdb.set_trace()
            scope.push_stack(True)
        else:
            #pdb.set_trace()
            scope.push_stack(False)
            
    def LESS(self,scope,instr,curr_line_number):
        #pdb.set_trace()
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        #pdb.set_trace()
        if left_operand < right_operand:
            scope.push_stack(True)
        else:
            scope.push_stack(False)
        
    def AND(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if left_operand and right_operand:
            scope.push_stack(True)
        else:
            scope.push_stack(False)
            
    def OR(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if left_operand or right_operand:
            scope.push_stack(True)
        else:
            scope.push_stack(False)
            
    def TESTFGOTO(self,scope,instr,curr_line_number):
        #pdb.set_trace()
        if scope.pop_stack() == False:
            #pdb.set_trace()
            curr_line_number[0] = int(instr.arg[0])-1
            
    def TESTTGOTO(self,scope,instr,curr_line_number):
        #pdb.set_trace()
        if scope.pop_stack() == True:
            curr_line_number[0] = int(instr.arg[0])-1
    
    def ADD(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if isInt(left_operand) and isInt(right_operand):
            scope.push_stack(left_operand+right_operand)
        else:
            raise OperandTypeException({
                        'symbol' : 'add',
                    })
        
    def SUB(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        #pdb.set_trace()
        if isInt(left_operand) and isInt(right_operand):
            scope.push_stack(left_operand-right_operand)        
        else:
            raise OperandTypeException({
                        'symbol' : 'sub',
                    })
                
    def MUL(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if isInt(left_operand) and isInt(right_operand):
            scope.push_stack(left_operand*right_operand)       
        else:
            raise OperandTypeException({
                        'symbol' : 'mul',
                    })
        
    def DIV(self,scope,instr,curr_line_number):
        right_operand = scope.pop_stack()
        left_operand = scope.pop_stack()
        if isInt(left_operand) and isInt(right_operand):
            scope.push_stack(left_operand/right_operand)  
        else:
            raise OperandTypeException({
                        'symbol' : 'div',
                    })
        
    def FUNCSTART(self,scope,variable,curr_line_number):
        #pdb.set_trace()
        for i in xrange(curr_line_number[0],len(prog_list)):
            line = prog_list[i]
            if 'FUNCEND' in line:
                #pdb.set_trace()
                return
            curr_line_number[0]+=1    
    
    def retrieve_scope(self,scope,variable,curr_line_number):
        curr_scope_index = len(environment_stack)-2
        check_scope = environment_stack[curr_scope_index]
        while curr_scope_index >= 0 and check_scope.symbol_exists(variable) == False:
            curr_scope_index -= 1
            check_scope = environment_stack[curr_scope_index]
        if curr_scope_index < 0:
            raise SymbolDoesNotExistException({
                'symbol' : variable,
            })
        else:
            return check_scope
        