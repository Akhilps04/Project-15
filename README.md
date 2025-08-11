# Bio-Signal Generator with Arduino Integration

---


```markdown
# Bio-Signal Generator & Real-Time Visualizer (ECG) with Arduino Integration

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
