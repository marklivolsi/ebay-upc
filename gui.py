from tkinter import *

root = Tk()

prod_details_label = Label(root,
                           text='Product Details',
                           font=('Helvetica', 36),
                           padx=10,
                           pady=10).grid(row=0, column=0, sticky=W)

upc_label = Label(root, text='UPC:', font=('Helvetica', 16), padx=10, pady=5).grid(row=1, column=0, sticky=W)

search_box = Entry(root, font=('Helvetica', 16), width=30).grid(row=0, column=1, sticky=W)
search_upc_btn = Button(root, text='Search UPC', fg='black').grid(row=0, column=2, sticky=W)



root.mainloop()