import asyncio
import websockets
from websockets.server import serve

all_clients = []
# Список, потому что закидываем каждое соединение, а соединений может быть несколько с одного ip
# Здесь будут клиенты


async def send_message(message: str):
    for client in all_clients:
        await client.send(message)


async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
    # client_socket соединение от клиента к сокету
    print('Connected new client')
    all_clients.append(client_socket)
    while True:
        new_message = await client_socket.recv()
#         Принимает данные из сокета в буфер и
#         возвращает эти данные как последовательность байтов (bytes).
#         Операция recv() блокирует выполнение кода до тех пор,
#         пока не будет получено хотя бы одно сообщение от сервера.
        print(f'New message from client: `{new_message}`')
        await send_message(message=new_message)


async def start_server():
    async with serve(new_client_connected, "localhost", 12345):
        await asyncio.Future()  # run forever
    # Callback это то, что происходит, когда клиент подключается.
    # Является асинхронной функцией
    # запуска WebSocket-сервера в асинхронном режиме на указанном хосте и порту


if __name__ == "__main__":
    asyncio.run(start_server())
