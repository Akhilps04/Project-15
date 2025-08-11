# Bio-Signal Generator with Arduino Integration
 Bio-Signal Generator & Real-Time Visualizer (ECG) with Arduino Integration

## 📌 Overview
A desktop application to:
1. **Generate synthetic ECG signals**
2. **Visualize them in real time**
3. **Send data to an Arduino** via serial communication

Developed in Python with **Tkinter**, **Matplotlib**, and **PySerial**.

---

## 🎯 Why This Approach?
Instead of relying on AI APIs or LLMs, the ECG signal is **math-generated** using NumPy, ensuring:
- Full offline functionality
- Complete waveform control
- Easy customization and extension

---

##  🛠 Features
- **Customizable ECG Generation**
  - Sampling rate (Hz)
  - Signal length
  - Heart rate (BPM)
  - Noise level
- **Static & Real-Time Visualization**
  - Black background, bright green signal (hospital-style)
  - Smooth scrolling (updates every 50 ms)
- **Arduino Serial Communication**
  - Send ECG data to a connected Arduino
  - Safe error handling and connection checks
- **Data Export**
  - Save as CSV or PNG
- **Port Detection**
  - Lists available serial ports
- **Threaded Sending**
  - Keeps GUI responsive during data transmission

---

## 📂 GUI Layout
- **Configuration Panel** – Input ECG parameters & serial settings
- **Control Buttons**
  - Generate & Plot
  - Start/Stop Real-time
  - Export CSV/Image
  - Send to Arduino
  - Check Ports
- **Plot Area** – Matplotlib plot embedded in Tkinter

---

## 📜 How It Works
1. **Generate ECG**  
   ```python
   t = np.linspace(0, length / fs, length)
   ecg = np.sin(2 * np.pi * (heart_rate / 60) * t)
   ecg += np.random.normal(0, noise, length)
2. Real-Time Mode
   - Show 200 samples at a time
  -  Slide window forward by 2 samples per frame
3. Send to Arduino
   - Open serial port
   - Transmit ECG values line-by-line
   - Close port after sending

---

## 🚀 Running the Application
python ecg_generator.py
pip install matplotlib numpy pyserial

## 🔮 Future Improvements
   - Use real ECG datasets
   - Gender and age-based waveform variations
   - AI classification of ECG patterns
   - Live streaming from ECG sensors

---

# Acknowledgments
Thanks to Apple and Berry Pvt for giving this task

---

## 📄 License
This project is for practical and demonstration purposes only. Please credit the authors if reused or modified.

---
<img width="920" height="544" alt="image" src="https://github.com/user-attachments/assets/6d741a14-2654-4f7c-a62d-4f9e0e1b197b" />

<img width="1535" height="815" alt="Screenshot 2025-08-11 205505" src="https://github.com/user-attachments/assets/79dd4b6e-4d1e-4398-8789-a2f9aba09489" />

<img width="1497" height="838" alt="Screenshot 2025-08-11 205432" src="https://github.com/user-attachments/assets/62064364-bea7-489e-bee4-66ee41036186" />


