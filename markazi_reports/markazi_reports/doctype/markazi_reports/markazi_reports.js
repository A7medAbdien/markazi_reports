// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Markazi Reports", {
// 	refresh(frm) {

// 	},
// });
const company_list = ["Key Al Markazi", "happyDay"]
const customer_list = [
    "DH STORE BAHRAIN WLL TM3 SEGAYA",
    "DH STORE BAHRAIN WLL TM6 SEEF",
    "DH STORE BAHRAIN WLL TM5 SAAR",
    "DH STORE BAHRAIN WLL TM4 REEF",
    "DH STORE BAHRAIN WLL TM2 HAJIYAT",
    "DH STORE BAHRAIN WLL TM1 GALALI",
    "Test",
]

frappe.ui.form.on("Sales Invoice", {
    onload(frm) {
        frm.toggle_display("custom_mismatching_", false);
        if (!frm.is_new()) {
            checkMismatched(frm);
        }
    },
    after_save(frm) {
        frm.toggle_display("custom_mismatching_", false);
        if (!frm.is_new()) {
            checkMismatched(frm);
        }
    },
});

const checkMismatched = (frm) => {
    if (
        frm.doc.company && company_list.includes(frm.doc.company)
        && frm.doc.customer && customer_list.includes(frm.doc.customer)
        && !frm.doc.is_return
    )
        checkIfMismatchedClient(frm);
}

const checkIfMismatchedClient = (frm) => {
    var items = frm.doc.items;
    if (items.length == 0) {
        frm.toggle_display("custom_mismatching_", false);
        return;
    }

    var missMatchItems = items.filter((item) =>
        item.custom_latest_price_list_rate != 0 &&
        item.rate != item.custom_latest_price_list_rate
    );
    console.log(missMatchItems);

    if (!missMatchItems || missMatchItems.length == 0) {
        frm.toggle_display("custom_mismatching_", false);
        return;
    } else {
        frm.toggle_display("custom_mismatching_", true);
        changeMismatchedSectionColor(frm);
        console.log("m", missMatchItems);
        console.log("f", frm.doc.custom_mismatching_table);
        console.log(!arraysEqual(frm.doc.custom_mismatching_table, missMatchItems));

        if (!arraysEqual(frm.doc.custom_mismatching_table, missMatchItems))
            frm.set_value("custom_mismatching_table", missMatchItems);
    }
};

const changeMismatchedSectionColor = (frm) => {
    const color = "#ff9696"; // #f57a7a
    frm.fields_dict["custom_mismatching_"].wrapper.css(
        "background-color",
        color
    );
};

const arraysEqual = (current, saved) => {
    if (current.length != saved.length) return false;
    for (let i = 0; i < current.length; i++) {
        console.log({
            current: { ...current[i] },
            saved: { ...saved[i] },
            c: {
                item_code: current[i].item_code,
                rate: current[i].rate,
                qty: current[i].qty,
                amount: current[i].amount,
                item_tax_template: current[i].item_tax_template,
                custom_latest_price_list_rate: current[i].custom_latest_price_list_rate,
            },
            s: {
                item_code: saved[i].item_code,
                rate: saved[i].rate,
                qty: saved[i].qty,
                amount: saved[i].amount,
                item_tax_template: saved[i].item_tax_template,
                custom_latest_price_list_rate: saved[i].custom_latest_price_list_rate,
            },
        });

        if (
            current[i].item_code != saved[i].item_code ||
            current[i].rate != saved[i].rate ||
            current[i].qty != saved[i].qty ||
            current[i].amount != saved[i].amount ||
            current[i].item_tax_template != saved[i].item_tax_template ||
            current[i].price_list_rate != saved[i].price_list_rate ||
            current[i].custom_latest_price_list_rate != saved[i].custom_latest_price_list_rate
        )
            return false;
    }
    return true;
}
