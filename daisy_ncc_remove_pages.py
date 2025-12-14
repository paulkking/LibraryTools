"""
Interface for removing all page numbers in DAISY 2 NCC by removing spans
Used to correct an issue with DAISYs that use the same reference to heading + first page which can cause errors
An alternative would be to remove only the first page under each heading, but consulting with user groups indicated this would be confusing.
"""

from bs4 import BeautifulSoup as bs

def removePages(ncc): # use file (as TextIOWrapper) as argument directly
    soup = bs(ncc,'html.parser')
    for span_tag in soup.find_all('span'):
        span_tag.replace_with('')

    return str(soup.prettify())
    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilename(title="Please select an NCC file:")
    if not file.endswith("ncc.html"):
        raise Exception("Filename must be 'ncc.html'")

    with open(file, encoding='UTF-8') as f:
        out = removePages(f)
        
    file2 = filedialog.asksaveasfile(title="Select a filename to save to:")
    with open(file2.name,"w",encoding='UTF-8') as f:
        f.write(out)