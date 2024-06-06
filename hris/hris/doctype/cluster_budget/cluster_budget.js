// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cluster Budget', {
	onload(frm) {
		if(frm.doc.__islocal) {
			return frm.call('get_months').then(() => {
				frm.refresh_field('monthly_distribution');
			});
		}
	},
});
