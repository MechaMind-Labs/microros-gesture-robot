# 🤖 Gesture Controlled Robot using IMU with micro-ROS & ROS 2 (ESP32-based)

Welcome to the **Gesture Controlled Robot** project!
Here we bring together **ESP32 + MPU6050 IMU + micro-ROS + ROS 2** to control and visualize robot movements using hand gestures.

---

## 🎥 ESP32+MPU6050 Gesture Control Demo  
https://github.com/user-attachments/assets/ebf6ab36-b1be-4994-98d0-e850d915f325

https://github.com/user-attachments/assets/ed5868a6-5296-4faf-98b2-f56f7fcc2eed

---

This project shows how you can:

* 📡 Stream real-time IMU data from an **ESP32** running micro-ROS.
* 🔗 Bridge it to a **ROS 2 agent** over serial USB.
* 🎛️ Visualize orientation and motion data inside **RViz2**.
* 🦾 Control a robot in simulation (and extend it to real robots).

---

## 🛠️ Hardware Setup (MPU6050 ↔ ESP32 I²C Wiring)

**Connections (default ESP32 pins for I²C):**

| MPU6050 Pin | ESP32 Pin                          |
| ----------- | ---------------------------------- |
| **VCC**     | 3.3V                               |
| **GND**     | GND                                |
| **SDA**     | GPIO21                             |
| **SCL**     | GPIO22                             |

👉 You can remap pins with `Wire.begin(SDA_pin, SCL_pin)` if you need different GPIOs.

---

## 💻 Software Requirements

* ROS 2 (Humble or compatible distro)
* [micro-ROS setup tools](https://micro.ros.org/docs/tutorials/core/first_application_linux/) 🛠️
* Arduino IDE with [`micro_ros_arduino`](https://github.com/micro-ROS/micro_ros_arduino) library
* Java (for running Telemetry Viewer `.jar` if used) → [Download from FarrellF](http://www.farrellf.com/TelemetryViewer/) ☕

---

## ⚡ Install `micro_ros_arduino` in Arduino IDE

1. Open Arduino IDE → `Sketch` → `Include Library` → `Manage Libraries...`
2. Search for **micro\_ros\_arduino** and install.
   *(Or download the repo as ZIP from [GitHub](https://github.com/micro-ROS/micro_ros_arduino) and add manually.)*
3. Open example sketches under `File → Examples → micro_ros_arduino`.
4. Select your ESP32 board & correct port, then upload.

---

## 📊 Telemetry Viewer Setup

1. Install Java (JRE/JDK).
2. Download `TelemetryViewer.jar` (or the tool provided).
3. Run it with:

   ```bash
   java -jar TelemetryViewer.jar
   ```
4. Configure serial port (e.g., `/dev/ttyUSB0`) and baud rate (e.g., `115200` or `921600`).

---


## 📥 Clone & Setup the Gesture Controlled Robot Workspace

Follow the steps below to clone the repository, move the packages into your ROS 2 workspace, install dependencies, and build everything.

---

### **1️⃣ Go to Home Directory**

```bash
cd ~
```

### **2️⃣ Clone the Repository**

```bash
git clone https://github.com/MechaMind-Labs/Gesture_Controlled_Robot.git
```

---

### **3️⃣ Create a ROS 2 Workspace**

```bash
mkdir -p gesture_ws/src
```

---

### **4️⃣ Move All Packages Into the Workspace**

```bash
mv Gesture_Controlled_Robot/* gesture_ws/src/
```

(Optional: remove empty repo folder)

```bash
rm -rf Gesture_Controlled_Robot
```

---

### **5️⃣ Navigate to the Workspace**

```bash
cd gesture_ws
```

---

### **6️⃣ Install Dependencies Using rosdep**

```bash
cd ~
sudo apt install python3-rosdep -y
sudo rosdep init
rosdep update
```

```bash
cd ~/gesture_ws
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

---

### **7️⃣ Build the Workspace**

```bash
colcon build
```

---

### **8️⃣ Source the Workspace**

```bash
source install/setup.bash
```
---

# 🚀 micro-ROS Setup Guide (ROS 2)

This is a step-by-step guide to install and build **micro-ROS** on your ROS 2 system.
Follow the instructions below to set up the firmware workspace, build the micro-ROS Agent, and prepare your development environment.

---

## 🛠️ 1. Source ROS 2 Environment

Before anything else, source your ROS 2 installation:

```bash
cd ~
source /opt/ros/$ROS_DISTRO/setup.bash
```

---

## 📁 2. Create micro-ROS Workspace & Clone Tools

```bash
mkdir microros_ws
cd microros_ws
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
```

---

## 📦 3. Install Dependencies

```bash
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y
```

Install pip (if not already installed):

```bash
sudo apt-get install python3-pip
```

---

## 🧱 4. Build micro-ROS Tools

```bash
colcon build
source install/local_setup.bash
```

---

## 🔧 5. Create Firmware Workspace

```bash
ros2 run micro_ros_setup create_firmware_ws.sh host
```

---

## 🏗️ 6. Build Firmware

```bash
ros2 run micro_ros_setup build_firmware.sh
source install/local_setup.bash
```

---

## 📥 7. Download micro-ROS Agent Packages

```bash
ros2 run micro_ros_setup create_agent_ws.sh
```

---

## 🏗️ 8. Build micro-ROS Agent

```bash
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash
```

---

## 🎉 You're Ready to Use micro-ROS!
---

⚠️ Replace `/dev/ttyUSB0` with your board’s serial port (check with `ls /dev/serial/by-id/*`).

---

🧩 **Run URDF to see Cylinder (imu_link)**

```bash
ros2 run robot_state_publisher robot_state_publisher ~/gesture_ws/src/imu_visualizer/urdf/imu_cube.urdf & rviz2
```
---

## 🚀 Run the Full Gesture Control Robot Project

### **1️⃣ Flash the ESP32 Firmware (micro_ros_imu.ino)**

1. Open **Arduino IDE**.
2. Navigate to the firmware file:

   ```
   imu_visualizer/firmware/micro_ros_imu/micro_ros_imu.ino
   ```
3. Connect your **ESP32** with the **exact wiring** shown in the project README.
4. In Arduino IDE, select:

   * **Board:** ESP32 Dev Module
   * **Port:** Correct COM port
5. Make sure the **baud rate is set to 115200**.
6. Click **Upload** to flash the firmware onto the ESP32.

---

### **2️⃣ Configure ROS 2 Humble Environment**

🧩 Add ROS Humble setup and ROS Domain ID to your `~/.bashrc`:

```bash
cd ~
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=1" >> ~/.bashrc
```

Reload the updated environment:

```bash
source ~/.bashrc
```

---

### Open **3 terminals** (each sourced to your ROS 2 workspace).

1️⃣ **Start the micro-ROS Agent (Terminal 1), then press reset button on ESP32**

```bash
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```

2️⃣ **Bring up the simulated robot (Terminal 2)**

```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch bot_bringup simulated_robot.launch.py
```

3️⃣ **Run IMU controller (subscriber + logic) (terminal 3)**

```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer imu_controller.launch.py
```
---

## 🚀 Run the IMU Cube Visualization

Open **2 terminals** (each sourced to your ROS 2 workspace).

1️⃣ **Start the micro-ROS Agent (Terminal 1), then press reset button on ESP32**

```bash
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```

2️⃣ **Visualize IMU Cylinder in RViz (Terminal 2)**

```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer view_imu.launch.py
```

👉 Now you can **see your IMU orientation in RViz and also control the robot with Gestures** 🎉

---

## ⚠️ Troubleshooting

* **No data?** → Check wiring (SDA/SCL), loose connections, baud rate, and serial port.
* **Permission denied on `/dev/ttyUSB0`?** →

  ```bash
  sudo usermod -a -G dialout $USER
  ```

  *(Log out and back in after adding user to `dialout`.)*
* **IMU outputs 0** → Ensure VCC = 3.3V and check IMU address.

---

## 📚 References

* 🌐 [micro-ROS Tutorials](https://micro.ros.org/docs/tutorials/core/first_application_linux/)
* 🌐 [ROS2 Humble Docs](https://docs.ros.org/en/humble/index.html)

---

## 🙌 Credits

Maintained by **[Curious-Utkarsh](https://github.com/Curious-Utkarsh)**
✨ You’ve built your own **Gesture Controlled Robot with ESP32 + micro-ROS + ROS 2**!

---
