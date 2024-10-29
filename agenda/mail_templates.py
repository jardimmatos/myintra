from agenda.models import Reserva


def try_object_mails(reserva : Reserva):
    to = reserva.created_by.email
    
    # limpar dos gestores o e-mail do destinatário
    gestores = list(set(reserva.espaco.gestores.values_list('email', flat=True)))
    try: gestores.remove(to) 
    except: pass

    # limpar dos admins os e-mails dos gestores
    admins = list(set(reserva.espaco.admins.values_list('email', flat=True)))
    try: admins.remove(to)
    except: pass

    for g in gestores:
        try: admins.remove(g)
        except: pass

    to = [to] if to else [] # apply to array
    bcc = [] # bcc = admins #(Suspendendo admins de receberem e-mails)
    cc = gestores
    return to, cc, bcc

def status_to_label(status: str):
    if status == 'CANCELLED': return 'CANCELADO'
    if status == 'OPENED': return 'ABERTO'
    if status == 'PENDING': return 'AGUARDANDO APROVAÇÃO'
    return status

def status_to_label_html(status: str):
    status_label = status_to_label(status)
    if status == 'CANCELLED': return '<span style="color:{0}"><b>{1}</b></span>'.format('red', status_label )
    if status == 'OPENED': return '<span style="color:{0}"><b>{1}</b></span>'.format('green', status_label )
    if status == 'PENDING': return '<span style="color:{0}"><b>{1}</b></span> <i>(Você receberá um novo e-mail em caso de aprovação ou cancelamento desta reserva)</i>'.format('orange', status_label )
    
    return status_label
    
def template_abertura_reserva(reserva : Reserva):
    
    content = """
            <div style="border-left-width: 7px;border-left-color: #70abcd;border-left-style: solid;padding: 0 0 0 8px;">
                <div><b>Responsável:</b> {0}</div>
                <div><b>Espaço:</b> {1}</div>
                <div><b>Finalidade:</b> {2}</div>
                <div><b>Data:</b> {3}</div>
                <div><b>Status:</b> {4}</div>
                <div><b>Observação:</b> {5}</div>
                <div><b>Criado por:</b> {6}</div>
            <div>
            <br>
            <br>
            <br>
            <small>identificador: {7}</small>
            """.format(
                reserva.responsavel,                            # 0
                reserva.espaco.descricao,                       # 1
                reserva.finalidade.descricao,                   # 2
                reserva.date_start_end,                         # 3
                status_to_label_html(reserva.status_reserva),   # 4
                reserva.observacao or '',                       # 5
                reserva.created_by.get_full_name() or '',       # 6
                reserva.id                                      # 7
            )
    
    to, cc, bcc = try_object_mails(reserva)
    
    params = dict()
    params['assunto'] = 'AgendaLabs - Nova reserva registrada'#, 'Notificação Agendalabs'),
    params['content'] = content
    params['to'] = to
    params['cc'] = cc
    params['bcc'] = bcc
    params['reply_to'] = []
    params['template'] = 'email/agenda/agenda_abertura.html'
    return params

def template_aprovacao_reserva(reserva : Reserva):
    content = """
            <div>
               <p>
                    <b>Sua reserva foi avaliada e aprovada. Para mais detalhes, segue abaixo o resumo da reserva.</b>
               </p> 
            </div>
            <div style="border-left-width: 7px;border-left-color: #569459;border-left-style: solid;padding: 0 0 0 8px;">
                <div><b>Responsável:</b> {0}</div>
                <div><b>Espaço:</b> {1}</div>
                <div><b>Finalidade:</b> {2}</div>
                <div><b>Data:</b> {3}</div>
                <div><b>Status:</b> {4}</div>
                <div><b>Observação:</b> {5}</div>
                <div><b>Criado por:</b> {6}</div>
            </div>
            <br>
            <div><i>Aprovado em {7}</i></div>
            <br>
            <br>
            <br>
            <small>identificador: {8}</small>
            """.format(
                reserva.responsavel,                            
                reserva.espaco.descricao,                       
                reserva.finalidade.descricao,                   
                reserva.date_start_end,                         
                status_to_label_html(reserva.status_reserva),   
                reserva.observacao or '',                       
                reserva.created_by.get_full_name() or '',       
                reserva.get_updated_at or '',                   
                reserva.id,                                     
            )
    
    to, cc, bcc = try_object_mails(reserva)
    
    params = dict()
    params['assunto'] = 'AgendaLabs - Aprovação de reserva'#, 'Notificação Agendalabs'),
    params['content'] = content
    params['to'] = to
    params['cc'] = cc
    params['bcc'] = bcc
    params['reply_to'] = cc + bcc
    params['template'] = 'email/agenda/agenda_aprovacao.html'
    return params

def template_cancelamento_reserva(reserva : Reserva):
    content = """
            <div>
               <p style="color: #941212">
                    <b>Não foi possível autorizar esta reserva. Para mais detalhes, segue abaixo o resumo da reserva e o motivo do cancelamento ou entre em contato neste mesmo e-mail.</b>
               </p> 
            </div>
            <div style="border-left-width: 7px;border-left-color: #924848;border-left-style: solid;padding: 0 0 0 8px;">
                <div><b>Responsável:</b> {0}</div>
                <div><b>Espaço:</b> {1}</div>
                <div><b>Finalidade:</b> {2}</div>
                <div><b>Data:</b> {3}</div>
                <div><b>Status:</b> {4}</div>
                <div><b>Observação:</b> {5}</div>
                <div><b>Criado por:</b> {6}</div>
            </div>
            <br>
            <div><i>Cancelado em {7}</i></div>
            <div style="color: #941212"><b>MOTIVO: {8}</b></div>
            <br>
            <br>
            <br>
            <small>identificador: {9}</small>
            
            """.format(
                reserva.responsavel,                                                        # 0
                reserva.espaco.descricao,                                                   # 1
                reserva.finalidade.descricao,                                               # 2
                reserva.date_start_end,                                                     # 3
                status_to_label_html(reserva.status_reserva),                               # 4
                reserva.observacao or '',                                                   # 5
                reserva.created_by.get_full_name() or '',                                   # 6
                reserva.get_updated_at or '',                                               # 7
                reserva.status_descricao or 'Nenhuma informação sobre este cancelamento',   # 8
                reserva.id                                                                  # 9
            )
    
    to, cc, bcc = try_object_mails(reserva)

    params = dict()
    params['assunto'] = 'AgendaLabs - Aprovação de reserva'#, 'Notificação Agendalabs'),
    params['content'] = content
    params['to'] = to
    params['cc'] = cc
    params['bcc'] = bcc
    params['reply_to'] = cc + bcc
    params['template'] = 'email/agenda/agenda_cancelamento.html'
    return params
