# Copyright (c) 2024, A.G and contributors
# For license information, please see license.txt

import frappe
from markazi_reports.markazi_reports.utils.list_dates import list_dates, week_ago, today


def execute(filters=None):
    columns = [
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 0,
        },
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "width": 0,
        },
        {
            "fieldname": "item_avg_cost",
            "label": "Avg Cost",
            "fieldtype": "Currancy",
            "width": 0,
        },
    ]

    # get purchse receipts
    prs = get_prs(filters)

    # extend columns with prs
    columns.extend([format_pr_to_col(pr) for pr in prs])

    # get Items of all prs {item_code(row): [{pr_name(col):,item_name(row):, item_rate(data):,}, ...]}
    item_details_dict = {}
    for pr in prs:
        item_details_dict = update_pr_item_details(pr, item_details_dict)

    # reformate data [{item_code:, item_name:, pr_name1:item_rate, pr_name2:, ...}, ...]
    data = format_data(item_details_dict)
    return columns, data


def format_data(item_details_dict):
    print("format_data")
    data = []
    for item_code, item_details in item_details_dict.items():
        row = {"item_code": item_code, "item_name": item_details[0]["item_name"]}
        total = 0
        for item_detail in item_details:
            total += item_detail["item_rate"]
            row[item_detail["pr_name"]] = item_detail["item_rate"]
        row["item_avg_cost"] = total / len(item_details)
        data.append(row)
    return data


def update_pr_item_details(pr, item_details_dict):
    print("update_pr_item_details")
    pr_all = frappe.get_doc("Purchase Receipt", pr["name"])
    print(pr_all)
    pr_items = pr_all.get("items")
    for item in pr_items:
        item_detail = {
            "item_name": item.get("item_name"),
            "item_rate": item.get("rate"),
            "pr_name": pr["name"],
        }
        try:
            item_details_dict[item.get("item_code")].append(item_detail)
        except KeyError:
            item_details_dict[item.get("item_code")] = [item_detail]
    return item_details_dict


def get_prs(filters):
    start_dt = filters.get("from_date") or week_ago()
    end_dt = filters.get("to_date") or today()
    supplier = filters.get("supplier") or ["!=", ""]

    prs = frappe.db.get_list(
        "Purchase Receipt",
        fields=["name", "posting_date", "supplier"],
        order_by="posting_date desc",
        filters={
            # "company": "Key Al Markazi",
            "posting_date": ("in", list_dates(start_dt, end_dt)),
            "status": "Completed",
            "supplier": supplier,
        },
    )
    return prs


# formate the pr to columns
def format_pr_to_col(pr):
    return {
        "fieldname": str(pr.name),
        "label": f"{str(pr.supplier)} / {str(pr.posting_date)}",
        "fieldtype": "Currancy",
        "width": 0,
    }
