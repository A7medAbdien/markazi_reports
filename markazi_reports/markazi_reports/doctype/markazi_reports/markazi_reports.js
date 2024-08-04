// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Markazi Reports", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Sales Invoice", {
    onload(frm) {
        // console.log("onload");
        if (frm.is_new()) {
            frm.toggle_display("custom_mismatching_", false);
        } else {
            checkIfMismatched(frm);
        }
    },
    refresh(frm) {
        // console.log("refresh");
        if (frm.is_new()) {
            frm.toggle_display("custom_mismatching_", false);
        } else {
            checkIfMismatched(frm);
        }
    },
});

const checkIfMismatched = (frm) => {
    frappe.call({
        method: "my_custom_app.my_custom_app.doctype.custom_stock_ledger.events.get_missmatched_items",
        args: {
            doc_name: frm.doc.name,
        },
        callback: (r) => {
            no_miss = r.message.length;
            // console.log(no_miss);
            if (no_miss > 0) {
                frm.toggle_display("custom_mismatching_", true);
                frm.doc.miss = r.message;
                changeMismatchedSectionColor(frm);
            } else frm.toggle_display("custom_mismatching_", false);
            refresh_field("custom_mismatching_");
        },
    });
};

const changeMismatchedSectionColor = (frm) => {
    const color = "#f57a7a";

    frm.fields_dict["custom_mismatching_"].wrapper.css(
        "background-color",
        color
    );
};
