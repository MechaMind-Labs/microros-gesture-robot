FROM osrf/ros:humble-desktop-full

ENV ROS_WS=/root/gesture_ws
ENV MICROROS_WS=/root/microros_ws
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

# Install base tools
RUN apt update && apt install -y \
    git \
    python3-rosdep \
    python3-colcon-common-extensions \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN rosdep update --rosdistro=humble

# ========== GESTURE WORKSPACE SETUP ==========
# Create gesture workspace and clone repo
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS/src
RUN git clone https://github.com/MechaMind-Labs/Gesture_Controlled_Robot.git .

# Install dependencies and build gesture workspace
WORKDIR $ROS_WS
RUN rosdep install --from-paths src -y --ignore-src --rosdistro=humble || \
    (apt update && rosdep install --from-paths src -y --ignore-src --rosdistro=humble)

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# ========== MICRO-ROS WORKSPACE SETUP ==========
# Step 2: Create micro-ROS workspace & clone tools
WORKDIR /root
RUN mkdir -p $MICROROS_WS/src
WORKDIR $MICROROS_WS
RUN git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Step 3: Install dependencies
RUN apt update && rosdep update && \
    rosdep install --from-paths src --ignore-src -y && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Build micro-ROS tools
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    colcon build && \
    source install/local_setup.bash"

# Steps 5-8: Create firmware workspace, build firmware, create agent, build agent
# Update apt cache before building (required for firmware dependencies)
RUN apt update

# All in one RUN command to maintain sourced environment
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    source install/local_setup.bash && \
    ros2 run micro_ros_setup create_firmware_ws.sh host && \
    ros2 run micro_ros_setup build_firmware.sh && \
    source install/local_setup.bash && \
    ros2 run micro_ros_setup create_agent_ws.sh && \
    ros2 run micro_ros_setup build_agent.sh && \
    source install/local_setup.bash"

# Configure bashrc with ROS Humble setup and ROS Domain ID
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source $ROS_WS/install/setup.bash" >> /root/.bashrc && \
    echo "source $MICROROS_WS/install/setup.bash" >> /root/.bashrc && \
    echo "export ROS_DOMAIN_ID=1" >> /root/.bashrc

WORKDIR /root

CMD ["bash"]