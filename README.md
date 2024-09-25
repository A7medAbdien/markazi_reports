## Markazi Reports

Markazi Reports

#### License

mit

## Installation

```sh
bench get-app https://github.com/A7medAbdien/markazi_reports.git
bench --site erpnextv15.local install-app markazi_reports
```

```sh
### App Versions
```

{
"erpnext": "15.36.1",
"frappe": "15.41.0",
"hrms": "15.29.0",
"ka_vehicle_maintenance": "0.0.1",
"ksa": "0.0.1",
"markazi_reports": "0.0.1",
"payments": "0.0.1",
"taxjar_integration": "0.0.1"
}

```
### Route
```

query-report/Sales Valuation Past

```
### Traceback
```

Traceback (most recent call last):
File "apps/frappe/frappe/app.py", line 114, in application
response = frappe.api.handle(request)
File "apps/frappe/frappe/api/**init**.py", line 49, in handle
data = endpoint(**arguments)
File "apps/frappe/frappe/api/v1.py", line 36, in handle_rpc_call
return frappe.handler.handle()
File "apps/frappe/frappe/handler.py", line 49, in handle
data = execute_cmd(cmd)
File "apps/frappe/frappe/handler.py", line 85, in execute_cmd
return frappe.call(method, **frappe.form_dict)
File "apps/frappe/frappe/**init**.py", line 1775, in call
return fn(*args, \*\*newargs)
File "apps/frappe/frappe/utils/typing_validations.py", line 31, in wrapper
return func(*args, **kwargs)
File "apps/frappe/frappe/**init**.py", line 928, in wrapper_fn
retval = fn(\*args, **get_newargs(fn, kwargs))
File "apps/frappe/frappe/desk/query_report.py", line 223, in run
result = generate_report_result(report, filters, user, custom_columns, is_tree, parent_field)
File "apps/frappe/frappe/**init**.py", line 928, in wrapper_fn
retval = fn(*args, \*\*get_newargs(fn, kwargs))
File "apps/frappe/frappe/desk/query_report.py", line 84, in generate_report_result
res = get_report_result(report, filters) or []
File "apps/frappe/frappe/desk/query_report.py", line 65, in get_report_result
res = report.execute_script_report(filters)
File "apps/frappe/frappe/core/doctype/report/report.py", line 163, in execute_script_report
res = self.execute_module(filters)
File "apps/frappe/frappe/core/doctype/report/report.py", line 180, in execute_module
return frappe.get_attr(method_name)(frappe.\_dict(filters))
File "apps/markazi_reports/markazi_reports/markazi_reports/report/sales_valuation_past/sales_valuation_past.py", line 92, in execute
product_bundles = get_product_bundles()
File "apps/markazi_reports/markazi_reports/markazi_reports/report/sales_valuation_past/sales_valuation_past.py", line 120, in get_product_bundles
return frappe.get_all(
File "apps/frappe/frappe/**init**.py", line 2064, in get_all
return get_list(doctype, *args, **kwargs)
File "apps/frappe/frappe/**init**.py", line 2039, in get_list
return frappe.model.db_query.DatabaseQuery(doctype).execute(\*args, **kwargs)
File "apps/frappe/frappe/model/db_query.py", line 191, in execute
result = self.build_and_run()
File "apps/frappe/frappe/model/db_query.py", line 232, in build_and_run
return frappe.db.sql(
File "apps/frappe/frappe/database/database.py", line 227, in sql
self.\_cursor.execute(query, values)
File "env/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
result = self.\_query(query)
File "env/lib/python3.10/site-packages/pymysql/cursors.py", line 322, in \_query
conn.query(q)
File "env/lib/python3.10/site-packages/pymysql/connections.py", line 563, in query
self.\_affected_rows = self.\_read_query_result(unbuffered=unbuffered)
File "env/lib/python3.10/site-packages/pymysql/connections.py", line 825, in \_read_query_result
result.read()
File "env/lib/python3.10/site-packages/pymysql/connections.py", line 1199, in read
first_packet = self.connection.\_read_packet()
File "env/lib/python3.10/site-packages/pymysql/connections.py", line 775, in \_read_packet
packet.raise_for_error()
File "env/lib/python3.10/site-packages/pymysql/protocol.py", line 219, in raise_for_error
err.raise_mysql_exception(self.\_data)
File "env/lib/python3.10/site-packages/pymysql/err.py", line 150, in raise_mysql_exception
raise errorclass(errno, errval)
pymysql.err.OperationalError: (1054, "Unknown column 'parent_name' in 'field list'")

```
### Request Data
```

{
"type": "GET",
"args": {
"report_name": "Sales Valuation Past",
"filters": "{\"company\":\"Key Al Markazi\"}",
"ignore_prepared_report": false,
"are_default_filters": true
},
"headers": {},
"error_handlers": {},
"url": "/api/method/frappe.desk.query_report.run",
"request_id": null
}

```
### Response Data
```

{
"exception": "pymysql.err.OperationalError: (1054, \"Unknown column 'parent_name' in 'field list'\")",
"exc_type": "OperationalError",
"\_exc_source": "markazi_reports (app)"
}

```

```
