import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import base64
from io import BytesIO
from PIL import Image, ImageTk
import tempfile
import os
from icon import ICON

class ImageMessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dr. Mythic Steganography v1.0")
        self.root.geometry("500x380")  # Adjusted size
        
        # Center the main window
        self.center_window(self.root)
        
        # Set custom icon for Windows
        try:
            # Create a temporary icon file
            icon_data = base64.b64decode(ICON.replace('\n', '').strip())
            
            # Create temporary file with .ico extension
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ico') as icon_file:
                icon_file.write(icon_data)
                icon_file.flush()
                
                # Set window icon
                self.root.iconbitmap(icon_file.name)
                
            # Clean up the temporary file
            try:
                os.unlink(icon_file.name)
            except:
                pass
                
        except Exception as e:
            print(f"Failed to load icon: {e}")
            # Program will continue without custom icon
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')  # Using 'clam' theme for a modern look
        
        # Configure styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        
        # Configure main window
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)  # Fixed window size
        
        # Create and configure main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Hide Secret Messages in Images", 
                              font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Message Entry Frame
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(message_frame, text="Enter your secret message:").pack(anchor=tk.W)
        self.message_text = tk.Text(message_frame, height=5, width=45, 
                                  font=('Segoe UI', 10),
                                  relief='solid', borderwidth=1)
        self.message_text.pack(pady=(5, 0), fill=tk.X)
        
        # File Selection Frame
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Selected Image:").pack(anchor=tk.W)
        self.file_label = ttk.Label(file_frame, text="No file selected",
                                  font=('Segoe UI', 9, 'italic'))
        self.file_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Style for primary button
        style.configure('Primary.TButton', background='#007bff', foreground='white')
        
        # Create buttons with equal width and proper spacing
        browse_btn = ttk.Button(button_frame, text="Browse Image", 
                              command=self.browse_file, width=20)
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        write_btn = ttk.Button(button_frame, text="Write Message", 
                             command=self.write_message, width=20)
        write_btn.pack(side=tk.RIGHT)
        
        read_btn = ttk.Button(main_frame, text="Read Message", 
                            command=self.read_message, width=42)
        read_btn.pack(pady=10)
        
        self.selected_file = None

    def center_window(self, window):
        """Center a tkinter window on the screen"""
        window.update_idletasks()
        
        # Get window size
        width = window.winfo_width()
        height = window.winfo_height()
        
        # Get screen size
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f'+{x}+{y}')

    def browse_file(self):
        filetypes = (
            ('JPEG files', '*.jpg;*.jpeg'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.selected_file = filename
            self.file_label.config(text=filename)

    def write_message(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image file first!")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide!")
            return
            
        try:
            with open(self.selected_file, 'ab') as file:
                file.write(b"\n===SECRET_MESSAGE_START===\n")
                file.write(message.encode())
                file.write(b"\n===SECRET_MESSAGE_END===")
            
            messagebox.showinfo("Success", "Message hidden successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def read_message(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image file first!")
            return
            
        try:
            with open(self.selected_file, 'rb') as file:
                content = file.read()
                try:
                    # Find the message between markers
                    start_marker = b"===SECRET_MESSAGE_START==="
                    end_marker = b"===SECRET_MESSAGE_END==="
                    
                    start_idx = content.find(start_marker)
                    if start_idx == -1:
                        messagebox.showinfo("Info", "No hidden message found in this image!")
                        return
                        
                    end_idx = content.find(end_marker)
                    if end_idx == -1:
                        messagebox.showinfo("Info", "No hidden message found in this image!")
                        return
                    
                    # Extract and decode the message
                    message = content[start_idx + len(start_marker):end_idx].decode().strip()
                    
                    # Show message in a new window
                    self.show_message_window(message)
                    
                except Exception as e:
                    messagebox.showerror("Error", "Failed to decode the message!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_message_window(self, message):
        top = tk.Toplevel(self.root)
        top.title("Hidden Message")
        top.geometry("400x300")
        top.configure(bg='#f0f0f0')
        top.resizable(False, False)
        
        # Make the window transient and grab focus
        top.transient(self.root)
        top.grab_set()
        
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Hidden message found:", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        text_widget = tk.Text(frame, height=10, width=40, 
                            font=('Segoe UI', 10),
                            relief='solid', borderwidth=1)
        text_widget.pack(pady=(10, 15), fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", message)
        text_widget.config(state='disabled')
        
        ttk.Button(frame, text="Close", command=top.destroy, 
                  width=20).pack()
        
        # Center the message window relative to main window
        top.update_idletasks()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        width = top.winfo_width()
        height = top.winfo_height()
        
        # Position message window centered above main window
        x = main_x + (main_width - width) // 2
        y = main_y - height - 10  # 10 pixels gap
        
        # If would appear off top of screen, show below main window instead
        if y < 0:
            y = main_y + main_height + 10
            
        top.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageMessageApp(root)
    root.mainloop() 