// Copyright (c) 2024, ahmed.g.abdien and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Valuation"] = {
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
            default: frappe.datetime.add_months(
                frappe.datetime.get_today(),
                -1
            ),
            reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1,
        },
        {
            fieldname: "supplier",
            label: __("Supplier"),
            fieldtype: "Link",
            options: "Supplier",
            // get_query: function () {
            //   const company = frappe.query_report.get_filter_value("company");
            //   return {
            //     filters: { company: company },
            //   };
            // },
        },
    ],
};
