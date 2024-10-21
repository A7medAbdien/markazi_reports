// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Markazi Reports", {
// 	refresh(frm) {

// 	},
// });
const company_list = ["Key Al Markazi"]

frappe.ui.form.on("Sales Invoice", {
    onload(frm) {
        if (frm.is_new()) {
            frm.toggle_display("custom_mismatching_", false);
        } else {
            if (frm.doc.company && company_list.includes(frm.doc.company))
                checkIfMismatchedClient(frm);
        }
    },
    refresh(frm) {
        if (frm.is_new()) {
            frm.toggle_display("custom_mismatching_", false);
        } else {
            if (frm.doc.company && company_list.includes(frm.doc.company))
                checkIfMismatchedClient(frm);
        }
    },
});

const checkIfMismatchedClient = (frm) => {
    var items = frm.doc.items;
    if (items.length == 0) {
        frm.toggle_display("custom_mismatching_", false);
        return;
    }
    var missMatchItems = items.filter((item) => item.rate != item.price_list_rate);
    if (!missMatchItems || missMatchItems.length == 0) {
        frm.toggle_display("custom_mismatching_", false);
        return;
    } else {
        frm.set_value("custom_mismatching_table", missMatchItems);
        frm.toggle_display("custom_mismatching_", true);
        changeMismatchedSectionColor(frm);
    }
};

const changeMismatchedSectionColor = (frm) => {
    const color = "#ff9696"; // #f57a7a
    frm.fields_dict["custom_mismatching_"].wrapper.css(
        "background-color",
        color
    );
};
