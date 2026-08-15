import frappe
from frappe.utils import getdate, nowdate, add_days

def verificar_vencimento_documentos():
    """
    Rotina executada diariamente via Scheduler do Frappe.
    Atualiza status de validade e emite alertas de vencimento.
    """
    hoje = getdate(nowdate())
    limite_alerta = add_days(hoje, 30)

    # 1. Buscar todos os documentos que possuem data de validade definida
    documentos = frappe.get_all(
        "Prime Documento do Colaborador",
        filters={"nao_expira": 0, "data_validade": ["is", "set"]},
        fields=["name", "colaborador", "nome_colaborador", "tipo_documento", "data_validade", "status_validade"]
    )

    total_atualizados = 0
    documentos_a_vencer = []
    documentos_vencidos = []

    for doc_data in documentos:
        validade = getdate(doc_data.data_validade)
        novo_status = None

        if validade < hoje:
            novo_status = "Vencido"
            documentos_vencidos.append(doc_data)
        elif validade <= limite_alerta:
            novo_status = "A Vencer"
            documentos_a_vencer.append(doc_data)
        else:
            novo_status = "Válido"

        if novo_status and novo_status != doc_data.status_validade:
            frappe.db.set_value(
                "Prime Documento do Colaborador",
                doc_data.name,
                "status_validade",
                novo_status,
                update_modified=False
            )
            total_atualizados += 1

    frappe.db.commit()

    # 2. Registrar log de auditoria da rotina
    log_msg = f"Rotina de Documentos Prime: {total_atualizados} atualizados. {len(documentos_a_vencer)} a vencer, {len(documentos_vencidos)} vencidos."
    frappe.logger("prime_erp").info(log_msg)

    return {
        "atualizados": total_atualizados,
        "a_vencer": len(documentos_a_vencer),
        "vencidos": len(documentos_vencidos)
    }
