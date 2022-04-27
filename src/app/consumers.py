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
            dice_pattern = re.compile("^d(4|8|10|12|20|100)$") # accepts dice rolls that are 4, 8, 10, 12, 20, and 100
            result = re.match(dice_pattern, message[0])
            if result: 
                die_num = int(message[0][1:])
                response = random.randint(1, die_num)
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
        dice_pattern = re.compile("^d(4|8|10|12|20|100)$") # accepts dice rolls that are 4, 8, 10, 12, 20, and 100
        result = re.match(dice_pattern, message[0])
        if result: 
            die_num = int(message[0][1:])
            response = random.randint(1, die_num)
            self.send({
                'roll': response
            })