## game/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class AgendaLabsWebsocket(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['channel_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print('agendalabs websocket socket connect', self.room_name, self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # print("agendalabs websocket Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print("agendalabs websocket receiving")
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        
        if event == 'CREATED':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "CREATED"
            })

        if event == 'UPDATED':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "UPDATED"
            })

        if event == 'APPROVED':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "APPROVED"
            })

        if event == 'CANCELLED':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "CANCELLED"
            })

    async def send_message(self, res):
        # print("agendalabs websocket send_message", res)
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))