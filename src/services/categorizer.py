import re

import pandas as pd


class TransactionCategorizer:
    CATEGORY_RULES = {
        'Inflow / Revenue': re.compile(r'(wynagrodzenie|pensja|salary|wpływ|przelew od)', re.IGNORECASE),
        'FMCG & Groceries': re.compile(r'(biedronka|lidl|auchan|kaufland|zabka|carrefour|freshmarket|stokrotka)', re.IGNORECASE),
        'Dining & Entertainment': re.compile(r'(mcdonalds|kfc|starbucks|pyszne|uber eats|wolt|restauracja|kawiarna|burger)', re.IGNORECASE),
        'Transportation & Travel': re.compile(r'(orlen|bp|shell|circle k|uber|bolt|jakdojade|pkp|bilet|mpk|ztm)', re.IGNORECASE),
        'SaaS & Subscriptions': re.compile(r'(netflix|spotify|hbo|amazon prime|disney|apple|gym|siłownia|karnet)', re.IGNORECASE),
        'Retail & E-commerce': re.compile(r'(allegro|zalando|ikea|media expert|rtv euro|zara|h&m|empik)', re.IGNORECASE),
        'Housing & Utilities': re.compile(r'(wynajem|czynsz|prąd|woda|gaz|internet|orange|play|t-mobile|plus)', re.IGNORECASE)
    }

    @classmethod
    def categorize_transaction(cls, description: str, amount: float) -> str:
        if amount > 0:
            return 'Inflow / Revenue'

        desc_str = str(description)

        for category, pattern in cls.CATEGORY_RULES.items():
            if pattern.search(desc_str):
                return category

        return 'Uncategorized Outflow'

    @classmethod
    def apply_categories(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['category'] = df.apply(
            lambda row: cls.categorize_transaction(row['description'], row['amount']),
            axis=1
        )
        return df
