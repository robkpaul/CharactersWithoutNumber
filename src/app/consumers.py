import json, re, random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        response = 'invalid command'
        text_data_json = json.loads(text_data)
        if(text_data_json['message'] != ''):
            message = str(text_data_json['message']).split()
            dice_pattern = re.compile("^[1-9]*d(4|6|8|10|12|20|100)$") # accepts dice rolls that are 4, 6, 8, 10, 12, 20, and 100
            result = re.match(dice_pattern, message)
            if result: 
                splits = message.split('d')
                response = 0
                for i in range(int(splits[0])):
                    response += random.randint(1, splits[1])
                self.send({
                    'roll': response
                })
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'dice_roll', 
                        'roll': response
                    }
                )
        print(response)

    def chat_message(self, event):
        message = event['message']
        dice_pattern = re.compile("^[1-9]*d(4|6|8|10|12|20|100)$") # accepts dice rolls that are 4, 6, 8, 10, 12, 20, and 100
        result = re.match(dice_pattern, message)
        if result: 
            splits = message.split('d')
            response = 0
            for i in range(int(splits[0])):
                response += random.randint(1, splits[1])
            self.send(text_data=json.dumps({
                'roll': response
            }))