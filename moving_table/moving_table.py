import time
from typing import Optional
from moving_table.oml_mrtu import *

# Wheel and encoder parameters
WHEEL_CIRCUMFERENCE = 40.0 * 3.14159265359  # mm
PULSES_PER_REVOLUTION = 12000  # Encoder pulses per wheel revolution


class MovingTableController:
    def __init__(self, motor1: ModbusAZ, motor2: ModbusAZ, motor3: ModbusAZ):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3

    # ---------------- Motor configuration ----------------
    def configure_motor(
        self, motor: ModbusAZ, acc: int = 1000, speed: int = 100000, current: int = 1000
    ) -> bool:
        """Configure motor acceleration, deceleration, current and reset alarms."""
        if not motor.writeParamAcc(time=acc, speed=speed):
            print(f"Failed to set acceleration for motor {motor}")
            return False
        if not motor.writeParamDec(time=acc, speed=speed):
            print(f"Failed to set deceleration for motor {motor}")
            return False
        if not motor.writeParamCurrent(current=current):
            print(f"Failed to set current for motor {motor}")
            return False
        motor.resetAlarm()
        return True

    # ---------------- Move linear table ----------------
    def move_table(
        self, distance_mm: float, speed_pulses: int, operation_type: int
    ) -> bool:
        """Move linear table motors (motor1, motor2) by distance_mm."""
        pulses = int((distance_mm / WHEEL_CIRCUMFERENCE) * PULSES_PER_REVOLUTION)
        print(f"Moving table {distance_mm} mm -> {pulses} pulses")

        if not self.motor1.startPosition(
            position=pulses, speed=speed_pulses, OpeType=operation_type
        ):
            print("Failed to move Motor 1")
            return False
        if not self.motor2.startPosition(
            position=pulses, speed=speed_pulses, OpeType=operation_type
        ):
            print("Failed to move Motor 2")
            return False

        return True

    # ---------------- Rotate table ----------------
    def rotate_table(
        self, angle_degrees: float, speed_pulses: int, operation_type: int
    ) -> bool:
        """Rotate table motor (motor3) by angle in degrees."""
        pulses_per_degree = 9000 / 90  # 9000 pulses = 90 degrees
        pulses = int(angle_degrees * pulses_per_degree)
        print(f"Rotating table {angle_degrees}° -> {pulses} pulses")

        if not self.motor3.startPosition(
            position=pulses, speed=speed_pulses, OpeType=operation_type
        ):
            print("Failed to rotate Motor 3")
            return False

        return True

    # ---------------- Combined move ----------------
    def go_to_table(
        self,
        distance_mm: float,
        linear_speed_pulses: int,
        angle_degrees: float,
        rotate_speed_pulses: int,
        operation_type: int,
        delay_after_move: Optional[float] = 0.2,
    ):
        """Move and rotate table sequentially."""
        print(f"🟢 Moving table: distance={distance_mm}mm, angle={angle_degrees}°")

        success = self.move_table(distance_mm, linear_speed_pulses, operation_type)
        print(f"➡ Move success: {success}")
        if not success:
            return False

        time.sleep(delay_after_move)

        success = self.rotate_table(angle_degrees, rotate_speed_pulses, operation_type)
        print(f"🔄 Rotate success: {success}")
        if not success:
            return False

        print(f"🏁 Table movement complete: {distance_mm} mm, {angle_degrees}°")
        return True
