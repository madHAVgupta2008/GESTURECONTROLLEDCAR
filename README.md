# 🚗 Gesture Controlled Car using AI & Computer Vision

This project presents an intelligent gesture-controlled robotic car that uses computer vision and machine learning to enable touchless control. The system detects hand gestures in real-time using a webcam and translates them into movement commands for a car controlled by Arduino.

The project integrates OpenCV and MediaPipe for hand tracking, along with a trained machine learning model for gesture classification. It also includes advanced features such as speed control based on hand distance and safety mechanisms like automatic stopping when no hand is detected or when the user's eyes are closed.

---

## 🔥 Key Features

- ✋ Real-time hand gesture recognition  
- 🤖 Machine learning-based gesture classification  
- 🚗 Direction control (Forward, Left, Right, Stop)  
- ⚡ Speed control using hand distance  
- 👁️ Eye detection for safety (auto stop + LED alert)  
- 🛑 Auto stop when no hand is detected  
- 🔄 Smooth movement using filtering techniques  
- 📡 Serial communication between Python and Arduino  

---

## 🧠 Technologies Used

- Python  
- OpenCV  
- MediaPipe  
- Scikit-learn (Random Forest Classifier)  
- Arduino (C/C++)  
- L298N Motor Driver  

---

## ⚙️ Working Principle

1. Webcam captures real-time video input  
2. MediaPipe detects hand landmarks  
3. Extracted data is fed into a trained ML model  
4. Model predicts gesture (Forward, Left, Right, Stop)  
5. Hand distance controls speed  
6. Commands are sent via serial communication to Arduino  
7. Arduino controls motors using L298N driver  
8. Safety features override movement when needed  

---

## 🛡️ Safety Features

- Stops automatically if no hand is detected  
- Stops if eyes are closed (driver monitoring)  
- LED indicator for stop condition  

---

## 📁 Project Structure
Gesture_Car_Project/
├── dataset.py
├── train_model.py
├── control_car.py
├── model.pkl
├── data.csv
├── gesture_car.ino / PlatformIO code


---

## 🚀 Applications

- Assistive technology (touchless control systems)  
- Robotics and automation  
- Human-computer interaction systems  
- Smart vehicles and safety systems  

---

## 🏆 Conclusion

This project demonstrates the integration of AI, computer vision, and embedded systems to create an intuitive and safe human-machine interface. It highlights the potential of gesture-based control systems in modern robotics and automation.

---
