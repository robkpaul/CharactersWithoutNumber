import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'type': 'connection_established'}))
    
    def receive(self):
        self.send(text_data=json.dumps({'type': 'message_received'}))
    def disconnect(self):
        self.send(text_data=json.dumps({'type': 'user_disconnect'}))