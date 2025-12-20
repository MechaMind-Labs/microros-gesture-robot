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
    && rm -rf /var/lib/apt/lists/*

# Create gesture workspace and clone repo first
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS/src
RUN git clone https://github.com/MechaMind-Labs/Gesture_Controlled_Robot.git .

WORKDIR /root

# Create microros workspace and set it up
RUN mkdir -p $MICROROS_WS/src
WORKDIR $MICROROS_WS/src
RUN git clone https://github.com/MechaMind-Labs/Gesture_Controlled_Robot.git .

# Initialize rosdep AFTER cloning
WORKDIR /root
RUN rosdep update --rosdistro=humble

# Install dependencies with proper error handling
WORKDIR $ROS_WS
RUN rosdep install --from-paths src -y --ignore-src --rosdistro=humble || \
    (apt update && rosdep install --from-paths src -y --ignore-src --rosdistro=humble)

# Build workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# Auto-source ROS and workspace
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source $ROS_WS/install/setup.bash" >> /root/.bashrc


WORKDIR $MICROROS_WS
RUN rosdep install --from-paths src -y --ignore-src --rosdistro=humble || \
    (apt update && rosdep install --from-paths src -y --ignore-src --rosdistro=humble)

# Build workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build && \ 
                  source install/local_setup.bash"

RUN ros2 run micro_ros_setup create_firmware_ws.sh host
RUN ros2 run micro_ros_setup create_firmware_ws.sh host
RUN ros2 run micro_ros_setup build_firmware.sh

RUN /bin/bash -c "source install/local_setup.bash"

RUN ros2 run micro_ros_setup create_agent_ws.sh
RUN ros2 run micro_ros_setup build_agent.sh

RUN /bin/bash -c "source install/local_setup.bash"

# Auto-source ROS and workspace
RUN echo "source $MICROROS_WS/install/setup.bash" >> /root/.bashrc && \
    echo "export ROS_DOMAIN_ID=1" >> /root/.bashrc

WORKDIR /root

RUN /bin/bash -c "source /root/.bashrc"

CMD ["bash"]
