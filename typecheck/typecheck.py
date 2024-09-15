from dataclasses import dataclass
from typing import List, Dict, Tuple

from mypyc.irbuild.format_str_tokenizer import tokenizer_format_call
from typing_extensions import assert_never

from typecheck.syntree import IntLiteral, RealLiteral, TextLiteral, Statement, FuncDecl, Expression, \
    FuncCall, BinaryMathOp, ReadVar, Assignment
from typecheck.typ import Type, Int, Real, Text, Null, Scalar


@dataclass
class Var:
    bound: Type
    #TODO @mark: does type bound need to be different from Type

    def type_name(self) -> str:
        return 'variable'


BindingKind = FuncDecl | Var
TypeState = Dict[str, BindingKind]


def check(prog: List[Statement]) -> Type | str:
    types: TypeState = {}
    last: Type = Null
    for stmt in prog:
        if isinstance(stmt, FuncDecl):
            if stmt.name in types:
                return f"function name '{stmt.name}' already declared (as {type(types[stmt.name]).__name__})"
            types[stmt.name] = stmt
        elif isinstance(stmt, Assignment):
            declared_typ = stmt.typ
            infer_typ = infer(stmt.value, types)
            if isinstance(infer_typ, str):
                return infer_typ
            if stmt.name in types:
                type_res = infer_reassignment(declared_typ, infer_typ, types[stmt.name])
            else:
                type_res = infer_declaration(declared_typ, infer_typ)
            if isinstance(type_res, str):
                return type_res
            types[stmt.name] = Var(type_res)
        else:
            infer_type = infer(stmt, types)
            if isinstance(infer_type, str):
                return infer_type
            last = infer_type
    return last


def infer(expr: Expression, types: TypeState) -> Type | str:
    # if expr in list(Scalar):
    #     return expr
    #TODO @mark: TEMPORARY! REMOVE THIS!
    if isinstance(expr, IntLiteral):
        return Int
    elif isinstance(expr, RealLiteral):
        return Real
    elif isinstance(expr, TextLiteral):
        return Text
    elif isinstance(expr, ReadVar):
        if not expr.name in types:
            return f"variable not found '{expr.name}'"
        target = types[expr.name]
        if not isinstance(target, Var):
            return f"tried to read '{expr.name}' but it is not a variable (it does exist)"
        return target.bound
    elif isinstance(expr, BinaryMathOp):
        func_call = expr.as_func_call()
        equivalent_functions = expr.as_func_decls()
        return infer_func_call_overloads(func_call, equivalent_functions, types)
    elif isinstance(expr, FuncCall):
        if expr.name not in types:
            return f"cannot call function '{expr.name}' because no such function is known"
        func = types[expr.name]
        if not isinstance(func, FuncDecl):
            return f"cannot call '{expr.name}' because it is a {func.type_name()}, not a function"
        return infer_func_call(expr, func, types)
    assert_never(expr)


def infer_reassignment(declared_typ: Type | None, infer_typ: Type, known_binding: BindingKind) -> Type | str:
    if isinstance(declared_typ, Var):
        return "not var"
        #TODO @mark:
    if declared_typ is not None:
        return f"redeclared"
        #TODO @mark:

        if is_assignable(declared_typ, infer_typ):
            return f"wrong type"
    if declared_typ is None:
        if known_binding is None:
            # newly declared
            pass
        else:
            # re-assign
            pass
    else:
        #
        pass


    if stmt.name in types:
        existing = types[stmt.name]
    if not isinstance(existing, Var):
        return f"variable name '{stmt.name}' already declared (as {type(types[stmt.name]).__name__})"
    if stmt.typ is not None:
        return (f"variable '{stmt.name}' cannot be declared because it is already declared (as "
                f"{type(existing).__name__}) (interpreting as declaration because of type "
                f"annotation {stmt.typ.__name__})")
    if not is_assignable(existing.bound, typ):
        return (f'variable {stmt.name} has type {existing.bound.__name__} but is being assigned an '
                f'expression of type {typ.__name__}, which is not compatible')
    types[stmt.name] = Var(typ)




def infer_declaration(declared_typ: Type | None, infer_typ: Type):
    if declared_typ is None:
        return infer_typ
    if is_assignable(declared_typ, infer_typ):
        return f"wrong type"
        #TODO @mark:
    return declared_typ


def infer_func_call(func_call: FuncCall, func_decl: FuncDecl, types: TypeState, actual_arg_types: List[Type] = None) -> Type | str:
    # #TODO @mark: problem if `infer` updates `types` but we select another overload
    actual_arg_types = actual_arg_types or [infer(arg, types) for arg in func_call.args]
    if len(func_call.args) != len(func_decl.params):
        return (f"cannot call function '{func_call.name}' with "
                f"{len(func_call.args)} args because it expects {len(func_decl.params)}")
    for nr, (arg_type, param_type) in enumerate(zip(actual_arg_types, func_decl.params)):
        if not is_assignable(arg_type, param_type):
            return (f"cannot call function '{func_call.name}' because argument {nr + 1} "
                    f"is of type {arg_type.type_name()}, while {param_type.type_name()} is expected")
    return func_decl.returns


def infer_func_call_overloads(func_call: FuncCall, func_decls: List[FuncDecl], types: TypeState) -> Type | str:
    assert len(func_decls) >= 1
    # #TODO @mark: problem if `infer` updates `types` but we select another overload [same as infer_func_call]
    actual_arg_types = [infer(arg, types) for arg in func_call.args]
    for func_decl in func_decls:
        res = infer_func_call(func_call, func_decl, types, actual_arg_types=actual_arg_types)
        if isinstance(res, str):
            continue
        #TODO @mark: probably should return func_decl later
        return res
    return f"none of {len(func_decls)} variants of '{func_call.name}' accept argument of types ({', '.join(arg.type_name() for arg in actual_arg_types)})"


def is_assignable(value_type: Type, target_type: Type):
    return value_type == target_type


