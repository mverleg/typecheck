from dataclasses import dataclass
from typing import List, Dict

from typing_extensions import assert_never

from typecheck.syntree import IntLiteral, RealLiteral, TextLiteral, Statement, FuncDecl, Expression, \
    FuncCall, BinaryMathOp, ReadVar
from typecheck.typ import Type, Int, Real, Text, Null


@dataclass
class Var:
    bound: Type
    #TODO @mark: does type bound need to be different from Type


TypeState = Dict[str, FuncDecl | Var]


def check(prog: List[Statement]) -> Type | str:
    types: TypeState = {}
    last: Type = Null
    for stmt in prog:
        if isinstance(stmt, FuncDecl):
            if stmt.name in types:
                return f"function name '{stmt.name}' already declared"
            types[stmt.name] = stmt
        else:
            infer_type = infer(stmt, types)
            if isinstance(infer_type, str):
                return infer_type
            last = infer_type
    return last


def infer(expr: Expression, types: TypeState) -> Type | str:
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
        for func_decl in expr.as_func_decls():
            # this infers arg types n+1 times
            func_res = infer_func_call(func_call, func_decl, types)
            if not isinstance(func_res, str):
                return func_res
        return f"no variant of {expr.kind.name} for arguments ({infer(expr.left, types)}, {infer(expr.right, types)})"
    elif isinstance(expr, FuncCall):
        if expr.name not in types:
            return f"cannot call function '{expr.name}' because no such function is known"
        return infer_func_call(expr, types[expr.name], types)
    assert_never(expr)


def infer_func_call(func_call: FuncCall, func_decl: FuncDecl, types: TypeState):
    if len(func_call.args) != len(func_decl.params):
        return (f"cannot call function '{func_call.name}' with "
                f"{len(func_call.args)} args because it expects {len(func_decl.params)}")
    for nr, (arg, param) in enumerate(zip(func_call.args, func_decl.params)):
        arg_type = infer(arg, types)
        if not is_assignable(arg_type, param):
            return (f"cannot call function '{func_call.name}' because argument {nr + 1} "
                    f"is of type {arg_type}, while {param} is expected")
    return func_decl.returns


def is_assignable(value_type: Type, target_type: Type):
    return value_type == target_type


