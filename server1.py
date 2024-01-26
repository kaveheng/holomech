import socket
import threading
from indeterminatebeam import Beam, Support, PointLoadV, DistributedLoadV

def handle_client(client_socket):
    # Receive input data from the client
    input_data = client_socket.recv(1024).decode("utf-8")

    # Split the input data into parameters
    length, support_location, point_load_magnitude, point_load_location, distributed_load_magnitude, distributed_load_start, distributed_load_end = map(float, input_data.split(','))

    # Initialize a Beam object
    beam = Beam(length)
    
    # Add supports
    support = Support(support_location, (1, 1, 1))  # Modify the support type as needed
    beam.add_supports(support)

    # Add loads
    point_load = PointLoadV(point_load_magnitude, point_load_location)
    distributed_load = DistributedLoadV(distributed_load_magnitude, (distributed_load_start, distributed_load_end))
    beam.add_loads(point_load, distributed_load)

    # Analyze the beam
    beam.analyse()

    # Get and send results back to the client
    bending_moment_at_3m = beam.get_bending_moment(3)
    x_range=range(1,int(length)+1)
    shear_forces_at_points = [beam.get_shear_force(point) for point in x_range] #[1, 2, 3, 4, 5]]

    response = "Bending moments at 3 m:" + str(bending_moment_at_3m) + "Shear forces at difrent meter of length:" + str(shear_forces_at_points)
    client_socket.send(response.encode("utf-8"))

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8080))
    server.listen(5)

    print("[*] Listening on localhost:8080")

    while True:
        client_socket, addr = server.accept()
        print("[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
