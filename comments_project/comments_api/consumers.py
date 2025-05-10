# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class CommentConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("comments", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("comments", self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.channel_layer.group_send(
#             "comments",
#             {
#                 "type": "send_comment",
#                 "message": data["message"]
#             }
#         )

#     async def send_comment(self, event):
#         await self.send(text_data=json.dumps({
#             "message": event["message"]
#         }))


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("comments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def receive(self, text_data):
        pass  # we don’t expect clients to send data via WebSocket

    async def new_comment(self, event):
        await self.send(text_data=json.dumps(event["comment"]))
