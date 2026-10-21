# 🤖 Gesture Controlled Robot using IMU with micro-ROS & ROS 2 (ESP32-based)

Welcome to the **Gesture Controlled Robot** project!  
Here we bring together **ESP32 + MPU6050 IMU + micro-ROS + ROS 2** to control and visualize robot movements using hand gestures.

---

## 🎥 ESP32+MPU6050 Gesture Control Demo  

https://github.com/user-attachments/assets/ebf6ab36-b1be-4994-98d0-e850d915f325


> **At a glance:** an ESP32 running micro-ROS reads an MPU6050 IMU and publishes orientation to ROS 2; moving-average and Madgwick filtering clean the data; tilting your hand drives a robot in Gazebo and an IMU cube in RViz. Docker image included.
>
> **Watch:** [full workshop](https://youtu.be/mkafPenW_4M) · [demo clip](https://youtu.be/Ebm1XX329LQ) · LinkedIn: [project post](https://www.linkedin.com/feed/update/urn:li:activity:7364174433982275584/) · [workshop post](https://www.linkedin.com/feed/update/urn:li:activity:7370482998141489152/)
>
> **Playlists:** [Workshops and Live Labs](https://www.youtube.com/playlist?list=PLdMuvhY3uTKtMOVVnfKRV4qswTEHeXTy2) · [Robotics Projects](https://www.youtube.com/playlist?list=PLdMuvhY3uTKstk7-rEB08oEmaAYHoISt5)
>
> **Related:** [UR5 MediaPipe pick-and-place](https://github.com/MechaMind-Labs/ur5-gesture-pick-and-place) — gesture control with a camera instead of an IMU · [Edge Avoiding Robot](https://github.com/MechaMind-Labs/edge-avoiding-robot) — the robot model used here

https://github.com/user-attachments/assets/ed5868a6-5296-4faf-98b2-f56f7fcc2eed

---

This project shows how you can:
* 📡 Stream real-time IMU data from an **ESP32** running micro-ROS
* 🔗 Bridge it to a **ROS 2 agent** over serial USB
* 🎛️ Visualize orientation and motion data inside **RViz2**
* 🦾 Control a robot in simulation (and extend it to real robots)

---

## 🛠️ Hardware Setup (MPU6050 ↔ ESP32 I²C Wiring)

**Connections (default ESP32 pins for I²C):**

| MPU6050 Pin | ESP32 Pin |
| ----------- | --------- |
| **VCC**     | 3.3V      |
| **GND**     | GND       |
| **SDA**     | GPIO21    |
| **SCL**     | GPIO22    |

👉 You can remap pins with `Wire.begin(SDA_pin, SCL_pin)` if you need different GPIOs.

---

## 📋 Table of Contents

1. [🐳 Quick Start with Docker (Recommended)](#-quick-start-with-docker-recommended)
2. [💻 Manual Installation on Local PC](#-manual-installation-on-local-pc)
3. [⚠️ Troubleshooting](#️-troubleshooting)
4. [📚 References](#-references)

---

# 🐳 Quick Start with Docker (Recommended)

Get up and running in minutes with our pre-built Docker image! This method eliminates dependency issues and provides a consistent environment.

## Prerequisites

- **Docker** installed on your system
- **ESP32** with MPU6050 sensor
- **USB cable** to connect ESP32 to your computer
- **Arduino IDE** for flashing firmware

---

**Step 1: Set up Docker's apt repository**
```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

**Step 2: Install Docker packages**
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

**Step 3: Post-installation steps (Run Docker without sudo)**
```bash
# Create docker group (if not exists)
sudo groupadd docker

# Add your user to the docker group
sudo usermod -aG docker $USER

# Activate the changes to groups
newgrp docker
```

**Step 4: Verify Docker Installation**
```bash
# Should print Hello From Docker!
docker run hello-world
```

#### On Windows/macOS:
Download and install **Docker Desktop** from:  
👉 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

---

## 🔌 Step 2: Flash ESP32 Firmware

Before running the Docker container, you need to flash the micro-ROS firmware to your ESP32.

### 2.1 Install Arduino IDE

Download and install Arduino IDE from [arduino.cc/en/software](https://www.arduino.cc/en/software)

### 2.2 Install micro_ros_arduino Library

1. Open Arduino IDE
2. Go to `Sketch` → `Include Library` → `Manage Libraries...`
3. Search for **micro_ros_arduino**
4. Click **Install**

### 2.3 Flash the Firmware

1. Clone this repository (if not already done):
   ```bash
   git clone https://github.com/MechaMind-Labs/microros-gesture-robot.git Gesture_Controlled_Robot
   cd Gesture_Controlled_Robot
   ```

2. Open the firmware file in Arduino IDE:
   ```
   imu_visualizer/firmware/micro_ros_imu/micro_ros_imu.ino
   ```

3. Connect your **ESP32** to your computer via USB

4. In Arduino IDE, configure:
   - **Board:** ESP32 Dev Module (Tools → Board)
   - **Port:** Select the correct COM/USB port (Tools → Port)
   - **Upload Speed:** 115200 (Tools → Upload Speed)

5. Click **Upload** (→) button to flash the firmware

6. Wait for "Done uploading" message

---

## 🔍 Step 3: Identify USB Device

After flashing, keep the ESP32 connected and identify its device path:

```bash
# List all USB serial devices
ls /dev/ttyUSB*
# OR
ls /dev/ttyACM*

# Alternatively, see detailed USB device info
ls -l /dev/serial/by-id/
```

**Common device paths:**
- `/dev/ttyUSB0` (most common for ESP32)
- `/dev/ttyACM0`
- `/dev/ttyUSB1` (if multiple devices connected)

📝 **Note:** Remember your device path - you'll need it in the next step!

---

## 🚀 Step 4: Run Docker Container

### 4.1 Allow Docker to Access Display (for RViz)

```bash
xhost +local:docker
```

### 4.2 Pull and Run the Docker Image

Replace `/dev/ttyUSB0` with your actual device path from Step 3:

```bash
docker run -it --rm \
  --name imu_gesture_control_robot \
  --network host \
  --device=/dev/ttyUSB0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  curiousutkarsh/imu_gesture_control_robot:humble bash
```

**Command Breakdown:**
- `--name imu_gesture_control_robot` → Container name
- `--network host` → Share host network for ROS 2 communication
- `--device=/dev/ttyUSB0` → Pass USB device to container
- `-e DISPLAY=$DISPLAY` → Enable GUI applications (RViz)
- `-v /tmp/.X11-unix:/tmp/.X11-unix:rw` → X11 socket for display

---

## 🎮 Step 5: Run the Project Inside Docker

Once inside the container, you'll see a bash prompt. The workspace is pre-built and ready to use!

### Option A: Full Gesture Control Robot 🤖

Open **3 terminal windows** and run these commands:

#### Terminal 1: Start micro-ROS Agent
```bash
# Inside Docker container
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```
**Then press the RESET button on your ESP32**

#### Terminal 2: Launch Simulated Robot
```bash
# Open a new terminal and attach to the running container
docker exec -it imu_gesture_control_robot bash
```
```bash
# Inside the new terminal
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch bot_bringup simulated_robot.launch.py
```

#### Terminal 3: Run IMU Controller
```bash
# Open another terminal and attach to the container
docker exec -it imu_gesture_control_robot bash
```
```bash
# Inside the terminal
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer imu_controller.launch.py
```

🎉 **Now control your robot with hand gestures!**

---

### Option B: IMU Cube Visualization Only 📊

If you just want to visualize IMU orientation without robot control:

#### Terminal 1: Start micro-ROS Agent
```bash
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```
**Press RESET on ESP32**

#### Terminal 2: Launch RViz Visualization
```bash
# In a new attached terminal
docker exec -it imu_gesture_control_robot bash
```
```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer view_imu.launch.py
```

👉 Watch your IMU orientation in real-time in RViz!

---

## 🔄 Managing Docker Container

### Stop the Container:
```bash
docker stop imu_gesture_control_robot
```

### Restart the Container:
```bash
docker start imu_gesture_control_robot
docker exec -it imu_gesture_control_robot bash
```

### Remove the Container:
```bash
docker stop imu_gesture_control_robot
docker rm imu_gesture_control_robot
```

### Pull Latest Image:
```bash
docker pull curiousutkarsh/imu_gesture_control_robot:humble
```

---

# 💻 Manual Installation on Local PC

If you prefer to set up everything manually on your local machine, follow these comprehensive steps.

## Prerequisites

- **Ubuntu 22.04** (or compatible Linux distribution)
- **ROS 2 Humble** installed
- **ESP32** with MPU6050 sensor
- **Arduino IDE**

---

## 📦 Step 1: Install System Dependencies

```bash
cd ~
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y \
    git \
    python3-rosdep \
    python3-colcon-common-extensions \
    python3-pip \
    default-jre

# Initialize rosdep if not already done
sudo apt install python3-rosdep -y
sudo rosdep init
rosdep update
```

---

## 📥 Step 2: Clone the Repository

```bash
cd ~
git clone https://github.com/MechaMind-Labs/microros-gesture-robot.git Gesture_Controlled_Robot
```

---

## 🏗️ Step 3: Set Up Gesture Control Workspace

### 3.1 Create Workspace
```bash
mkdir -p ~/gesture_ws/src
```

### 3.2 Move Packages
```bash
mv Gesture_Controlled_Robot/* ~/gesture_ws/src/
rm -rf Gesture_Controlled_Robot
```

### 3.3 Install Dependencies
```bash
cd ~/gesture_ws
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### 3.4 Build Workspace
```bash
colcon build
source install/setup.bash
```

---

## 🔧 Step 4: Set Up micro-ROS

### 4.1 Source ROS 2 Environment
```bash
cd ~
source /opt/ros/humble/setup.bash
```

### 4.2 Create micro-ROS Workspace
```bash
mkdir -p ~/microros_ws/src
cd ~/microros_ws
git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
```

### 4.3 Install Dependencies
```bash
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -y
sudo apt-get install python3-pip -y
```

### 4.4 Build micro-ROS Tools
```bash
colcon build
source install/local_setup.bash
```

### 4.5 Create Firmware Workspace
```bash
ros2 run micro_ros_setup create_firmware_ws.sh host
```

### 4.6 Build Firmware
```bash
ros2 run micro_ros_setup build_firmware.sh
source install/local_setup.bash
```

### 4.7 Create Agent Workspace
```bash
ros2 run micro_ros_setup create_agent_ws.sh
```

### 4.8 Build micro-ROS Agent
```bash
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash
```

---

## ⚡ Step 5: Flash ESP32 Firmware

### 5.1 Install Arduino IDE & micro_ros_arduino

Follow the same instructions as in the Docker section ([Step 2](#-step-2-flash-esp32-firmware))

### 5.2 Flash the Firmware
```bash
# Open the firmware file in Arduino IDE
# Path: ~/gesture_ws/src/imu_visualizer/firmware/micro_ros_imu/micro_ros_imu.ino
```

Follow the Arduino IDE flashing procedure from the Docker section.

---

## 🔧 Step 6: Configure Environment

Add ROS 2 setup to your `.bashrc`:

```bash
cd ~
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=1" >> ~/.bashrc
source ~/.bashrc
```

---

## 🎮 Step 7: Run the Project

### Option A: Full Gesture Control Robot 🤖

Open **3 terminal windows**:

#### Terminal 1: micro-ROS Agent
```bash
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```
**Press RESET on ESP32**

#### Terminal 2: Simulated Robot
```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch bot_bringup simulated_robot.launch.py
```

#### Terminal 3: IMU Controller
```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer imu_controller.launch.py
```

---

### Option B: IMU Visualization Only 📊

#### Terminal 1: micro-ROS Agent
```bash
source ~/.bashrc
cd ~/microros_ws
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```
**Press RESET on ESP32**

#### Terminal 2: RViz Visualization
```bash
source ~/.bashrc
cd ~/gesture_ws
source install/setup.bash
ros2 launch imu_visualizer view_imu.launch.py
```

---

## 📊 Optional: Telemetry Viewer Setup

For advanced data visualization:

### Install Java
```bash
sudo apt install default-jre -y
```

### Download Telemetry Viewer
Download `TelemetryViewer.jar` from [FarrellF](http://www.farrellf.com/TelemetryViewer/)

### Run Telemetry Viewer
```bash
java -jar TelemetryViewer.jar
```

Configure serial port (e.g., `/dev/ttyUSB0`) and baud rate (`115200` or `921600`).

---

# ⚠️ Troubleshooting

## Common Issues and Solutions

### 🔴 No IMU Data Received

**Symptoms:** RViz shows no movement, terminal shows no data

**Solutions:**
1. Check MPU6050 wiring (SDA → GPIO21, SCL → GPIO22)
2. Verify 3.3V power supply (NOT 5V!)
3. Press RESET button on ESP32 after starting micro-ROS agent
4. Check baud rate is 115200 in both firmware and agent

### 🔴 Permission Denied on `/dev/ttyUSB0`

**Error:** `Permission denied: '/dev/ttyUSB0'`

**Solution:**
```bash
# Add your user to dialout group
sudo usermod -a -G dialout $USER

# For Docker users, also add to tty group
sudo usermod -a -G tty $USER

# Log out and log back in for changes to take effect
```

### 🔴 IMU Outputs All Zeros

**Symptoms:** IMU publishes data but all values are 0

**Solutions:**
1. Check MPU6050 VCC is connected to 3.3V (NOT 5V)
2. Verify I2C address (default: 0x68, alternative: 0x69)
3. Test with I2C scanner sketch
4. Check for loose connections

### 🔴 Docker: Cannot Connect to Display

**Error:** `cannot open display: :0`

**Solution:**
```bash
# Run this before starting container
xhost +local:docker

# If still failing, try:
xhost +
```

### 🔴 Docker: USB Device Not Found

**Error:** Device `/dev/ttyUSB0` not found in container

**Solutions:**
1. Verify device path on host: `ls /dev/ttyUSB*`
2. Make sure ESP32 is connected before starting container
3. Use correct device path in `--device` flag
4. Check USB cable is data-capable (not charge-only)

### 🔴 ROS 2 Agent Can't Find Device

**Error:** `Failed to open serial port`

**Solutions:**
```bash
# Check available ports
ls -l /dev/ttyUSB*
ls -l /dev/ttyACM*

# Check if device is recognized
dmesg | grep tty

# Try different baud rates
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200
```

### 🔴 Build Failures

**Error:** Package build failures during `colcon build`

**Solutions:**
```bash
# Update dependencies
cd ~/gesture_ws  # or ~/microros_ws
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Clean and rebuild
rm -rf build/ install/ log/
colcon build
```

### 🔴 Arduino Upload Fails

**Error:** Cannot upload to ESP32

**Solutions:**
1. Hold BOOT button while uploading
2. Check correct board selected (ESP32 Dev Module)
3. Lower upload speed to 115200
4. Try different USB cable
5. Install CH340 or CP2102 drivers if needed

---

## 🐛 Getting More Help

If you encounter issues not covered here:

1. Check existing [GitHub Issues](https://github.com/MechaMind-Labs/microros-gesture-robot/issues)
2. Enable verbose output:
   ```bash
   ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -v6
   ```
3. Check ROS 2 topics:
   ```bash
   ros2 topic list
   ros2 topic echo /imu/data
   ```
4. Monitor serial output from ESP32:
   - Arduino IDE → Tools → Serial Monitor
   - Set baud rate to 115200

---

# 📚 References

## Official Documentation
- 🌐 [micro-ROS Tutorials](https://micro.ros.org/docs/tutorials/core/first_application_linux/)
- 🌐 [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/index.html)
- 🌐 [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- 🌐 [MPU6050 Datasheet](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)

## Libraries & Tools
- 📦 [micro_ros_arduino](https://github.com/micro-ROS/micro_ros_arduino)
- 📦 [micro_ros_setup](https://github.com/micro-ROS/micro_ros_setup)
- 🔧 [Docker Documentation](https://docs.docker.com/)

## Tutorials
- 📖 [Docker Installation Guide](https://docs.docker.com/engine/install/ubuntu/)
- 📖 [ROS 2 Installation](https://docs.ros.org/en/humble/Installation.html)
- 📖 [Arduino IDE Setup](https://www.arduino.cc/en/Guide)

---

# 🙌 Credits & Contribution

**Maintained by:** [Curious-Utkarsh](https://github.com/Curious-Utkarsh)

**Contributors Welcome!** 🎉

If you'd like to contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# 📄 License

This project is open-source and available under the MIT License.

---

# ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 🤝 **Contributing** to the codebase

---

✨ **You've built your own Gesture Controlled Robot with ESP32 + micro-ROS + ROS 2!** ✨

Happy Building! 🚀🤖
