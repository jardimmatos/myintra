import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from users.tasks import set_user_logged_task
from datetime import datetime
from users.models import LoggedUser, User
from asgiref.sync import sync_to_async


class GlobalWebsocket2(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print('global socket connect', self.room_name, self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # print("global Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print("global receiving")
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'INITING':
            # print("global INITING")
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': 'Iniciando',
                "event": "INITING"
            })
        if event == 'MOVE':
            # print("global MOVE")
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # print("global START")
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # print("global END")
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, res):
        # print("global send_message", res)
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))


class GlobalWebsocket(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_connection_counts = 0

    async def connect(self):
        # print('websocket socket scopes', self.scope)
        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print('websocket connect', self.room_group_name)
        # print('self.room_name', self.room_name)
        # print('self.room_group_name', self.room_group_name)
        # print('self.channel_name', self.channel_name)

        if 'channel_session_user' in self.room_group_name:
            try:
                uid = self.room_group_name.split('channel_session_user_')[1]
                user = await sync_to_async(User.objects.get)(id=uid)
                await sync_to_async(
                    LoggedUser.objects.get_or_create)(
                        user=user, defaults={'user': user})
            except Exception:
                pass

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # print("websocket Disconnected", close_code, self.room_group_name)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print("websocket receiving", text_data, self.room_group_name)
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        notify = response.get("notify", True)

        obj = dict()
        obj = {
            'type': 'send_message',
            'message': message,
            "event": event,
            "notify": notify
        }
        await self.channel_layer.group_send(self.room_group_name, obj)

    async def send_message(self, res):
        # print(
        # "websocket send_message", res, self.room_name,self.room_group_name)
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"payload": res}))


# Websocket teste para jogo da velha
class MyWebsocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print('socket connect', self.room_name, self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))


class MyWebsocket2(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # print('on connecting')

        # self.set_user_logged(str(self.scope['user']))

        # Para permitir o ws apenas para usuários autenticados
        # self.user = self.scope['user']
        # if self.user.is_authenticated:
        #     # accept connection if user is logged in
        #     self.accept()
        # else:
        #     # don't accept connection if user is not logged in
        #     self.close()

        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # user = self.scope ['user']

        # if user.is_authenticated:
        #     self.update_user_status (user, True)
        # await self.send_status ()

    async def disconnect(self, close_code):

        # print('on desconnecting', )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print('on receiving', text_data)
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)

        if 'AnonymousUser' == str(self.scope['user']):
            return

        # try:
        #     user = await database_sync_to_async(
        # self.get_user)(str(self.scope['user']))
        #     print('user', user, user.is_authenticated)

        # except Exception as e:
        #     print('ops receive ' + str(e))
        #     return

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': '<div>{} - <small> {}</small></div><div>{}</div>'
                .format(
                    str(self.scope["user"]),
                    str(datetime.now()),
                    message),
                'event': "END"
            })
        if event == 'LOGGED':
            # Send message to room group
            if (message.get('online') == 1):
                # print('online 1')
                set_user_logged_task.delay(str(self.scope['user']))
            if (message.get('online') == 0):
                # print('online 0')
                pass
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "LOGGED"
            })

    async def send_message(self, res):
        # print('on sending from back', res)
        """ Receive message from room group """
        # users = await database_sync_to_async(self.get_users_online)()
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res
            }))
