import json, re, random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('connection on %s' % self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, close_code):
        print('disconnect from %s with code %s' % (self.room_group_name, close_code))
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        response = 'invalid command'
        text_data_json = json.loads(text_data)
        if(text_data_json['message'] != ""):
            message = str(text_data_json['message']).split()
            message = message[0]
            dice_pattern = re.compile("^([1-9]\d?)?d(4|6|8|10|12|20|100)$") # accepts dice rolls that are 4, 6, 8, 10, 12, 20, and 100
            result = re.match(dice_pattern, str(message))
            if result: 
                splits = message.split('d')
                num_rolls = 1 if splits[0] == '' else int(splits[0])
                roll_size = int(splits[1])
                response = 0
                for i in range(num_rolls):
                    response += random.randint(1, roll_size)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message', 
                        'roll': response,
                        'user': text_data_json['user']
                    }
                )
            print('"' + message + '": ' + str(response))

    def chat_message(self, event):
        print(event)
        self.send(text_data=json.dumps({
            'roll': event['roll'],
            'user':  event['user']
        }))