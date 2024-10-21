import frappe


def on_sales_invoice_submit(doc, envnt):
    # it updates product bundle and shows woring
    # if id did not find a prodct pundle for this item
    # for the companies in companies list
    update_product_bundle_on_sales(doc, ["Key Al Markazi"])


def on_sales_invoice_validate(doc, envnt):
    # show_price_list_worning(doc)
    pass


def show_price_list_worning(doc):
    # doc here is sales invoice
    price_list = doc.selling_price_list
    print(f"\n\n\n  {price_list}")

    # item has price list
    item_price_not_match = []
    for item in doc.items:
        item_price = frappe.get_last_doc(
            "Item Price",
            {
                "item_code": item.item_code,
                "price_list": price_list,
                "selling": 1,
            },
        )
        if item.rate != item_price.price_list_rate:
            item_price_not_match.append(
                {
                    "item_name": item.item_name,
                    "item_code": item.item_code,
                    "price_list_rate": item.price_list_rate,
                    "rate": item.rate,
                }
            )

    if len(item_price_not_match) > 0:
        message = []
        for item in item_price_not_match:
            message.append(f"{item['item_code']}: {item['item_name']}")
        frappe.throw(title="Price list rate does not match", msg=message, as_list=True)


@frappe.whitelist()
def get_missmatched_items(doc_name):
    si = frappe.get_doc("Sales Invoice", doc_name)
    miss = []
    for sii in si.items:
        if sii.price_list_rate != sii.rate:
            miss.append(sii)

    si.custom_mismatching_table = miss
    print(si.custom_mismatching_table)
    return miss


@frappe.whitelist()
def update_item_prices(items):
    import json

    items = json.loads(items)
    print("\n\n\n")
    print(items)

    for item in items:
        item_doc = frappe.get_doc("Sales Invoice Item", item["name"])
        item_doc.price_list_rate = item["price_list_rate"]
        item_doc.rate = item["rate"]
        item_doc.save()

    return {"status": "success"}


def update_product_bundle_on_sales(doc, company_list):
    print("\n\n\n  update_product_bundle_on_sales")
    if doc.company not in company_list:
        return
    for item in doc.items:
        try:
            product_bundle_doc = frappe.get_doc("Product Bundle", item.item_code)
        except frappe.DoesNotExistError:
            frappe.throw(f"{item.item_code} does not have a product bundle")

        new_price = (item.rate + product_bundle_doc.custom_price) / 2
        new_gp = new_price - product_bundle_doc.custom_cost
        new_cut = 0
        if product_bundle_doc.custom_has_cut:
            new_cut = new_gp * product_bundle_doc.custom_cut_rate
        new_np = new_gp - new_cut

        product_bundle_doc.custom_price = new_price
        product_bundle_doc.custom_gp = new_gp
        product_bundle_doc.custom_cut = new_cut
        product_bundle_doc.custom_np = new_np
        product_bundle_doc.save()
        print("update_product_bundle_on_sales", product_bundle_doc.as_dict())
    print("\n\n\n")


def update_product_bundle_name(doc, event):
    item_code = doc.item_code
    item_name = doc.item_name
    product_bundle_name = frappe.get_doc(
        "Product Bundle",
        item_code,
        fields=["name", "custom_parent_name"],
    )
    product_bundle_name.custom_parent_name = item_name
    product_bundle_name.save()

    frappe.db.commit()


def update_product_bundle_cost(doc, event):
    stock_ledger_entry_type = doc.voucher_type
    print(f"\n\n\n Item from custom update_product_bundle_cost \n\n\n")
    print(stock_ledger_entry_type)

    # if not purchase leave
    if stock_ledger_entry_type != "Purchase Receipt":
        return

    item_code = doc.item_code
    valuation_rate = doc.incoming_rate
    print(valuation_rate)

    # get all product bundle items that this item was in, Parent
    product_bundles_items = frappe.get_all(
        "Product Bundle Item",
        fields=["name", "item_code", "valuation_rate", "parent"],
        filters={"item_code": item_code},
    )

    for bundle_item in product_bundles_items:
        # get full doc and take the avg
        bundle_item_doc = frappe.get_doc("Product Bundle Item", bundle_item.name)
        print(bundle_item.valuation_rate, valuation_rate)
        new_valuation_rate = (valuation_rate + bundle_item_doc.valuation_rate) / 2
        bundle_item_doc.valuation_rate = new_valuation_rate
        print(bundle_item_doc.valuation_rate)
        bundle_item_doc.save()

        # get its parent / product bundle
        product_bundle_doc = frappe.get_doc("Product Bundle", bundle_item_doc.parent)

        cost = 0
        for item in product_bundle_doc.items:
            cost += item.valuation_rate
        product_bundle_doc.custom_cost = cost
        product_bundle_doc.save()

    frappe.db.commit()
    print(f"\n\n\n Item from custom app \n\n\n")
    print(product_bundles_items)
