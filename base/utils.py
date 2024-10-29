from datetime import datetime
from cryptography.fernet import Fernet
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.pagination import PageNumberPagination


def chunks_split_list(lista, k):
    # transforma uma lista em lista de subgrupos com k itens cada
    #lista de entrada
    #['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #
    #lista de saída
    #[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'], ['U', 'V', 'W', 'X', 'Y', 'Z']]
    for i in range(0, len(lista), k):
        yield lista[i:i + k]
        
def split_list(max_items, items):
    return list(chunks_split_list(items, max_items))

# Gerar Nova Chave
CRYPT_KEY = b'okX-QwAhIz6hTJ7Gq2j933E89g9YlPtYhcf1hvYtg4o='
f = Fernet(CRYPT_KEY)

def criptografar(value):
    mensagem_cripto = f.encrypt(value.encode()) #converter string pra bytes
    return mensagem_cripto.decode() # devolver em string

def descriptografar(token):
    mensagem_descripto  = f.decrypt(token.encode())
    return mensagem_descripto.decode() # devolver em string


class CustomParamPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'


def call_ws(channel_name='room_channel_notifications', msg='', tag='CHANGED', obj={}, notify=False):
    '''
        função para chamada de ws para disparo de gatilhos baseado nas tags
        Parâmetros
         - channel_name: str - nome do channel
         - msg: str - mensagem que será transportada para o ws
         - tag: str - tag que será utilizada na chamada
         - obj: dict - objeto
         - notify: boolean - indicador de exibição de alerta

    '''
    # print('calling ws', msg, tag)
    # usado apenas para disparar um CHANGED type para o channel
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            'type': 'send_message',
            'message': str(msg),
            "event": str(tag),
            "notify": notify,
            "obj": obj
        }
    )

def register_gateway(request, msg='register gateway', app='base', notify=False, priority=0):
    """ 
        Priority - 0: low, 1: medium, 2:high
        Apenas para utilização de flag de cores caso necessário, por exemplo, nome de classe css
    """
    try:
        channel_name='room_channel_gateway'

        data_hora = str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        user = request.user if request and request.user else "Automação"
        html = f"""
                <samp style="color: grey">[{data_hora}]</samp> - <samp style="color: white">[{user}]<samp><br>
                <samp style="color: grey">[{app}]</samp> - <samp style="color: green">{str(msg)}</samp>
            """
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {
                'type': 'send_message',
                'message': msg,
                'html': html,
                'date_time': data_hora,
                "app": app,
                "user": f'{user}',
                "priority": priority,
                "notify": notify
            }
        )
    except Exception as ex:
        print('Falha ao registrar log em Gateway', str(ex))