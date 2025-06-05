import fitz 
import os
import re
from pathlib import Path
from tkinter import filedialog, messagebox, Tk, Label, Button, IntVar, Spinbox, StringVar, Entry
from tkinter.ttk import Frame
from PyPDF2 import PdfReader, PdfWriter

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def extract_filtered_toc(pdf_path, toc_level=None):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=True)  
    if toc_level:
        toc = [item for item in toc if item[0] == toc_level]
    return toc

def split_pdf_by_toc(pdf_path, output_dir, toc_level=None):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    toc = extract_filtered_toc(pdf_path, toc_level)

    if not toc:
        messagebox.showerror("Error", "No Table of Contents found.")
        return

    seen = set()
    filtered = []
    for level, title, page in toc:
        if title not in seen and 1 <= page <= num_pages:
            seen.add(title)
            filtered.append((title, page - 1))  

    for i, (title, start_page) in enumerate(filtered):
        end_page = filtered[i + 1][1] - 1 if i + 1 < len(filtered) else num_pages - 1
        writer = PdfWriter()
        for p in range(start_page, end_page + 1):
            writer.add_page(reader.pages[p])
        output_filename = sanitize_filename(title) + ".pdf"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "wb") as f_out:
            writer.write(f_out)

    messagebox.showinfo("Success", f"PDF split into {len(filtered)} files.")

class PDFSplitterGUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.init_ui()

    def init_ui(self):
        self.master.title("TWT PDF Splitter")
        self.pack(padx=10, pady=10)

        self.pdf_path = StringVar()
        self.output_dir = StringVar()
        self.toc_level = IntVar(value=0)

        Label(self, text="Select PDF File:").grid(row=0, column=0, sticky='w')
        Entry(self, textvariable=self.pdf_path, width=40).grid(row=0, column=1)
        Button(self, text="Browse", command=self.browse_pdf).grid(row=0, column=2)

        Label(self, text="Output Folder:").grid(row=1, column=0, sticky='w')
        Entry(self, textvariable=self.output_dir, width=40).grid(row=1, column=1)
        Button(self, text="Browse", command=self.browse_output).grid(row=1, column=2)

        Label(self, text="TOC Level (0 = all):").grid(row=2, column=0, sticky='w')
        Spinbox(self, from_=0, to=10, textvariable=self.toc_level, width=5).grid(row=2, column=1, sticky='w')

        Button(self, text="Split PDF", command=self.run_split).grid(row=3, column=1, pady=10)

    def browse_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def run_split(self):
        pdf_path = self.pdf_path.get()
        output_dir = self.output_dir.get()
        toc_level = self.toc_level.get() or None

        if not pdf_path or not output_dir:
            messagebox.showerror("Input Error", "Please select both a PDF and output folder.")
            return

        split_pdf_by_toc(pdf_path, output_dir, toc_level)

def main():
    root = Tk()
    app = PDFSplitterGUI(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
