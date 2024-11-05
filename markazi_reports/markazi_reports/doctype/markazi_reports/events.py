import frappe

company_list = ["Key Al Markazi"]
customer_list = [
    "DH STORE BAHRAIN WLL TM3 SEGAYA",
    "DH STORE BAHRAIN WLL TM6 SEEF",
    "DH STORE BAHRAIN WLL TM5 SAAR",
    "DH STORE BAHRAIN WLL TM4 REEF",
    "DH STORE BAHRAIN WLL TM2 HAJIYAT",
    "DH STORE BAHRAIN WLL TM1 GALALI",
]


def on_sales_invoice_validate(doc, event):
    print("\n\n\n  on_sales_invoice_validate")
    # if (doc.company not in company_list) or (doc.customer not in customer_list):
    #     return
    set_price_latest_list(doc)


def on_sales_invoice_submit(doc, envnt):
    # it updates product bundle and shows woring
    # if id did not find a prodct pundle for this item
    # for the companies in companies list
    if doc.company not in company_list:
        return
    update_product_bundle_on_sales(doc)


def on_submit_stock_ledger(doc, event):
    if doc.company not in company_list:
        return
    update_product_bundle_cost(doc)


def update_product_bundle_on_sales(doc):
    print("\n\n\n  update_product_bundle_on_sales")
    for item in doc.items:
        try:
            product_bundle_doc = frappe.get_doc("Product Bundle", item.item_code)
        except frappe.DoesNotExistError:
            frappe.throw(f"{item.item_code} does not have a product bundle")

        product_bundle_doc.custom_parent_name = item.item_name
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


# runs on submit stock entery
def update_product_bundle_cost(doc):
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
        fields=["name", "item_code", "custom_valuation_rate", "parent"],
        filters={"item_code": item_code},
    )

    for bundle_item in product_bundles_items:
        # get full doc and take the avg
        bundle_item_doc = frappe.get_doc("Product Bundle Item", bundle_item.name)
        # print(bundle_item.valuation_rate, valuation_rate)
        new_valuation_rate = (
            valuation_rate + bundle_item_doc.custom_valuation_rate
        ) / 2
        bundle_item_doc.custom_valuation_rate = new_valuation_rate
        # print(bundle_item_doc.valuation_rate)
        bundle_item_doc.save()

        # get its parent / product bundle
        product_bundle_doc = frappe.get_doc("Product Bundle", bundle_item_doc.parent)

        cost = 0
        for item in product_bundle_doc.items:
            cost += item.custom_valuation_rate
        product_bundle_doc.custom_cost = cost
        product_bundle_doc.save()

    frappe.db.commit()
    print(f"\n\n\n Item from custom app \n\n\n")
    print(product_bundles_items)


def set_price_latest_list(doc):
    price_list = get_last_price_list()
    print("\n\n\n")
    print(price_list)
    if price_list is None:
        frappe.throw("No price list found")
        return
    print("\n\n\n")
    print(doc.items[0])
    for items in doc.items:
        price = get_item_price(items.item_code, price_list.name)
        items.custom_latest_price_list_rate = price


def get_item_price(item_code, price_list_name):
    item_price_list_rate = frappe.db.get_value(
        doctype="Item Price",  # Corrected the doctype name if needed
        filters={"price_list": price_list_name, "item_code": item_code},
        fieldname="price_list_rate",
        as_dict=True,
    )

    # Debugging output
    print("\n\n\n")
    print(f"Price List: {price_list_name}, Item Code: {item_code}")
    print("Item Price List Rate:", item_price_list_rate)

    # Check if a rate was found
    if item_price_list_rate:
        return item_price_list_rate.get("price_list_rate")
    else:
        print("Price list rate not found.")
        return None


def get_last_price_list():
    # TODO: createa setting doctype and add thos to it
    trusted_users_to_create_price_list = ["Administrator", "ahmed.abdin@shahico.net"]
    price_list = frappe.get_last_doc(
        "Price List",
        filters={"selling": 1, "owner": ["in", trusted_users_to_create_price_list]},
    )
    return price_list
