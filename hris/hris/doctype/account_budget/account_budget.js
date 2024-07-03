// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account Budget', {
	onload(frm) {
		if(frm.doc.__islocal) {
			return frm.call('get_months').then(() => {
				frm.refresh_field('distribution');
			});
		}
	},

	refresh(frm) {

		frm.set_query("account", function(doc) {
			return {
				filters: {
					'company': doc.company,
					'is_group': 0
				}
			}
		})
	},

	
});
