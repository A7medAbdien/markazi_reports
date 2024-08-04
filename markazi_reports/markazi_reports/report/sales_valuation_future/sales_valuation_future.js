// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Valuation Future"] = {
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
        {
            fieldname: "cost",
            label: __("Avg Cost"),
            fieldtype: "Float",
            // default: frappe.datetime.get_today(),
            // reqd: 1,
        },
    ],
};