# Copyright (c) 2024, A.G and contributors
# For license information, please see license.txt

from dataclasses import fields
import frappe
from frappe.query_builder.functions import Avg, Sum
from markazi_reports.markazi_reports.utils.AttrDict import AttrDict


def execute(filters=None):
    columns, data = [], []

    columns = [
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
            "fieldname": "price",
            "label": "Price",
            "fieldtype": "Float",
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
            "fieldname": "t_cut",
            "label": "Cut (33%)",
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
            "fieldname": "breack_even_margin",
            "label": "Breack Even Margin 10%",
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

    is_timestamp = filters.get("from_date") and filters.get("to_date")
    filtred_cost = filters.get("cost")
    filtered_cost = filters.get("cost") if filters.get("cost") else -1

    if is_timestamp:
        product_bundles = [
            AttrDict(item) for item in get_calculated_product_bundels(filters)
        ]
    else:
        product_bundles = get_product_bundles()

    data = [
        {
            "name": row.name,
            "parent_name": row.parent_name,
            "cost": row.cost,
            "price": row.price,
            "gross_profit": (row.price - row.cost),
            "gross_profit_p": (row.price - row.cost) / row.cost if row.cost else 0,
            "t_cut": (row.price - row.cost) * 0.33,
            "net_profit": ((row.price - row.cost) * 0.77),
            "net_profit_p": (
                ((row.price - row.cost) * 0.77) / row.cost if row.cost else 0
            ),
            "breack_even_margin": row.cost * 0.1,
            "actual_margin": (
                1 if ((row.price - row.cost) * 0.77) > row.cost * 0.1 else 0
            ),
        }
        for row in product_bundles
        if row.cost > filtered_cost
    ]

    return columns, data


def get_product_bundles():
    pds_ = frappe.get_all(
        "Product Bundle",
        fields=["name", "custom_parent_name", "custom_cost", "custom_price"],
    )
    
    pds = [
        AttrDict({
            "name":pd.name,
            "parent_name": pd.custom_parnet_name,
            "cost": pd.custom_cost,
            "price": pd.custom_price
        })
        for pd in pds_
    ]
    return pds


def get_calculated_product_bundels(filters):
    procut_bundel = []
    # get sales invices
    sii = get_sales_invoice_items(filters)

    # fotmate sales invice items to product bundle
    procut_bundel = [
        {
            "name": row.item_code,
            "parent_name": row.item_name,
            "price": row.price,
            "cost": 0,
        }
        for row in sii
    ]

    # get purchase receipts
    pri = get_purchase_receipt_items(filters)

    # formate pruchase receipt items to product bundle
    for row in pri:
        for item in procut_bundel:
            if item["name"] == row.parent:
                item["cost"] = row.cost

    return procut_bundel


def get_sales_invoice_items(filters):
    sii = frappe.qb.DocType("Sales Invoice Item")
    si = frappe.qb.DocType("Sales Invoice")

    query = (
        frappe.qb.from_(si)
        .inner_join(sii)
        .on(si.name == sii.parent)
        .select(
            sii.item_code,
            sii.item_name,
            Avg(sii.rate).as_("price"),
        )
        .where(
            (si.docstatus == 1) & (si.posting_date[filters.from_date : filters.to_date])
        )
        .groupby(sii.item_code)
    )
    return query.run(as_dict=True)


def get_purchase_receipt_items(filters):
    pr = frappe.qb.DocType("Purchase Receipt")
    pri = frappe.qb.DocType("Purchase Receipt Item")
    pd = frappe.qb.DocType("Product Bundle Item")

    pri_query = (
        frappe.qb.from_(pr)
        .inner_join(pri)
        .on(pr.name == pri.parent)
        .select(
            pri.item_code,
            Avg(pri.rate).as_("rate"),
        )
        .where(
            (pr.docstatus == 1) & (pr.posting_date[filters.from_date : filters.to_date])
        )
        .groupby(pri.item_code)
    )

    query = (
        frappe.qb.from_(pri_query)
        .inner_join(pd)
        .on(pri_query.item_code == pd.item_code)
        .select(
            pd.parent,
            # pd.item_code,
            pd.qty,
            pri_query.rate,
            Sum(pd.qty * pri_query.rate).as_("cost"),
        )
        .groupby(pd.parent)
    )
    return query.run(as_dict=True)
