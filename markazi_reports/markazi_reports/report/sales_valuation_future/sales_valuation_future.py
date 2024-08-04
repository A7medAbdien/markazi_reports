# Copyright (c) 2024, A.G and contributors
# For license information, please see license.txt

import frappe
from markazi_reports.markazi_reports.utils.AttrDict import AttrDict
from markazi_reports.markazi_reports.report.sales_valuation_past.sales_valuation_past import (
    get_product_bundles,
    get_calculated_product_bundels,
)


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
            "fieldname": "t_cut",
            "label": "tMart 33%",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "bem",
            "label": "Break Even Margin 10%",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "bep",
            "label": "Break Even Price",
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
            "fieldname": "price",
            "label": "Final Price",
            "fieldtype": "Float",
            "width": 0,
        },
        {
            "fieldname": "price_check",
            "label": "Price Check",
            "fieldtype": "Int",
            "width": 0,
        },
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
            "fieldname": "actual_margin",
            "label": "Actual Margin",
            "fieldtype": "Int",
            "width": 0,
        },
    ]


def get_data(filters):
    is_timestamp = filters.get("from_date") and filters.get("to_date")
    filtered_cost = filters.get("cost") if filters.get("cost") else -1
    if is_timestamp:
        product_bundles = [
            AttrDict(item) for item in get_calculated_product_bundels(filters)
        ]
    else:
        product_bundles = get_product_bundles()

    return [
        {
            "name": row.name,
            "parent_name": row.parent_name,
            "cost": row.cost,
            "t_cut": row.cost * 0.66,
            "bem": row.cost * 0.1,
            "bep": row.cost * 1.76,
            "s_price": row.cost * 2,
            "price": row.price,
            # "price_check": 1,
            # "gross_profit": (row.price - row.cost),
            # "gross_profit_p": (row.price - row.cost) / row.cost if row.cost else 0,
            # "net_profit": (row.price - row.cost) - (row.cost * 0.66),
            # "net_profit_p": (
            #     ((row.price - row.cost) - (row.cost * 0.66)) / row.cost
            #     if row.cost
            #     else 0
            # ),
            # "actual_margin": (
            #     1
            #     if ((row.cost * 0.1) > ((row.price - row.cost) - (row.cost * 0.66)))
            #     else 0
            # ),
        }
        for row in product_bundles
        if row.cost > filtered_cost
    ]
