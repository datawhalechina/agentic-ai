"""Offline tests using TinyDB and the notebook's actual Agent functions."""

import ast
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import traceback
from types import SimpleNamespace
from typing import Any, Dict, Optional
import unittest
from unittest.mock import Mock

from tinydb import Query, TinyDB


LAB = Path(__file__).resolve().parents[1]


class InventoryDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        original_cwd = Path.cwd()
        os.chdir(self.temp_dir.name)
        self.addCleanup(os.chdir, original_cwd)
        spec = importlib.util.spec_from_file_location("inv_utils", LAB / "inv_utils.py")
        self.inv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.inv)
        self.addCleanup(self.inv.db.close)

    def track_database(self, db):
        self.addCleanup(db.close)
        return db

    def notebook_agent(self):
        # Compile the shipped definitions, without running API/config/demo cells.
        notebook = json.loads((LAB / "M5_UGL_1_R.ipynb").read_text(encoding="utf-8"))
        wanted = {
            "generate_llm_code", "_extract_execute_block",
            "execute_generated_code", "customer_service_agent",
        }
        definitions = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            for node in ast.parse("".join(cell["source"])).body:
                if isinstance(node, ast.FunctionDef) and node.name in wanted:
                    definitions.append(node)
                elif isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "PROMPT"
                    for target in node.targets
                ):
                    definitions.append(node)
        self.assertEqual(
            {node.name for node in definitions if isinstance(node, ast.FunctionDef)},
            wanted,
        )
        content = (
            "<execute_python>\n"
            "answer_text = str(inventory_tbl.search(Query().item_id == 'SG001')"
            "[0]['quantity_in_stock'])\n"
            "</execute_python>"
        )
        create = Mock(return_value=SimpleNamespace(choices=[
            SimpleNamespace(message=SimpleNamespace(content=content))
        ]))
        namespace = {
            "Any": Any, "Dict": Dict, "Optional": Optional, "Query": Query,
            "io": io, "json": json, "re": re, "sys": sys, "traceback": traceback,
            "inv_utils": self.inv, "utils": SimpleNamespace(print_html=Mock()),
            "client": SimpleNamespace(chat=SimpleNamespace(
                completions=SimpleNamespace(create=create)
            )),
        }
        exec(compile(ast.Module(body=definitions, type_ignores=[]), str(LAB / "M5_UGL_1_R.ipynb"), "exec"), namespace)
        return namespace["customer_service_agent"], create

    def test_seed_custom_path_populates_requested_database_only(self):
        self.inv.inventory_table.insert({"item_id": "KEEP"})
        self.inv.transactions_table.insert({"transaction_id": "KEEP"})
        default_before = Path("store_db.json").read_bytes()

        db, inventory, transactions = self.inv.seed_db("other_store.json")
        self.track_database(db)

        self.assertEqual(len(inventory), 6)
        self.assertEqual(inventory.get(Query().item_id == "SG001")["quantity_in_stock"], 23)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions.all()[0]["balance_after_transaction"], 500.0)
        self.assertEqual(Path("store_db.json").read_bytes(), default_before)
        # Confirm the returned tables and on-disk data refer to the same database.
        reopened = self.track_database(TinyDB("other_store.json"))
        self.assertEqual(reopened.table("inventory").all(), inventory.all())

    def exercise_reseed(self, db, inventory, transactions):
        inventory.truncate()
        inventory.insert({"item_id": "SG001", "quantity_in_stock": 1})
        transactions.truncate()
        transactions.insert({"transaction_id": "OLD", "balance_after_transaction": 1})
        # Warm the selected table's real TinyDB query cache before resetting it.
        self.assertEqual(inventory.search(Query().item_id == "SG001")[0]["quantity_in_stock"], 1)
        agent, create = self.notebook_agent()
        result = agent("Check Aviator stock", db=db, inventory_tbl=inventory,
                       transactions_tbl=transactions, reseed=True)

        self.assertIsNone(result["exec"]["error"])
        self.assertEqual(result["exec"]["answer"], "23")
        self.assertEqual(len(result["exec"]["inventory_after"]), 6)
        self.assertEqual(len(result["exec"]["transactions_after"]), 1)
        self.assertEqual(transactions.all()[0]["balance_after_transaction"], 500.0)
        create.assert_called_once()
        self.assertIn("ROWS: 6", create.call_args.kwargs["messages"][1]["content"])

    def test_notebook_reseed_uses_selected_database(self):
        self.inv.inventory_table.insert({"item_id": "KEEP"})
        self.inv.transactions_table.insert({"transaction_id": "KEEP"})
        default_before = Path("store_db.json").read_bytes()
        db = self.track_database(TinyDB("other_store.json"))

        self.exercise_reseed(db, db.table("inventory"), db.table("transactions"))

        self.assertEqual(Path("store_db.json").read_bytes(), default_before)

    def test_notebook_reseed_invalidates_default_database_query_cache(self):
        db, inventory, transactions = self.inv.seed_db()
        self.track_database(db)
        self.exercise_reseed(db, inventory, transactions)

    def test_notebook_without_reseed_preserves_existing_data(self):
        db = self.track_database(TinyDB("other_store.json"))
        inventory, transactions = db.table("inventory"), db.table("transactions")
        inventory.insert({"item_id": "SG001", "quantity_in_stock": 1})
        transactions.insert({"transaction_id": "KEEP", "balance_after_transaction": 20})
        before = Path("other_store.json").read_bytes()
        agent, create = self.notebook_agent()

        result = agent("Check Aviator stock", db=db, inventory_tbl=inventory,
                       transactions_tbl=transactions)

        self.assertIsNone(result["exec"]["error"])
        self.assertEqual(result["exec"]["answer"], "1")
        self.assertEqual(Path("other_store.json").read_bytes(), before)
        create.assert_called_once()

    def test_legacy_seed_helpers_keep_default_table_and_balance_arguments(self):
        self.inv.create_inventory()
        self.inv.create_transactions(123.45)

        self.assertEqual(len(self.inv.inventory_table), 6)
        self.assertEqual(self.inv.transactions_table.all()[0]["balance_after_transaction"], 123.45)


if __name__ == "__main__":
    unittest.main()
