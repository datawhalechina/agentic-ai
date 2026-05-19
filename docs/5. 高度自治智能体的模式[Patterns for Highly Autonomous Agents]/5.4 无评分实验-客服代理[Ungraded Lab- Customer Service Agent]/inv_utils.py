# ==== Imports ====
from typing import Any
import random
from datetime import datetime
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# Initialize TinyDB
db = TinyDB("store_db.json")
inventory_table = db.table("inventory")
transactions_table = db.table("transactions")


def create_inventory():
    """
    Create and store the initial sunglasses inventory in TinyDB.
    Each item has name, item_id, description, quantity_in_stock, and price.
    """
    random.seed(42)

    sunglasses_data = [
        {
            "item_id": "SG001",
            "name": "Aviator",
            "description": "Originally designed for pilots, these teardrop-shaped lenses with thin metal frames offer timeless appeal. The large lenses provide excellent coverage while the lightweight construction ensures comfort during long wear.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 80
        },
        {
            "item_id": "SG002",
            "name": "Wayfarer",
            "description": "Featuring thick, angular frames that make a statement, these sunglasses combine retro charm with modern edge. The rectangular lenses and sturdy acetate construction create a confident look.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 95
        },
        {
            "item_id": "SG003",
            "name": "Mystique",
            "description": "Inspired by 1950s glamour, these frames sweep upward at the outer corners to create an elegant, feminine silhouette. The subtle curves and often embellished temples add sophistication to any outfit.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 70
        },
        {
            "item_id": "SG004",
            "name": "Sport",
            "description": "Designed for active lifestyles, these wraparound sunglasses feature a single curved lens that provides maximum coverage and wind protection. The lightweight, flexible frames include rubber grips.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 110
        },
        {
            "item_id": "SG005",
            "name": "Classic",   # renamed from "Round"
            "description": "Classic round profile with minimalist metal frames, offering a timeless and versatile style that fits both casual and formal wear.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 60  # under $100
        },
        {
            "item_id": "SG006",
            "name": "Moon",  # new entry
            "description": "Oversized round style with bold plastic frames, evoking retro aesthetics with a modern twist.",
            "quantity_in_stock": random.randint(3, 25),
            "price": 120  # over $100
        }
    ]

    inventory_table.truncate()
    inventory_table.insert_multiple(sunglasses_data)
    return sunglasses_data


def create_transactions(opening_balance=500.00):
    """
    Create and store the initial transactions in TinyDB.
    Includes the daily opening balance.
    """
    opening_transaction = {
        "transaction_id": "TXN001",
        "customer_name": "OPENING_BALANCE",
        "transaction_summary": "Daily opening register balance",
        "transaction_amount": opening_balance,
        "balance_after_transaction": opening_balance,
        "timestamp": datetime.now().isoformat()
    }

    transactions_table.truncate()
    transactions_table.insert(opening_transaction)
    return opening_transaction


def seed_db(db_path="store_db.json"):
    db = TinyDB(db_path)
    inventory_table = db.table("inventory")
    transactions_table = db.table("transactions")
    create_inventory()       # llena inventory_table
    create_transactions()    # llena transactions_table
    return db, inventory_table, transactions_table


# ==== Schema helpers for TinyDB ====
def _shorten(v: Any, n: int = 60) -> str:
    s = str(v)
    return s if len(s) <= n else s[:n-1] + "…"


def infer_type(value: Any) -> str:
    """Infer a simple type string from a Python value."""
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    return "string"


def build_schema_for_table(tbl, table_name: str, k: int = 3) -> str:
    rows = tbl.all()
    if not rows:
        return f"TABLE: {table_name} (empty)"
    
    # Infer simple types + take some examples
    schema = {}
    for r in rows:
        for k_, v in r.items():
            if k_ not in schema:
                schema[k_] = {"type": type(v).__name__, "examples": []}
            if len(schema[k_]["examples"]) < k and v not in schema[k_]["examples"]:
                schema[k_]["examples"].append(str(v))

    lines = [f"TABLE: {table_name}", "COLUMNS:"]
    for col, info in schema.items():
        ex = f" | examples: {info['examples']}" if info["examples"] else ""
        lines.append(f"  - {col}: {info['type']}{ex}")
    lines.append(f"ROWS: {len(rows)}")
    lines.append(f"PREVIEW (first 3 rows): {rows}")
    return "\n".join(lines)


def build_schema_block(inventory_tbl, transactions_tbl) -> str:
    inv = build_schema_for_table(inventory_tbl, "inventory_tbl")
    tx = build_schema_for_table(transactions_tbl, "transactions_tbl")
    notes = (
        "NOTES:\n"
        "- inventory_tbl.price is in USD.\n"
        "- inventory_tbl.quantity_in_stock > 0 means available stock.\n"
        "- inventory_tbl.name describes the style (e.g., 'Classic', 'Moon').\n"
        "- transactions_tbl.timestamp is ISO-8601.\n"
    )
    return f"{inv}\n\n{tx}\n\n{notes}"


# ==== Helpers for transactions ====
def get_current_balance(transactions_tbl, default: float = 0.0) -> float:
    txns = transactions_tbl.all()
    return txns[-1].get("balance_after_transaction", default) if txns else default


def next_transaction_id(transactions_tbl, prefix: str = "TXN") -> str:
    return f"{prefix}{len(transactions_tbl)+1:03d}"
