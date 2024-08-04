// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

const changeRowColor = () => {
    const color = "#f57a7a";

    // Get all rows in the report table
    const rows = document.querySelectorAll(".dt-row");

    rows.forEach((row) => {
        // Find the cell value in the specific column
        const rowCells = row.querySelectorAll(".dt-cell");
        const actualMarginCell = rowCells[rowCells.length - 1];

        if (actualMarginCell) {
            if (actualMarginCell.innerText === "1") {
                rowCells.forEach((cell) => {
                    cell.style.backgroundColor = color;
                    row.querySelectorAll("div").forEach((div) => {
                        div.style.backgroundColor = color;
                    });
                });
                row.style.backgroundColor = color;
            }
        }
    });
};

frappe.query_reports["Sales Valuation Past"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1,
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            // default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            // reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            // default: frappe.datetime.get_today(),
            // reqd: 1,
        },
    ],
    onload: function (report) {
        report.page.add_inner_button("Highlight", () => changeRowColor());
        report.page.change_inner_button_type("Highlight", null, "primary");
    },
};
