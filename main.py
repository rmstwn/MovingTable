from moving_table.moving_table import MovingTableController
from moving_table.oml_mrtu import *
import threading

# ------------------- Initialize communication -------------------
# Table 1 on USB0
comm_table1 = commPC(argPort="/dev/ttyUSB0", argBaudrate=115200)
motor1_t1 = ModbusAZ(comm=comm_table1, serverAddress=1)
motor2_t1 = ModbusAZ(comm=comm_table1, serverAddress=2)
motor3_t1 = ModbusAZ(comm=comm_table1, serverAddress=3)
table1 = MovingTableController(motor1_t1, motor2_t1, motor3_t1)

# Table 2 on USB1
comm_table2 = commPC(argPort="/dev/ttyUSB1", argBaudrate=115200)
motor1_t2 = ModbusAZ(comm=comm_table2, serverAddress=1)
motor2_t2 = ModbusAZ(comm=comm_table2, serverAddress=2)
motor3_t2 = ModbusAZ(comm=comm_table2, serverAddress=3)
table2 = MovingTableController(motor1_t2, motor2_t2, motor3_t2)

# ------------------- Configure motors -------------------
for table in [table1, table2]:
    for m in [table.motor1, table.motor2, table.motor3]:
        table.configure_motor(m)

# ------------------- Move tables -------------------
# # Move table 1: 100mm forward, rotate 45 degrees
# table1.go_to_table(
#     distance_mm=100,
#     linear_speed_pulses=8000,
#     angle_degrees=45,
#     rotate_speed_pulses=4000,
#     operation_type=1,
# )

# # Move table 2: 100mm forward, rotate 45 degrees
# table2.go_to_table(
#     distance_mm=100,
#     linear_speed_pulses=8000,
#     angle_degrees=45,
#     rotate_speed_pulses=3500,
#     operation_type=1,
# )


# --- Define movement for each table ---
def move_table1():
    table1.go_to_table(
        distance_mm=0,  # linear movement in mm
        angle_degrees=0,  # rotation in degrees
        linear_speed=5000,  # linear speed in pulses
        rotate_speed=2000,  # rotation speed in pulses
        operation_type=1,
    )


def move_table2():
    table2.go_to_table(
        distance_mm=0,
        angle_degrees=0,
        linear_speed=5000,
        rotate_speed=2000,
        operation_type=1,
    )


# --- Run both tables simultaneously ---
thread1 = threading.Thread(target=move_table1)
thread2 = threading.Thread(target=move_table2)

thread1.start()
thread2.start()

# Wait until both tables finish
thread1.join()
thread2.join()

print("✅ Both tables have completed their movements.")
