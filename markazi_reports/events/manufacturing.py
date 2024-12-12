import frappe
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry


def on_validate_work_order(doc, _):
    # print(f"\n\n\n {doc.company} \n\n\n")

    # consider only allowed companies
    markazi_settings = frappe.get_doc("Markazi Settings")
    allowed_companies = [
        company.company for company in markazi_settings.allowed_companies]
    if (doc.company not in allowed_companies):
        return
    # print(f"\n\n\n {doc.company} \n\n\n")

    # set nessessary values and submit Work Order
    frappe.db.set_value("Work Order", doc.name, "skip_transfer", 1)
    frappe.db.set_value("Work Order", doc.name, "allow_alternative_item", 1)
    frappe.db.set_value("Work Order", doc.name, "docstatus", 1)
    frappe.db.set_value("Work Order", doc.name, "status", "Completed")
    frappe.db.commit()

    # get items out of stock
    work_order_items = doc.required_items
    items_out_of_stock = list(filter(
        lambda item: item.available_qty_at_source_warehouse < item.required_qty,
        work_order_items
    ))
    # print(f"\n\n\n {items_out_of_stock} \n\n\n")

    # make stock entry and save it
    stock_entry = make_stock_entry(doc.name, "Manufacture", doc.qty)
    stock_entry = frappe.get_doc(stock_entry)
    stock_entry.save()
    # print(f"\n\n\n stock_entry {stock_entry} \n\n\n")

    # submit stock entry if no items out of stock
    if (len(items_out_of_stock) == 0):
        stock_entry.submit()

    # print(f"\n\n\n {doc.as_dict()} \n\n\n")
    # print("on_validate_work_order")
