from channels.generic.websocket import JsonWebsocketConsumer

class TestConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, content):
        self.send_json({
            'message': 'Hello, this is a response from the server!'
        })
