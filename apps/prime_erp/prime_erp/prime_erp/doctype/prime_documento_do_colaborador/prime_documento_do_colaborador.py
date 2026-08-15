import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, add_days, now_datetime

class PrimeDocumentodoColaborador(Document):
    def validate(self):
        self.calcular_status_validade()
        self.tratar_auditoria_aprovacao()

    def calcular_status_validade(self):
        if self.nao_expira:
            self.status_validade = "Não se Aplica"
            self.data_validade = None
            return

        if not self.data_validade:
            self.status_validade = "Não se Aplica"
            return

        hoje = getdate(nowdate())
        validade = getdate(self.data_validade)
        alerta_dias = add_days(hoje, 30)

        if validade < hoje:
            self.status_validade = "Vencido"
        elif validade <= alerta_dias:
            self.status_validade = "A Vencer"
        else:
            self.status_validade = "Válido"

    def tratar_auditoria_aprovacao(self):
        if self.status_aprovacao in ["Aprovado", "Rejeitado"]:
            if not self.validado_por:
                self.validado_por = frappe.session.user
                self.data_validacao = now_datetime()
        elif self.status_aprovacao == "Pendente":
            self.validado_por = None
            self.data_validacao = None
