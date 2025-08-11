import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import serial.tools.list_ports
import time
import threading
import csv
from matplotlib.animation import FuncAnimation

# --- ECG Signal Generator ---
def generate_ecg(length=1000, fs=500, heart_rate=60, noise=0.01):
    t = np.linspace(0, length / fs, length)
    ecg = np.sin(2 * np.pi * (heart_rate / 60) * t)
    ecg += np.random.normal(0, noise, length)
    return t, ecg

# --- Serial Sender Thread ---
def send_to_arduino(data, port='COM5', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        with open("sent_data.txt", "w") as log_file:
            for i, value in enumerate(data):
                line = f"{value:.4f}\n"
                ser.write(line.encode())
                log_file.write(line)
                time.sleep(0.01)
                if i % 100 == 0:
                    print(f"Sent {i}/{len(data)} data points")
        ser.close()
        print("Data sent to Arduino successfully!")
        return True
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return False
    except PermissionError:
        print(f"Permission denied for {port}. Try running as administrator")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- GUI App ---
class ECGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ECG Generator and Sender")

        self.fs = tk.IntVar(value=500)
        self.length = tk.IntVar(value=1000)
        self.hr = tk.IntVar(value=60)
        self.noise = tk.DoubleVar(value=0.01)
        self.port = tk.StringVar(value="COM5")

        self.gender = tk.StringVar(value="Male")
        self.age_group = tk.StringVar(value="Adult")

        # Animation variables
        self.is_animating = False
        self.animation = None
        self.data_index = 0
        self.window_size = 200  # Number of points to show at once
        self.scroll_speed = 50  # Points per second

        self.create_widgets()

    def create_widgets(self):
        config_frame = ttk.LabelFrame(self.root, text="Waveform Settings")
        config_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(config_frame, text="Sample Length").grid(row=0, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.length).grid(row=0, column=1, padx=5)

        ttk.Label(config_frame, text="Heart Rate (BPM)").grid(row=1, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.hr).grid(row=1, column=1, padx=5)

        ttk.Label(config_frame, text="Sampling Rate (Hz)").grid(row=2, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.fs).grid(row=2, column=1, padx=5)

        ttk.Label(config_frame, text="Noise Level").grid(row=3, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.noise).grid(row=3, column=1, padx=5)

        ttk.Label(config_frame, text="Serial Port").grid(row=4, column=0, sticky="w")
        ttk.Entry(config_frame, textvariable=self.port).grid(row=4, column=1, padx=5)

        ttk.Label(config_frame, text="Gender").grid(row=5, column=0, sticky="w")
        gender_menu = ttk.Combobox(config_frame, textvariable=self.gender, values=["Male", "Female", "Other"])
        gender_menu.grid(row=5, column=1, padx=5)

        ttk.Label(config_frame, text="Age Group").grid(row=6, column=0, sticky="w")
        age_menu = ttk.Combobox(config_frame, textvariable=self.age_group, values=["Infant", "Child", "Adult", "Senior"])
        age_menu.grid(row=6, column=1, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Generate & Plot", command=self.plot_ecg).grid(row=0, column=0, pady=2)
        ttk.Button(button_frame, text="Start Real-time", command=self.start_animation).grid(row=1, column=0, pady=2)
        ttk.Button(button_frame, text="Stop Real-time", command=self.stop_animation).grid(row=2, column=0, pady=2)
        ttk.Button(button_frame, text="Export CSV", command=self.export_csv).grid(row=3, column=0, pady=2)
        ttk.Button(button_frame, text="Export Image", command=self.export_image).grid(row=4, column=0, pady=2)
        ttk.Button(button_frame, text="Send to Arduino", command=self.send_serial).grid(row=5, column=0, pady=2)
        ttk.Button(button_frame, text="Check Ports", command=self.check_ports).grid(row=6, column=0, pady=2)

        # Plot area
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Set up the plot for real-time display
        self.ax.set_xlim(0, 4)  # 4 second window
        self.ax.set_ylim(-2, 2)
        self.ax.set_title("Real-time ECG Monitor", color="white", fontsize=14)
        self.ax.set_xlabel("Time (s)", color="white")
        self.ax.set_ylabel("Amplitude (mV)", color="white")
        self.ax.tick_params(colors="white")
        self.ax.grid(True, alpha=0.3)
        
        # Set dark theme
        self.ax.set_facecolor("black")
        self.fig.patch.set_facecolor("black")

        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def plot_ecg(self):
        try:
            t, ecg = generate_ecg(
                length=self.length.get(),
                fs=self.fs.get(),
                heart_rate=self.hr.get(),
                noise=self.noise.get()
            )
            self.t = t
            self.ecg = ecg

            self.ax.clear()
            self.ax.set_facecolor("black")
            self.fig.patch.set_facecolor("black")
            self.ax.plot(t, ecg, color="lime", linewidth=1.5)
            self.ax.set_title("Synthetic ECG", color="white")
            self.ax.set_xlabel("Time (s)", color="white")
            self.ax.set_ylabel("Amplitude", color="white")
            self.ax.tick_params(colors="white")
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
            
            messagebox.showinfo("Success", "ECG signal generated and plotted!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate ECG: {e}")

    def start_animation(self):
        if not hasattr(self, 'ecg'):
            messagebox.showwarning("Warning", "Please generate ECG signal first!")
            return
        
        if self.is_animating:
            return
        
        print("Starting animation...")
        self.is_animating = True
        self.data_index = 0
        
        # Create a longer signal for continuous scrolling
        fs = self.fs.get()
        duration = 30  # 30 seconds of data
        length = fs * duration
        t_long = np.linspace(0, duration, length)
        ecg_long = generate_ecg(length=length, fs=fs, heart_rate=self.hr.get(), noise=self.noise.get())[1]
        
        self.t_long = t_long
        self.ecg_long = ecg_long
        
        print(f"Generated {len(ecg_long)} data points for animation")
        
        # Start the animation using a different approach
        self.animate()
        
    def animate(self):
        if not self.is_animating:
            return
            
        try:
            # Calculate the window of data to display
            window_start = self.data_index
            window_end = min(window_start + self.window_size, len(self.ecg_long))
            
            if window_end >= len(self.ecg_long):
                # Loop back to beginning
                self.data_index = 0
                window_start = 0
                window_end = self.window_size
            
            # Get the data window
            t_window = self.t_long[window_start:window_end]
            ecg_window = self.ecg_long[window_start:window_end]
            
            # Clear and redraw
            self.ax.clear()
            self.ax.set_facecolor("black")
            self.fig.patch.set_facecolor("black")
            
            # Plot the current window
            self.ax.plot(t_window, ecg_window, color="lime", linewidth=2)
            
            # Set up the display
            self.ax.set_xlim(t_window[0], t_window[-1])
            self.ax.set_ylim(-2, 2)
            self.ax.set_title("Real-time ECG Monitor", color="white", fontsize=14)
            self.ax.set_xlabel("Time (s)", color="white")
            self.ax.set_ylabel("Amplitude (mV)", color="white")
            self.ax.tick_params(colors="white")
            self.ax.grid(True, alpha=0.3)
            
            # Add heartbeat indicator
            if len(ecg_window) > 0:
                max_val = np.max(ecg_window)
                if max_val > 1.5:  # Threshold for heartbeat detection
                    self.ax.axhline(y=max_val, color="red", alpha=0.5, linestyle="--")
            
            # Increment the data index for scrolling
            self.data_index += 2  # Adjust speed here
            
            self.canvas.draw()
            
            # Schedule next frame
            self.root.after(50, self.animate)  # 50ms = 20 FPS
            
        except Exception as e:
            print(f"Animation error: {e}")
            self.is_animating = False

    def stop_animation(self):
        self.is_animating = False
        print("Real-time animation stopped!")

    def export_csv(self):
        if hasattr(self, 'ecg'):
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".csv")
                if file_path:
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Time", "ECG"])
                        for i in range(len(self.t)):
                            writer.writerow([self.t[i], self.ecg[i]])
                    messagebox.showinfo("Success", "CSV exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {e}")
        else:
            messagebox.showwarning("Warning", "Please generate ECG signal first!")

    def export_image(self):
        if hasattr(self, 'ecg'):
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".png")
                if file_path:
                    self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("Success", "Image exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export image: {e}")
        else:
            messagebox.showwarning("Warning", "Please generate ECG signal first!")

    def send_serial(self):
        if hasattr(self, 'ecg'):
            def send_thread():
                success = send_to_arduino(self.ecg, self.port.get())
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Data sent to Arduino successfully!"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to send data to Arduino"))
            
            threading.Thread(target=send_thread, daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please generate ECG signal first!")

    def check_ports(self):
        try:
            ports = serial.tools.list_ports.comports()
            port_list = [port.device for port in ports]
            if port_list:
                messagebox.showinfo("Available Ports", f"Available serial ports:\n{chr(10).join(port_list)}")
            else:
                messagebox.showwarning("No Ports", "No serial ports found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check ports: {e}")

# --- Launch App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ECGApp(root)
    root.mainloop()
