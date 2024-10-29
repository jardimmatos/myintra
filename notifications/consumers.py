## game/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationsWebsocket(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print('notifications websocket socket connect', self.room_name, self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # print("notifications websocket Disconnected", close_code)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print("notification websocket receiving", text_data)
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        notify = response.get("notify", True)

        if event == 'CREATED':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "CREATED",
                "notify": notify
            })

        if event == 'CHANGED':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "CHANGED",
                'notify': notify
            })

        if event == 'DELETED':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "DELETED",
                'notify': notify
            })


    async def send_message(self, res):
        # print("notifications websocket send_message", res)
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({ "payload": res }))