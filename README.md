PDF Splitter
===================
Justin Vecchio

Justin@JustinVec.com

----------

I developed this tool to address a recurring workflow bottleneck. Our team was spending more time than ideal manually splitting large PDF files for another department, which introduced avoidable labor costs and potentially slowed down overall project turnaround. By automating the splitting process based on the table of contents, this solution helps reduce manual effort and significantly speeds up the delivery of finalized files to the department.

Features
----------

-   Extracts and filters TOC entries using `PyMuPDF`

-   Splits PDF pages using `PyPDF2` based on TOC titles



How to Use
-------------

1.  Launch the app (this is if you are running the script directly, I created an exe file so skipt to number two if you are using the PDF.exe):

    `python pdf_splitter.py`

2.  In the GUI:

    -   Click **"Browse"** to select the PDF file.

    -   Choose an output folder.

    -   Specify the TOC level (e.g., 1 for first-level headings). Set to `0` to use **all levels**.

    -   Click **"Split PDF"** to generate individual files.

3.  Output PDFs will be saved in the selected folder with filenames derived from TOC titles.

* * * * *

Packaging
-------------------------------------------

These are the steps I followed to create a standalone .exe of the application to share with transportation dept.

### 1\. Install PyInstaller

`pip install pyinstaller`

### 2\. Create PyInstaller Configuration in PyCharm

-   Go to **Run > Edit Configurations**.

-   Add a new **Python** configuration.

-   Name it `Package with PyInstaller`.

-   Set `Script path` to the file containing your main function (e.g., `pdf_splitter.py`).

-   In **Parameters**, add:

    `-F -w pdf_splitter.py`

    -   `-F`: Create a single-file executable

    -   `-w`: Hide the terminal window (for GUI apps)

### 3\. Run the Configuration

-   Run the config from PyCharm.

-   After completion, the `.exe` file will be located in the `dist/` directory.


Known Issues
---------------

-   Some PDFs may not contain extractable TOC metadata.

-   Title collisions may overwrite output files if not unique.

* * * * *

Project Structure
--------------------
`PDF.py       
dist/
└── PDF.exe`

* * * * *

