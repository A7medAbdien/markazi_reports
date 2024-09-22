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
            // checkIfMismatched(frm);
            checkIfMismatchedClient(frm);
        }
    },
    refresh(frm) {
        if (frm.is_new()) {
            frm.toggle_display("custom_mismatching_", false);
        } else {
            // checkIfMismatched(frm);
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
    frm.toggle_display("custom_mismatching_", true);
    var missMatchItems = items.map((item) => {
        if (item.rate != item.price_list_rate) {
            return item;
        }
    });
    frm.set_value("custom_mismatching_table", missMatchItems);
    changeMismatchedSectionColor(frm);
};

const checkIfMismatched = (frm) => {
    frappe.call({
        method: "markazi_reports.markazi_reports.doctype.markazi_reports.events.get_missmatched_items",
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
    const color = "#ff9696"; // #f57a7a
    frm.fields_dict["custom_mismatching_"].wrapper.css(
        "background-color",
        color
    );
};
