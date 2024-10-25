import tkinter as tk
from tkinter import ttk, filedialog
import os
from PIL import Image
from pydub import AudioSegment
import subprocess
from tkinter import messagebox

VTAToggle = False
Image.MAX_IMAGE_PIXELS = None

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter App")
        self.root.geometry("400x500")

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Image Converter", command=self.show_image_converter)
        self.file_menu.add_command(label="Audio Converter", command=self.show_audio_converter)
        self.file_menu.add_command(label="Video Converter", command=self.show_video_converter)
        self.file_menu.add_command(label="Video to Audio Converter", command=self.show_audio_to_video_converter)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.converter_frame = ttk.Frame(root)
        self.converter_frame.pack()

        self.input_listbox = None
        self.output_listbox = None
        self.selected_files_listbox = None

        self.select_file_button = None
        self.select_directory_button = None
        self.convert_button = None

        self.selected_input_files = []
        self.selected_output_format = None

    def clear_frame(self):
        for widget in self.converter_frame.winfo_children():
            widget.destroy()

    def show_video_converter(self):
        self.clear_frame()
        input_formats = ['mp4', 'mkv', 'mov']
        output_formats = ['mp4', 'mkv', 'mov']
        self.create_converter_ui(input_formats, output_formats)

    def show_image_converter(self):
        self.clear_frame()
        input_formats = ['jpg', 'jpeg', 'png', 'gif', 'tga', 'ico', 'webp']
        output_formats = ['jpg', 'jpeg', 'png', 'gif', 'tga', 'ico', 'webp']
        self.create_converter_ui(input_formats, output_formats)

    def show_audio_converter(self):
        self.clear_frame()
        input_formats = ['mp3', 'wav', 'ogg']
        output_formats = ['mp3', 'wav', 'ogg']
        self.create_converter_ui(input_formats, output_formats)

    def show_audio_to_video_converter(self):
        global VTAToggle
        self.clear_frame()
        input_formats = ['mp4', 'mkv', 'mov']
        output_formats = ['mp3', 'wav', 'ogg']
        self.create_converter_ui(input_formats, output_formats)
        VTAToggle = True

    def create_converter_ui(self, input_formats, output_formats):
        if input_formats is None:
            input_formats = []
        if output_formats is None:
            output_formats = []

        input_output_frame = ttk.Frame(self.converter_frame)
        input_output_frame.pack(side=tk.TOP, padx=5, pady=5)

        button1_frame = ttk.Frame(self.converter_frame)
        button1_frame.pack(side=tk.TOP, padx=5, pady=5)

        file_frame = ttk.Frame(self.converter_frame)
        file_frame.pack(side=tk.TOP, padx=5, pady=5)

        button2_frame = ttk.Frame(self.converter_frame)
        button2_frame.pack(side=tk.TOP, padx=5, pady=5)

        promo_label_frame = ttk.Frame(self.converter_frame)
        promo_label_frame.pack(side=tk.TOP, padx=5, pady=5)

        input_label = tk.Label(input_output_frame, text="Select Input File Types")
        input_label.grid(row=0, column=0, padx=(0, 5))

        output_label = tk.Label(input_output_frame, text="Select Output File Types")
        output_label.grid(row=0, column=1, padx=(0, 5))

        self.input_listbox = tk.Listbox(input_output_frame, selectmode=tk.MULTIPLE, exportselection=False)
        for item in input_formats:
            self.input_listbox.insert(tk.END, item)
        self.input_listbox.grid(row=1, column=0, padx=(0, 5))

        self.output_listbox = tk.Listbox(input_output_frame, selectmode=tk.SINGLE, exportselection=False)
        for item in output_formats:
            self.output_listbox.insert(tk.END, item)
        self.output_listbox.grid(row=1, column=1)

        self.select_file_button = ttk.Button(button1_frame, text="Select a file", command=self.select_input_files)
        self.select_file_button.grid(row=2, column=0, pady=(5, 0))

        self.select_directory_button = ttk.Button(button1_frame, text="Select a directory", command=self.select_input_directory)
        self.select_directory_button.grid(row=2, column=1, pady=(5, 0))

        files_to_convert_label = tk.Label(file_frame, text="Files to Convert")
        files_to_convert_label.pack(pady=(5, 0), padx=(0, 5))

        self.selected_files_listbox = tk.Listbox(file_frame)
        self.selected_files_listbox.pack(pady=(5, 0), padx=(0, 5))

        self.convert_button = ttk.Button(button2_frame, text="Convert", command=self.convert_images)
        self.convert_button.grid(row=5, column=0, pady=(1, 0))

        self.clear_files_button = ttk.Button(button2_frame, text="Clear Files", command=self.clear_selected_files)
        self.clear_files_button.grid(row=5, column=1, pady=(1, 0))

        promo_label = tk.Label(promo_label_frame, text="Made By:", anchor="e", background="grey")
        promo_label.pack(side=tk.LEFT)

        square_text = tk.Label(promo_label_frame, text="Square", foreground="cyan", background="grey")
        square_text.pack(side=tk.LEFT)

        zeb_text = tk.Label(promo_label_frame, text="Zeb", foreground="lime green", background="grey")
        zeb_text.pack(side=tk.LEFT)

    def clear_selected_files(self):
        self.selected_files_listbox.delete(0, tk.END)

    def select_input_files(self):
        selected_input = self.input_listbox.curselection()

        if selected_input:
            self.selected_input_files = [self.input_listbox.get(idx) for idx in selected_input]

            file_types = [(f"{ext.upper()} Files", f"*.{ext}") for ext in self.selected_input_files]
            file_dialog_types = [("Allowed Input Types", " ".join([f"*.{ext}" for ext in self.selected_input_files]))]

            file_paths = filedialog.askopenfilenames(
                title="Select Input Files",
                filetypes=file_dialog_types
            )

            self.selected_files_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.selected_files_listbox.insert(tk.END, file_path)

    def select_input_directory(self):
        selected_directory = filedialog.askdirectory(title="Select Input Directory")

        if selected_directory:
            file_list = [f for f in os.listdir(selected_directory) if f.endswith(tuple(self.selected_input_files))]

            self.selected_files_listbox.delete(0, tk.END)
            for file_name in file_list:
                file_path = os.path.join(selected_directory, file_name)
                self.selected_files_listbox.insert(tk.END, file_path)

    def convert_images(self):
        global VTAToggle
        output_format = self.output_listbox.get(self.output_listbox.curselection()[0])
        output_directory = filedialog.askdirectory(title="Select Output Directory")

        if output_format and output_directory:
            for file_path in self.selected_files_listbox.get(0, tk.END):
                if self.selected_input_files[0] in ['jpg', 'jpeg', 'png', 'gif', 'tga', 'ico', 'webp']:
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                    if output_format == 'jpg':
                        self.convert_to_jpg(file_path, output_file_path)
                    else:
                        if os.path.exists(output_file_path):
                            confirmed = self.confirm_overwrite(output_file_path)
                            if not confirmed:
                                return
                        img = Image.open(file_path)
                        img.save(output_file_path, format=output_format)
                        img.close()
                elif self.selected_input_files[0] in ['mp3', 'wav', 'ogg']:
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                    self.convert_audio(file_path, output_file_path, output_directory, output_format)
                elif self.selected_input_files[0] in ['mp4', 'mkv', 'mov']:
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                    self.convert_to_video(file_path, output_directory, output_format)
                elif VTAToggle == True and self.selected_input_files[0] in ['mp4', 'mkv', 'mov']:
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}")
                    self.convert_to_audio(file_path, output_directory, output_format)
                else:
                    print(f"Unsupported input format: {self.selected_input_files[0]}")
                    self.show_popup("Unsupported Format", f"The selected input format '{self.selected_input_files[0]}' is not supported.")
        self.show_popup("Conversion Completed.", f"The converted files have been saved in {output_file_path}")

    def convert_to_jpg(self, input_path, output_path):
        try:
            if os.path.exists(output_path):
                confirmed = self.confirm_overwrite(output_path)
                if not confirmed:
                    return
            img = Image.open(input_path)
            rgb_img = img.convert("RGB")
            rgb_img.save(output_path, format="JPEG")
            img.close()
        except Exception as e:
            print(f"Error converting {input_path} to JPG: {str(e)}")

    def convert_audio(self, input_path, output_path, output_directory, output_format):
        try:
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}")
            if os.path.exists(output_path):
                confirmed = self.confirm_overwrite(output_path)
                if not confirmed:
                    print(f"Conversion canceled by user. Image {input_path} was not converted.")
                    return
            sound = AudioSegment.from_file(input_path)
            sound.export(output_path, format=output_format)
        except Exception as e:
            print(f"Error converting {input_path} to {output_format}: {str(e)}")

    def convert_to_video(self, input_path, output_directory, output_format):
        try:
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}")
            if os.path.exists(output_file_path):
                confirmed = self.confirm_overwrite(output_file_path)
                if not confirmed:
                    return
            subprocess.run(['ffmpeg', '-y', '-i', input_path, output_file_path])
        except Exception as e:
            print(f"Error converting {input_path} to {output_format}: {str(e)}")

    def convert_to_audio(self, input_path, output_directory, output_format):
        global VTAToggle
        try:
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}")
            if os.path.exists(output_file_path):
                confirmed = self.confirm_overwrite(output_file_path)
                if not confirmed:
                    return
            subprocess.run(['ffmpeg', '-y', '-i', input_path, '-vn', '-acodec', 'libvorbis', '-ac', '2', '-ab', '128k', '-ar', '44100', output_file_path])
        except Exception as e:
            print(f"Error converting {input_path} to {output_format}: {str(e)}")
        VTAToggle = False

    def show_popup(self, title, message):
        messagebox.showinfo(title, message)

    def confirm_overwrite(self, file_path):
        response = messagebox.askyesno("File Already Exists", f"A file named '{os.path.basename(file_path)}' already exists.\nDo you want to overwrite it?")
        return response

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()