from unittest import TestCase

import pandas as pd

from src.services.categorizer import TransactionCategorizer


class TestCategorizer(TestCase):
    def test_income_categorization(self):
        # Even if description says "Biedronka", a positive amount should override
        # as it might be a refund.
        category = TransactionCategorizer.categorize_transaction("Zwrot Biedronka", 50.00)
        self.assertEqual(category, "Inflow / Revenue")

    def test_regex_matching(self):
        cat1 = TransactionCategorizer.categorize_transaction("Zakupy Auchan Waw", -120.50)
        self.assertEqual(cat1, "FMCG & Groceries")

        cat2 = TransactionCategorizer.categorize_transaction("Uber przejazd z wczoraj", -30.00)
        self.assertEqual(cat2, "Transportation & Travel")

    def test_case_insensitivity(self):
        cat = TransactionCategorizer.categorize_transaction("nEtFlIx SUBSCRIPTION", -45.00)
        self.assertEqual(cat, "SaaS & Subscriptions")

    def test_fallback_category(self):
        cat = TransactionCategorizer.categorize_transaction("Random Unmatched Name Corp", -10.00)
        self.assertEqual(cat, "Uncategorized Outflow")

    def test_apply_categories_dataframe(self):
        data = pd.DataFrame([
            {'description': 'WPLATA ZABKA', 'amount': -15.00},
            {'description': 'WYNAGRODZENIE', 'amount': 5000.00}
        ])

        result = TransactionCategorizer.apply_categories(data)

        self.assertTrue('category' in result.columns)
        self.assertEqual(result.iloc[0]['category'], 'FMCG & Groceries')
        self.assertEqual(result.iloc[1]['category'], 'Inflow / Revenue')
