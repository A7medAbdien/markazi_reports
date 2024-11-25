# Copyright (c) 2024, A.G and contributors
# For license information, please see license.txt

import frappe
from markazi_reports.markazi_reports.utils.AttrDict import AttrDict
from markazi_reports.markazi_reports.report.sales_valuation_past.sales_valuation_past import (
    get_product_bundles,
    get_calculated_product_bundels,
)
from datetime import datetime, timedelta


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "name",
            "label": "Item Code",
            "fieldtype": "Link",
            "options": "Product Bundle",
            "width": 0,
        },
        {
            "fieldname": "parent_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "width": 0,
        },
        {
            "fieldname": "cost",
            "label": "Avg Cost",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "s_price",
            "label": "Suggested Price",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "t_cut",
            "label": "tMart 33%",
            "fieldtype": "Float",
            "width": 0,
        },
        #        {
        #            "fieldname": "price",
        #            "label": "Final Price",
        #            "fieldtype": "Float",
        #            "width": 0,
        #        },
        # {
        #     "fieldname": "price_check",
        #     "label": "Price Check",
        #     "fieldtype": "Int",
        #     "width": 0,
        # },
        {
            "fieldname": "gross_profit",
            "label": "GP",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "gross_profit_p",
            "label": "GP%",
            "fieldtype": "Percent",
            "width": 0,
        },
        {
            "fieldname": "bep",
            "label": "Break Even Price",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "net_profit",
            "label": "NP",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "net_profit_p",
            "label": "NP%",
            "fieldtype": "Percent",
            "width": 0,
        },
        {
            "fieldname": "bem",
            "label": "Break Even Margin 10%",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "actual_margin",
            "label": "Actual Margin",
            "fieldtype": "Int",
            "width": 0,
        },
    ]


def get_data(filters):
    # Calculate default values
    today = datetime.today().date()  # Current date
    week_before_today = today - timedelta(days=7)  # A week before today

    # Set default values if not already provided
    filters["from_date"] = filters.get("from_date", week_before_today)
    filters["to_date"] = filters.get("to_date", today)

    is_timestamp = filters.get("from_date") and filters.get("to_date")
    filtered_cost = filters.get("cost") if filters.get("cost") else -1
    if is_timestamp:
        product_bundles = [
            AttrDict(item) for item in get_calculated_product_bundels(filters)
        ]
    else:
        product_bundles = get_product_bundles()

    def calculate_row(row):
        cost = row.cost
        s_price = cost * 2
        t_cut = s_price * 0.33
        gross_profit = s_price - cost
        gross_profit_p = (gross_profit / cost * 100) if cost else 0
        bep = cost * 1.67
        net_profit = gross_profit - t_cut
        net_profit_p = (net_profit / cost * 100) if cost else 0
        bem = cost * 0.1  # Break-even Margin
        actual_margin = 1 if net_profit > bem else 0

        return {
            "name": row.name,
            "parent_name": row.parent_name,
            "cost": cost,
            "s_price": s_price,
            "t_cut": t_cut,
            "bem": bem,
            "bep": bep,
            "gross_profit": gross_profit,
            "gross_profit_p": gross_profit_p,
            "net_profit": net_profit,
            "net_profit_p": net_profit_p,
            "breack_even_margin": bem,
            "actual_margin": actual_margin,
        }

    return [calculate_row(row) for row in product_bundles if row.cost > filtered_cost]
