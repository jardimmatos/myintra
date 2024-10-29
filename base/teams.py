import json
import requests

from base.utils import split_list

class TeamsTemplates:
    TEMPLATE_SIMPLES = 0
    TEMPLATE_HTML = 1 # este padrao não aceita imagens no corpo HTML
    TEMPLATE_FACTS = 2

    def __init__(self, options={}):
        self.template = options.get('template', self.TEMPLATE_SIMPLES)
        self.channel = options.get('channel', None)
        self.title = options.get('title', '')
        self.subtitle = options.get('subtitle', '')
        self.messages = options.get('messages', [])
        self.url_image = options.get('url_image', None)
        self.color = options.get('color', 'd70076')

    
    def template_simples_imagem(self):
        items = []
        # Card Templates
        # https://adaptivecards.io/designer

        # TITULO
        items.append({
            "type": "TextBlock",
            "text": self.title,
            "size":"medium",
            "style": "heading"
        })

        # Imagem
        if self.url_image: 
            items.append({ "type": "Image", "url": self.url_image })
        
        # MENSAGEM
        for m in self.messages:
            items.append({
                "type": "TextBlock",
                "text": m
            })

        # RODAPÉ
        items.append({
            "type": "TextBlock",
            "text": self.subtitle,
            "size":"small",
            "style": "heading",
            "isSubtle": True
        })

        # BOTAO INTRANET
        # items.append({
        #     "type": "ActionSet",
        #     "actions": [
        #         {
        #             "type": "Action.OpenUrl",
        #             "title": "Intranet",
        #             "tooltip": "Acessar Intranet",
        #             "url": "https://meuservidor.dev.br"
        #         }
        #     ]
        # })
        # {
        #     "type": "TextBlock",
        #     "text": "For Samples and Templates, see [https://adaptivecards.io/samples](https://adaptivecards.io/samples)"
        # },

        payload = {
            "type":"message",
            "attachments":[
                {
                    "contentType":"application/vnd.microsoft.card.adaptive",
                    "contentUrl":None,
                    "content":{
                        "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                        "type":"AdaptiveCard",
                        "version":"1.2",
                        "body":items
                    }
                }
            ]
        }
        # self.send(payload)
        return payload

    def template_html(self):
        payload = {
            "type":"message",
            "attachments":[
                {
                    "contentType": "application/vnd.microsoft.teams.card.o365connector",
                    "content": {
                        "@type": "MessageCard",
                        "@context": "https://schema.org/extensions",
                        "summary": "Summary",
                        "title": self.title,
                        "sections": [ { "text": m } for m in self.messages ]
                    }
                }
            ]
        }
        # self.send(payload)
        return payload

    def template_facts(self):
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": self.color,
            "summary": "tasks",
            "sections": [{
                "activityTitle": self.title,
                "activitySubtitle": self.subtitle,
                "activityImage": "https://i.imgur.com/IWRNYlR.png",
                "facts": [{ "name": m[0], "value": m[1] } for m in self.messages],
                "markdown": True
            }],
        }
           
        # self.send(payload)
        return payload


    def send(self):
        try:
            if self.template == self.TEMPLATE_HTML:
                payload = self.template_html()
            
            elif self.template == self.TEMPLATE_FACTS:
                payload = self.template_facts()

            else:
                payload = self.template_simples_imagem()

            payload = json.dumps(payload)
            response = requests.post(self.channel, payload)
            # print(response.__dict__)
        except Exception as ex:
            print('Exception on send TeamsTemplates: ', str(ex))


        

def format_message(message):
    # print('message teams', message)
    ''' message deve conter um dict com as keys SERVER, LOGS e descricao da integração (INTEGRACAO) '''
    content_body = []
    header_body = {
        "type": "ColumnSet",
        "style": "accent",
        "bleed": True,
        "columns": [
            {
                "type": "Column",
                "width": "auto",
                "items": [
                    {
                        "type": "Image",
                        "url": "#",
                        "altText": "Myintranet",
                        "size": "Small"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "stretch",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"{message.get('INTEGRACAO', '#')}",
                        "size": "Medium"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"{message.get('SERVER', '#')}",
                        "spacing": "None"
                    }
                ]
            }
        ]
    }
    content_body.append(header_body)
    for l in message.get('LOGS'):
        content_body.append( { "type": "TextBlock", "text": str(l) } )

    default_payload = { 
        "msteams": {
            "width": "Full"
        },
        "$schema": "http://adaptivecards.io/schemas/1.2.0/adaptive-card.json", 
        "type": "AdaptiveCard", 
        "version": "1.0" 
    }
    default_payload['body'] = content_body

    full_body =  {
    "type":"message",
    "attachments":[
       {
          "contentType":"application/vnd.microsoft.card.adaptive",
          "contentUrl":None,
          "content":default_payload
       }
    ]
     }
    return full_body

def send_to_teams(channel, message):
    if not channel: return
    url = channel
    # quebrar os logs em grupos de logs limitados a 20 logs por mensagem no teams
    splited_logs_msgs = split_list(20, message.get('LOGS'))
    for msgs in splited_logs_msgs:
        message['LOGS'] = msgs

        payload = json.dumps(format_message(message))
        response = requests.post(url, payload)
    return response


# NOVOS METODOS
def send_to_teams_channel(options):
    try:
        # print('sending content...', options)
        channel = options.get('channel', None)
        title = options.get('title', 'Notificação')
        subtitle = options.get('subtitle', 'Intranet')
        message = options.get('message', [])
        url_image = options.get('url_image', None)
        if not channel: return
        if len(message) == 0: return

        items = []
        # Card Templates
        # https://adaptivecards.io/designer

        # TITULO
        items.append({
            "type": "TextBlock",
            "text": title,
            "size":"medium",
            "style": "heading"

        })

        # Imagem
        if url_image: 
            items.append({ "type": "Image", "url": url_image })
        
        # MENSAGEM
        for m in message:
            items.append({
                "type": "TextBlock",
                "text": m
            })

        # RODAPÉ
        items.append({ "type": "TextBlock", "text": '-' })
        items.append({
            "type": "TextBlock",
            "text": subtitle,
            "size":"small",
            "style": "heading",
            "isSubtle": True
        })

        # BOTAO INTRANET
        items.append({
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "Intranet",
                    "tooltip": "Acessar Intranet",
                    "url": "https://meuservidor.dev.br"
                }
            ]
        })

        default_payload = {
            "type":"message",
            "attachments":[
                {
                    "contentType":"application/vnd.microsoft.card.adaptive",
                    "contentUrl":None,
                    "content":{
                        "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                        "type":"AdaptiveCard",
                        "version":"1.2",
                        "body":items
                    }
                }
            ]
        }
        
        url = channel
        payload = json.dumps(default_payload)
        response = requests.post(url, payload)
        # print('response', response.__dict__)
    except Exception as ex:
        print('Exception on send_to_teams_channel: ', str(ex))
    return options

# def send_to_teams_channel(channel, title, subtitle, message):
#     if not channel: return
#     url = channel
#     payload = json.dumps(format_message(title, subtitle, message))
#     response = requests.post(url, payload)
#     return response



'''payload={
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "d70076",
        "summary": "Larry Bryant created a new task",
        "sections": [{
            "activityTitle": "Larry Bryant created a new task",
            "activitySubtitle": "On Project Tango",
            "activityImage": "https://i.imgur.com/IWRNYlR.png",
            "facts": [{
                "name": "Assigned to",
                "value": "Unassigned"
            }, {
                "name": "Due date",
                "value": "Mon May 01 2017 17:07:18 GMT-0700 (Pacific Daylight Time)"
            }, {
                "name": "Status",
                "value": "Not started"
            }],
            "markdown": True
        }],
        "potentialAction": [{
            "@type": "ActionCard",
            "name": "Add a comment",
            "inputs": [{
                "@type": "TextInput",
                "id": "comment",
                "isMultiline": False,
                "title": "Add a comment here for this task"
            }],
            "actions": [{
                "@type": "HttpPOST",
                "name": "Add comment",
                "target": "https://docs.microsoft.com/outlook/actionable-messages"
            }]
        }, {
            "@type": "ActionCard",
            "name": "Set due date",
            "inputs": [{
                "@type": "DateInput",
                "id": "dueDate",
                "title": "Enter a due date for this task"
            }],
            "actions": [{
                "@type": "HttpPOST",
                "name": "Save",
                "target": "https://docs.microsoft.com/outlook/actionable-messages"
            }]
        }, {
            "@type": "OpenUri",
            "name": "Learn More",
            "targets": [{
                "os": "default",
                "uri": "https://docs.microsoft.com/outlook/actionable-messages"
            }]
        }, {
            "@type": "ActionCard",
            "name": "Change status",
            "inputs": [{
                "@type": "MultichoiceInput",
                "id": "list",
                "title": "Select a status",
                "isMultiSelect": "false",
                "choices": [{
                    "display": "In Progress",
                    "value": "1"
                }, {
                    "display": "Active",
                    "value": "2"
                }, {
                    "display": "Closed",
                    "value": "3"
                }]
            }],
            "actions": [{
                "@type": "HttpPOST",
                "name": "Save",
                "target": "https://docs.microsoft.com/outlook/actionable-messages"
            }]
        }]
    }'''

'''
    {
   "type":"message",
   "attachments":[
      {
         "contentType":"application/vnd.microsoft.card.adaptive",
         "contentUrl":null,
         "content":{
            "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
            "type":"AdaptiveCard",
            "version":"1.2",
            "body":[
                {
                "type": "TextBlock",
                "text": "For Samples and Templates, see [https://adaptivecards.io/samples](https://adaptivecards.io/samples)"
                }
            ]
         }
      }
   ]
}
'''


