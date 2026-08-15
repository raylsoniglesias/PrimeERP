frappe.ui.form.on("Prime Documento do Colaborador", {
    refresh: function(frm) {
        if (frm.doc.status_validade === "Vencido") {
            frm.dashboard.set_headline_alert(__("Atenção: Este documento está VENCIDO!"), "red");
        } else if (frm.doc.status_validade === "A Vencer") {
            frm.dashboard.set_headline_alert(__("Atenção: Este documento vence nos próximos 30 dias."), "orange");
        } else if (frm.doc.status_validade === "Válido") {
            frm.dashboard.set_headline_alert(__("Documento Válido."), "green");
        }
    },
    nao_expira: function(frm) {
        if (frm.doc.nao_expira) {
            frm.set_value("data_validade", "");
        }
    }
});