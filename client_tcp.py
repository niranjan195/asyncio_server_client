from test_server import Client


def main():
    print("client set")
    c = Client(host="localhost", port=9000)
    count = 0
    while count != 15:
        # data = str(count) + "tcp"
        data = input("Enter data")
        count += 1
        print("Sending data", data)
        c.send(data)
        data = c.receive()
        print("Received data", data)
    c.close()


main()
