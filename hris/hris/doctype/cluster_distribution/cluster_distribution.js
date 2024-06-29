// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cluster Distribution', {
	refresh: function(frm) {


		frm.set_query("debit_account", function(doc) {
			return {
				filters: {
					'company': doc.company,
					'root_type': ["in", ["Expense"]],
					'is_group': 0
				}
			}
		});

		frm.set_query("credit_account", function(doc) {
			return {
				filters: {
					'company': doc.company,
					'root_type': ["in", ["Liability"]],
					'is_group': 0
				}
			}
		});

	}
});
