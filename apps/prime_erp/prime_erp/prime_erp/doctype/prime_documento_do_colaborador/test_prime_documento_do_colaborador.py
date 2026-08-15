import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, nowdate

class TestPrimeDocumentodoColaborador(FrappeTestCase):
    def test_regras_validade_e_auditoria(self):
        doc = frappe.new_doc("Prime Documento do Colaborador")
        doc.tipo_documento = "DOC-TST"
        doc.anexo_documento = "/files/teste.pdf"
        
        # 1. Documento vencido
        doc.data_validade = add_days(nowdate(), -5)
        doc.nao_expira = 0
        doc.calcular_status_validade()
        self.assertEqual(doc.status_validade, "Vencido")

        # 2. Documento a vencer (< 30 dias)
        doc.data_validade = add_days(nowdate(), 10)
        doc.calcular_status_validade()
        self.assertEqual(doc.status_validade, "A Vencer")

        # 3. Documento válido
        doc.data_validade = add_days(nowdate(), 60)
        doc.calcular_status_validade()
        self.assertEqual(doc.status_validade, "Válido")

        # 4. Documento que não expira
        doc.nao_expira = 1
        doc.calcular_status_validade()
        self.assertEqual(doc.status_validade, "Não se Aplica")
        self.assertIsNone(doc.data_validade)

        # 5. Auditoria de aprovação
        doc.status_aprovacao = "Aprovado"
        doc.tratar_auditoria_aprovacao()
        self.assertIsNotNone(doc.validado_por)
        self.assertIsNotNone(doc.data_validacao)
