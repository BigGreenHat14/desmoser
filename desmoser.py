import sys
def assign_to_main(var_name, value):
    """Assigns a variable to a value in the __main__ module's namespace."""
    main_module = sys.modules.get("__main__")
    if main_module:
        setattr(main_module, var_name, value)
class DesmosObject():
    def __init__(self,exp):
        if type(exp) == complex:
            self.exp = r"\left(" + str(exp.real) + " + " + str(exp.imag) + r"i\right)"
            self.rawexp = str(exp.real) + " + " + str(exp.imag) + "i"
        elif type(exp) == list:
            self.exp = "\\left[" + ",".join([str(i) for i in exp]) + "\\right]"
            self.rawexp = ",".join([str(i) for i in exp])
        elif type(exp) == tuple:
            self.exp = "\\left(" + ",".join([str(i) for i in list(exp)]) + "\\right)"
            self.rawexp = "\\left(" + ",".join([str(i) for i in list(exp)]) + "\\right)"
        elif type(exp) != DesmosObject:
            self.exp = r"\left(" + str(exp) + r"\right)"
            self.rawexp = exp
        else:
            self.exp = exp.exp
            self.rawexp = exp.rawexp
    def __add__(self,other):
        return DesmosObject(self.exp + r"+" + DesmosObject(other).exp)
    def __sub__(self,other):
        return DesmosObject(self.exp + r"-" + DesmosObject(other).exp)
    def __mul__(self,other):
        return DesmosObject(self.exp + r"\cdot" + DesmosObject(other).exp)
    def __truediv__(self,other):
        return DesmosObject(self.exp + r"\div" + DesmosObject(other).exp)
    def __floordiv__(self,other):
        return self._func((self.exp + r"\div" + DesmosObject(other).exp),"floor")
    def __mod__(self,other):
        return self._func(f"{self.exp},{DesmosObject(other).exp}","mod")
    def _func(self,exp,name):
        return DesmosObject(r"\operatorname{" + name + r"}\left(" + self + r"\right)")
    def __pow__(self,other):
        return DesmosObject(r"" + self.exp + r"^{" + DesmosObject(other).exp + r"}")
    def __eq__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r"=" + DesmosObject(other).exp + r":1,0\right\}")
    def __ne__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r"=" + DesmosObject(other).exp + r":0,1\right\}")
    def __lt__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r"<" + DesmosObject(other).exp + r":1,0\right\}")
    def __gt__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r">" + DesmosObject(other).exp + r":1,0\right\}")
    def __le__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r"\le" + DesmosObject(other).exp + r":1,0\right\}")
    def __ge__(self,other):
        return DesmosObject(r"\left\{" + self.exp + r"\ge" + DesmosObject(other).exp + r":1,0\right\}")
    def __trunc__(self):
        return DesmosObject(r"\operatorname{floor}\left(\left|" + self.exp + r"\right|\right)\cdot\operatorname{sign}\left(" + self.exp + r"\right)")
    def __ceil__(self):
        return self._func("ceil")
    def __round__(self):
        return self._func("round")
    def __floor__(self):
        return self._func("floor")
    def tocomplex(self):
        return DesmosObject(self.exp + "0i")
    def __repr__(self):
        return "DesmosObject(\"" + self.rawexp + "\")"
    def __str__(self):
        return self.rawexp
    def __get__(self,instance,owner):
        return DesmosObject(self.exp + "." + DesmosObject(instance))
    def __getitem__(self,instance):
        return DesmosObject(self.exp + "\\left[" + DesmosObject(instance) + "\\right]")
    def __len__(self):
        return DesmosObject(self.exp + ".\\operatorname{length}")
    def nth_root(self,n=2):
        return DesmosObject(r"\sqrt[" + DesmosObject(n).exp + "]{" + self.exp + "}")
    def convert_to_expression(self,assignvar:str="",action:str=""):
        assignvar = str(assignvar)
        action = str(action)
        if assignvar == "":
            return self.exp
        else:
            if action:
                return f"{assignvar} = {action} \\to {self.exp}"
            else:
                return f"{assignvar} = {self.exp}"
def join_actions(actions:list):
    actions = [DesmosObject(i) for i in actions]
    return ",".join(actions)
def builtin_function(obj,name):
    DesmosObject(obj)._func(name)
def function(name,*params):
    return f"{var(name)}\\left({','.join([value.exp for value in _listexp(params)])}\\right)"
def if_else(condition,trueval,falseval="0\\div0"):
    return DesmosObject("\\left\\{" + DesmosObject(condition).exp + " = 0:" + DesmosObject(falseval).exp + "," + DesmosObject(trueval).exp + "\\right\\}")
def imag(obj):
    return DesmosObject(r"\operatorname{imag}\left(" + obj + "\\right)")
def real(obj):
    return DesmosObject(r"\operatorname{real}\left(" + obj + "\\right)")
def _listexp(l):
    return [DesmosObject(value) for value in list(l)]
def match_case(select:DesmosObject,options:dict):
    if type(options) == list: options = {i: v for i, v in enumerate(options)}
    options = {key: DesmosObject(value) for key, value in options.items()}
    obj = undefined
    for key,value in options.items(): obj = if_else(select == key,value,obj)
    return obj
def var(name):
    subscript = name[1:]
    name = name[0]
    if not subscript:
        return DesmosObject(name)
    else:
        return DesmosObject(name + "_{" + subscript + "}")
try:
    noautodef = sys.modules["__main__"].__dict__["_noautodef"]
except:
    noautodef = False
if not noautodef:
    for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ":
        assign_to_main(i,DesmosObject(i))
    assign_to_main("expression",DesmosObject)
    assign_to_main("if_else",if_else)
    assign_to_main("join_actions",join_actions)
    assign_to_main("var",var)
    assign_to_main("builtin_function",builtin_function)
    assign_to_main("function",function)
    undefined = DesmosObject("0\\div0")
    assign_to_main("undefined",undefined)
    assign_to_main("match_case",match_case)