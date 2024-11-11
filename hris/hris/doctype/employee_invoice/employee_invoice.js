// Copyright (c) 2024, RAFI and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Invoice', {
	
	employee: function(frm) {
		frm.add_fetch("employee", "ctc", "salary_amount");
	},
});
