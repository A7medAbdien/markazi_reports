// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Markazi Reports", {
// 	refresh(frm) {

// 	},
// });
const company_list = ["Key Al Markazi"]
const customer_list = [
    "DH STORE BAHRAIN WLL TM3 SEGAYA",
    "DH STORE BAHRAIN WLL TM6 SEEF",
    "DH STORE BAHRAIN WLL TM5 SAAR",
    "DH STORE BAHRAIN WLL TM4 REEF",
    "DH STORE BAHRAIN WLL TM2 HAJIYAT",
    "DH STORE BAHRAIN WLL TM1 GALALI",
]

frappe.ui.form.on("Sales Invoice", {
    // onload(frm) {
    //     if (frm.is_new()) {
    //         frm.toggle_display("custom_mismatching_", false);
    //     } else {
    //         checkMismatched(frm);
    //     }
    // },
    onload(frm) {
        frm.toggle_display("custom_mismatching_", false);
        if (frm.is_new()) {
        } else {
            // checkMismatched(frm);
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
    var missMatchItems = items.filter((item) => item.rate != item.price_list_rate);
    if (!missMatchItems || missMatchItems.length == 0) {
        frm.toggle_display("custom_mismatching_", false);
        return;
    } else {
        // if (frm.doc.arraysEqual(frm.doc))
        // frm.set_value("custom_mismatching_table", missMatchItems);
        frm.toggle_display("custom_mismatching_", true);
        changeMismatchedSectionColor(frm);
    }
};

const arraysEqual = (a1, a2) =>
    a1.length === a2.length && a1.every((o, idx) => objectsEqual(o, a2[idx]));

const objectsEqual = (o1, o2) =>
    typeof o1 === 'object' && Object.keys(o1).length > 0
        ? Object.keys(o1).length === Object.keys(o2).length
        && Object.keys(o1).every(p => objectsEqual(o1[p], o2[p]))
        : o1 === o2;

const changeMismatchedSectionColor = (frm) => {
    const color = "#ff9696"; // #f57a7a
    frm.fields_dict["custom_mismatching_"].wrapper.css(
        "background-color",
        color
    );
};
