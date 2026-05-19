# =========================
# Imports
# =========================

# --- Third-party ---
import duckdb
import pandas as pd

# --- Standard library ---
import re
from html import escape
from typing import Any, Optional, Callable, List


# =========================
# READ tools (simple internal SQL when applicable)
# =========================
def t_get_inventory_data(
    con: duckdb.DuckDBPyConnection,
    product_name: Optional[str] = None,
    item_id: Optional[str] = None
) -> dict[str, Any]:
    """
    Lee inventario por nombre (case-insensitive) o item_id.
    Retorna {"rows": DataFrame, "match_count": int, "item": dict|None}
    """
    if not product_name and not item_id:
        # sin filtros: devolver todo (útil para browse)
        df = con.execute("SELECT * FROM inventory_df").df()
    elif item_id:
        df = con.execute(
            "SELECT * FROM inventory_df WHERE item_id = ?",
            [item_id]
        ).df()
    else:
        df = con.execute(
            "SELECT * FROM inventory_df WHERE lower(name)=lower(?)",
            [product_name]
        ).df()
    item = df.iloc[0].to_dict() if len(df) == 1 else None
    return {"rows": df, "match_count": int(len(df)), "item": item}


def t_get_transaction_data(
    con: duckdb.DuckDBPyConnection,
    mode: str = "last_balance"
) -> dict[str, Any]:
    """
    mode="last_balance": retorna último balance y ultima id
    """
    if mode == "last_balance":
        df = con.execute(
            "SELECT transaction_id, balance_after_transaction "
            "FROM transaction_df ORDER BY transaction_id DESC LIMIT 1"
        ).df()
        last_id = str(df.iloc[0]["transaction_id"]) if not df.empty else None
        last_bal = float(df.iloc[0]["balance_after_transaction"]) if not df.empty else 0.0
        return {"mode": mode, "last_txn_id": last_id, "last_balance": last_bal}
    return {"mode": mode}


# =========================
# WRITE tools (mutate DataFrames in memory via return values)
# =========================
def _next_txn_id(df: pd.DataFrame, prefix: str = "TXN") -> str:
    if df.empty:
        return f"{prefix}001"
    nums = []
    for v in df["transaction_id"].astype(str):
        tail = re.findall(r"(\d+)$", v)
        nums.append(int(tail[0]) if tail else 0)
    nxt = (max(nums) if nums else 0) + 1
    return f"{prefix}{nxt:03d}"


def t_update_inventory(
    inventory_df: pd.DataFrame,
    item_id: str,
    quantity_new: Optional[int] = None,
    delta: Optional[int] = None
) -> dict[str, Any]:
    """
    Actualiza cantidad por item_id:
    - si 'delta' está provisto: nueva = actual + delta
    - si 'quantity_new' está provisto: nueva = ese valor
    Retorna {"inventory_df": df_actualizado, "updated": {...}}
    """
    if item_id is None:
        return {"error": "item_id_missing"}
    inv = inventory_df.copy()
    inv["item_id"] = inv["item_id"].astype(str)
    mask = inv["item_id"] == str(item_id)
    if not mask.any():
        return {"error": "item_not_found"}
    current = int(inv.loc[mask, "quantity_in_stock"].iloc[0])
    if delta is None and quantity_new is None:
        return {"error": "need_delta_or_quantity_new"}
    new_q = int(quantity_new) if quantity_new is not None else current + int(delta)
    inv.loc[mask, "quantity_in_stock"] = new_q
    return {"inventory_df": inv, "updated": {"item_id": item_id, "quantity_in_stock": int(new_q)}}


def t_append_transaction(
    transaction_df: pd.DataFrame,
    customer_name: str,
    summary: str,
    amount: float,
    txn_prefix: str = "TXN"
) -> dict[str, Any]:
    """
    Agrega una transacción y recalcula balance con base en el último registro.
    Retorna {"transaction_df": df_actualizado, "transaction": {...}}
    """
    out = transaction_df.copy()
    last_bal = float(out["balance_after_transaction"].iloc[-1]) if not out.empty else 0.0
    new_bal = last_bal + float(amount)
    txn_id = _next_txn_id(out, txn_prefix)
    row = {
        "transaction_id": txn_id,
        "customer_name": customer_name,
        "transaction_summary": summary,
        "transaction_amount": float(amount),
        "balance_after_transaction": new_bal
    }
    out = pd.concat([out, pd.DataFrame([row])], ignore_index=True)
    return {"transaction_df": out, "transaction": row}


# =========================
# Propose-only (does not mutate DataFrame, only computes new balance)
# =========================
def t_propose_transaction(
    con: duckdb.DuckDBPyConnection,
    customer_name: str,
    summary: str,
    amount: float
) -> dict[str, Any]:
    df = con.execute(
        "SELECT balance_after_transaction FROM transaction_df "
        "ORDER BY transaction_id DESC LIMIT 1"
    ).df()
    last_bal = float(df.iloc[0, 0]) if not df.empty else 0.0
    new_bal = last_bal + float(amount)
    return {
        "transaction_id": "AUTO_TXN",
        "customer_name": customer_name,
        "transaction_summary": summary,
        "transaction_amount": float(amount),
        "balance_after_transaction": new_bal
    }


# =========================
# Helpers (calculations & validations)
# =========================
def t_compute_total(qty: int, price: float) -> dict[str, Any]:
    return {"amount": float(qty) * float(price)}


def t_compute_refund(qty: int, price: float) -> dict[str, Any]:
    return {"amount": -float(qty) * float(price)}


def t_assert_true(value: Any) -> dict[str, Any]:
    ok = bool(value)
    return {"ok": ok}


def t_assert_non_null(value: Any) -> dict[str, Any]:
    return {"ok": value is not None}


def t_assert_gt(value: float, threshold: float) -> dict[str, Any]:
    try:
        return {"ok": float(value) > float(threshold)}
    except Exception:
        return {"ok": False, "reason": "non_numeric"}


def t_assert_nonnegative_stock(inventory_df: pd.DataFrame, item_id: str) -> dict[str, Any]:
    inv = inventory_df
    mask = inv["item_id"].astype(str) == str(item_id)
    if not mask.any():
        return {"ok": False, "reason": "item_not_found"}
    q = int(inv.loc[mask, "quantity_in_stock"].iloc[0])
    return {"ok": q >= 0, "qty": q}


# =========================
# Project inventory (projection-style alias; internally uses update)
# =========================
def t_project_inventory(inventory_df: pd.DataFrame, item_id: str, delta: int) -> dict[str, Any]:
    return t_update_inventory(inventory_df=inventory_df, item_id=item_id, delta=delta)


# =========================
# Tool registry (includes aliases used by the plan/LLM)
# =========================
ToolFn = Callable[..., dict[str, Any]]
TOOL_REGISTRY: dict[str, ToolFn] = {
    # READ
    "get_inventory_data":      lambda **kw: t_get_inventory_data(kw["con"], kw.get("product_name"), kw.get("item_id")),
    "get_transaction_data":    lambda **kw: t_get_transaction_data(kw["con"], kw.get("mode", "last_balance")),
    # Aliases esperados por algunos planes
    "lookup_product":          lambda **kw: t_get_inventory_data(kw["con"], kw.get("product_name"), kw.get("item_id")),

    # WRITE / mutate
    "update_inventory":        lambda **kw: t_update_inventory(kw["inventory_df"], kw["item_id"], kw.get("quantity_new"), kw.get("delta")),
    "append_transaction":      lambda **kw: t_append_transaction(kw["transaction_df"], kw["customer_name"], kw["summary"], kw["amount"], kw.get("txn_prefix","TXN")),
    # Propose-only
    "propose_transaction":     lambda **kw: t_propose_transaction(kw["con"], kw["customer_name"], kw["summary"], kw["amount"]),
    # Projection alias (delta)
    "project_inventory":       lambda **kw: t_project_inventory(kw["inventory_df"], kw["item_id"], kw["delta"]),

    # helpers
    "compute_total":           lambda **kw: t_compute_total(kw["qty"], kw["price"]),
    "compute_refund":          lambda **kw: t_compute_refund(kw["qty"], kw["price"]),

    # validations
    "assert_true":             lambda **kw: t_assert_true(kw["value"]),
    "assert":                  lambda **kw: t_assert_true(kw["value"]),           # alias
    "assert_non_null":         lambda **kw: t_assert_non_null(kw["value"]),
    "assert_gt":               lambda **kw: t_assert_gt(kw["value"], kw["threshold"]),
    "assert_nonnegative_stock":lambda **kw: t_assert_nonnegative_stock(kw["inventory_df"], kw["item_id"]),
}


# =========================
# Required-arg spec + canonicalization
# =========================
TOOL_SIGNATURES = {
    # READ
    "get_inventory_data": [],
    "get_transaction_data": [],
    # Alias (permitimos product_name o item_id, por eso no exigimos)
    "lookup_product": [],

    # WRITE / mutate
    "update_inventory": ["item_id"],                # además requiere uno de {delta, quantity_new}
    "append_transaction": ["customer_name", "summary", "amount"],
    "project_inventory": ["item_id", "delta"],

    # Propose-only
    "propose_transaction": ["customer_name", "summary", "amount"],

    # helpers
    "compute_total": ["qty", "price"],
    "compute_refund": ["qty", "price"],

    # validations
    "assert_true": ["value"],
    "assert": ["value"],
    "assert_non_null": ["value"],
    "assert_gt": ["value", "threshold"],
    "assert_nonnegative_stock": ["inventory_df", "item_id"],
}


def canonicalize_args(tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    a = dict(args or {})

    # lookup_product / get_inventory_data
    if tool_name in ("lookup_product", "get_inventory_data"):
        if "product_name" not in a:
            for alt in ("name", "product", "query"):
                if alt in a and a[alt] is not None:
                    a["product_name"] = a.pop(alt)
                    break
        # item_id pasa tal cual si viene

    # compute_total / compute_refund: quantity->qty, unit_price->price
    if tool_name in ("compute_total", "compute_refund"):
        if "qty" not in a and "quantity" in a:
            a["qty"] = a.pop("quantity")
        if "price" not in a and "unit_price" in a:
            a["price"] = a.pop("unit_price")
        # 'sign' se ignora; refund ya maneja el signo negativo

    # update_inventory / project_inventory: alias change->delta, new_quantity->quantity_new
    if tool_name in ("update_inventory", "project_inventory"):
        if "delta" not in a and "change" in a:
            a["delta"] = a.pop("change")
        if "quantity_new" not in a:
            for alt in ("new_quantity", "quantity", "qty_new"):
                if alt in a and a[alt] is not None:
                    a["quantity_new"] = a.pop(alt)
                    break

    # propose/append_transaction: summary alias
    if tool_name in ("propose_transaction", "append_transaction"):
        if "summary" not in a and "transaction_summary" in a:
            a["summary"] = a.pop("transaction_summary")

    return a


def missing_required(tool_name: str, args: dict[str, Any]) -> List[str]:
    req = TOOL_SIGNATURES.get(tool_name, [])
    missing = [k for k in req if k not in args or args[k] is None]
    # regla especial: update_inventory necesita delta o quantity_new
    if tool_name == "update_inventory" and ("delta" not in args and "quantity_new" not in args):
        missing.append("delta|quantity_new")
    return missing


MISSING = object()


def get_from_context(ctx: dict[str, Any], path: str, default: Any = MISSING):
    if not isinstance(path, str) or not path.startswith("context."):
        return path
    cur: Any = ctx
    for part in path.split(".")[1:]:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


def resolve_args(args: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in (args or {}).items():
        if isinstance(v, str) and v.startswith("context."):
            val = get_from_context(ctx, v, default=None)
            out[k.replace("_from", "")] = val
        else:
            out[k] = v
    return out


# =========================
# 4) Executor (tools-only plan)
# =========================

def run_tools_for_step(step: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    results = {}
    for spec in step.get("tools", []):
        name = spec.get("use")
        rkey = spec.get("result_key")
        if not name or not rkey:
            raise ValueError("Each tool spec requires 'use' and 'result_key'")
        fn = TOOL_REGISTRY.get(name)
        if not fn:
            raise ValueError(f"Unknown tool: {name}")

        raw_args = spec.get("args", {})
        args = resolve_args(raw_args, ctx)
        args = canonicalize_args(name, args)

        missing = missing_required(name, args)
        if missing:
            raise ValueError(
                f"Missing required args for tool '{name}': {missing}. "
                f"Provided: {list(args.keys())}"
            )

        # inject shared handles
        args.setdefault("con", ctx["__con__"])
        args.setdefault("inventory_df", ctx["__frames__"]["inventory_df"])
        args.setdefault("transaction_df", ctx["__frames__"]["transaction_df"])

        res = fn(**args)

        # auto-apply: if the tool returned updated DataFrame(s), refresh the context and DuckDB
        mutated = False
        if isinstance(res, dict):
            if "inventory_df" in res and isinstance(res["inventory_df"], pd.DataFrame):
                ctx["__frames__"]["inventory_df"] = res["inventory_df"]
                ctx["__con__"].unregister("inventory_df")
                ctx["__con__"].register("inventory_df", res["inventory_df"])
                mutated = True
            if "transaction_df" in res and isinstance(res["transaction_df"], pd.DataFrame):
                ctx["__frames__"]["transaction_df"] = res["transaction_df"]
                ctx["__con__"].unregister("transaction_df")
                ctx["__con__"].register("transaction_df", res["transaction_df"])
                mutated = True

        ctx[rkey] = res
        results[rkey] = res
        if mutated:
            results[rkey]["__applied__"] = True
    return results


def run_tool_validation(v: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    name = v.get("name", "validation")
    tname = v.get("use_tool")
    fn = TOOL_REGISTRY.get(tname)
    if not fn:
        return {"name": name, "ok": False, "error": f"unknown_tool:{tname}"}

    raw_args = v.get("args", {})
    args = resolve_args(raw_args, ctx)
    args = canonicalize_args(tname, args)

    missing = missing_required(tname, args)
    if missing:
        return {
            "name": name,
            "ok": False,
            "error": f"missing_required_args:{tname}:{missing}",
            "provided_keys": list(args.keys()),
        }

    args.setdefault("con", ctx["__con__"])
    args.setdefault("inventory_df", ctx["__frames__"]["inventory_df"])
    args.setdefault("transaction_df", ctx["__frames__"]["transaction_df"])

    res = fn(**args)
    ok = bool(res.get("ok", True))
    return {"name": name, "ok": ok, "result": res}

