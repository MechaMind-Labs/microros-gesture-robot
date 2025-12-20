#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

// Using the standard Imu message type
#include <sensor_msgs/msg/imu.h>

// MPU6050 includes
#include <MPU6050_tockn.h>
#include <Wire.h>

// micro-ROS variables
rcl_publisher_t publisher;
sensor_msgs__msg__Imu msg; // Using Imu message type
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_init_options_t init_options;

// MPU6050 setup
MPU6050 mpu6050(Wire);

// Constants
#define LED_PIN 13
#define ROS_DOMAIN_ID 1
// 1,000,000 microseconds in a second. 1,000,000 / 50 Hz = 20,000 microseconds.
#define PUBLISH_DELAY_MICROSECONDS 20000 

// Error handling macro
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}

void error_loop(){
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void setup() {
  // A high baud rate is crucial for high-frequency data
  Serial.begin(2000000);
  set_microros_transports();

  // Initialize MPU6050
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  
  delay(2000);

  // Standard micro-ROS initialization
  allocator = rcl_get_default_allocator();
  init_options = rcl_get_zero_initialized_init_options();
  RCCHECK(rcl_init_options_init(&init_options, allocator));
  RCCHECK(rcl_init_options_set_domain_id(&init_options, ROS_DOMAIN_ID));
  RCCHECK(rclc_support_init_with_options(&support, 0, NULL, &init_options, &allocator));
  RCCHECK(rclc_node_init_default(&node, "micro_ros_mpu6050_node", "", &support));

  // Initialize the publisher with the Imu message type
  RCCHECK(rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, Imu),
    "imu/data_raw"));

  // --- Pre-configure parts of the message that don't change ---
  // Set the frame_id for the message header.
  msg.header.frame_id.data = "imu_link";
  msg.header.frame_id.size = strlen(msg.header.frame_id.data);
  msg.header.frame_id.capacity = msg.header.frame_id.size + 1;
  
  // Set covariances to indicate orientation is not available.
  msg.orientation_covariance[0] = -1;
}

void loop() {
  static unsigned long last_publish_time = 0;
  static int message_counter = 0;
  
  // Use microseconds for more precise timing at high frequencies
  unsigned long now = micros(); 
  
  // Update MPU6050 data on every loop iteration for fresh values
  mpu6050.update();

  // Check if it's time to publish
  if (now - last_publish_time >= PUBLISH_DELAY_MICROSECONDS) {
    
    // --- Populate the message header with current time ---
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    msg.header.stamp.sec = ts.tv_sec;
    msg.header.stamp.nanosec = ts.tv_nsec;

    // --- Populate Angular Velocity (deg/s to rad/s) ---
    msg.angular_velocity.x = mpu6050.getGyroX() * (PI / 180.0);
    msg.angular_velocity.y = mpu6050.getGyroY() * (PI / 180.0);
    msg.angular_velocity.z = mpu6050.getGyroZ() * (PI / 180.0);

    // --- Populate Linear Acceleration (g's to m/s^2) ---
    msg.linear_acceleration.x = mpu6050.getAccX() * 9.80665;
    msg.linear_acceleration.y = mpu6050.getAccY() * 9.80665;
    msg.linear_acceleration.z = mpu6050.getAccZ() * 9.80665;
    
    // Publish the populated message
    rcl_ret_t ret = rcl_publish(&publisher, &msg, NULL);
    if (ret == RCL_RET_OK) {
      last_publish_time = now;
      
      // Toggle LED every 50 messages (once per second at 50Hz) for feedback
      if (++message_counter >= 50) {
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        message_counter = 0;
      }
    }
  }
}
