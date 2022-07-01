from tkinter import Tk, Label, Button, Entry, IntVar, W, filedialog, messagebox
import preProcess as pp
import Clustering as cl

import matplotlib

matplotlib.use('TkAgg')
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class GUI:


##################################################################################################################


        # Change label contents
    def __init__(self, master):

        self.master = master
        master.title("K Means Clustering")
        self.data = None
        self.path = None
        self.is_preprocess = False
        self.cluster_num = IntVar()
        self.run_num = IntVar()
        self.cluster_model = None

        self.total_label_text = IntVar()
        # self.total_label_text.set(self.total) # need to delete this but its a good example
        # self.total_label = Label(master, textvariable=self.total_label_text) # need to delete this but its a good example

        self.label_cluster = Label(master, text="Number of clusters k:")
        self.label_num_of_runs = Label(master, text="Number of runs:")

        vcmd1 = master.register(self.validate) # we have to wrap the command
        vcmd2 = master.register(self.validate) # we have to wrap the command
        self.entry_cluster_num = Entry(master, validate="key", validatecommand=(vcmd1, '%P'),textvariable=self.cluster_num)
        self.entry_run_num = Entry(master, validate="key", validatecommand=(vcmd2, '%P'), textvariable=self.run_num)

        # Create a File Explorer label
        self.label_file_explorer = Label(master, text="File Explorer")

        self.button_explore = Button(master, text="Browse Files", command=self.browseFiles)
        self.button_preprocess = Button(master, text="Pre-process", command=self.preProcess)
        self.button_cluster_maker = Button(master, text="Cluster", command=self.clustering)

        # Grid method is chosen for placing
        # the widgets at respective positions
        # in a table like structure by
        # specifying rows and columns

        self.label_file_explorer.grid(row=0, column=0, sticky=W)
        self.button_explore.grid(column=0, row=1,sticky=W)
        self.label_cluster.grid(column=0, row=2, sticky=W)
        self.entry_cluster_num.grid(column=0, row=3, sticky=W)
        self.label_num_of_runs.grid(column=0, row=4, sticky=W)
        self.entry_run_num.grid(column=0, row=5, sticky=W)
        self.button_preprocess.grid(column=0, row=6, sticky=W)
        self.button_cluster_maker.grid(column=0, row=7, sticky=W)

        # self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        #
        # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        # self.label_file_explorer.grid(column=1, row=1)


        #self.button_exit.grid(column=1, row=6,sticky=E)

        # Let the window wait for any events

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Excel files",
                                                          "*.xlsx*"),
                                                         ("all files",
                                                          "*.*")))
        self.label_file_explorer.configure(text="File Opened: " + filename)
        # set the path
        self.path = filename


    def preProcess(self):
        # check if the file is empty
        is_it_ok = self.check_file()
        # check if the number are ok
        is_it_ok2 = self.check_nums(self.cluster_num, self.run_num)

        if self.path is None:
            messagebox.showinfo(title="K Means Clustering", message="\n You need to select a file first.")
            return
        if is_it_ok is not True:
            messagebox.showinfo(title="K Means Clustering", message="\n You need to select a none empty excel file first.")
            return
        elif is_it_ok2 is not True:
            messagebox.showinfo(title="K Means Clustering", message="\n You must choose number of clusters and number of runs (both bigger then 0 when number of runs is limited to 100 and number of clusters is limited to 40.)")
            return
        self.data = pp.read_xlsx(self.path)
        if self.data is not None:
            self.data = pp.complete_vals(self.data) # filling null values
            self.data = pp.normalization_vals(self.data)
            self.data = pp.group_data(self.data)
            messagebox.showinfo(title="K Means Clustering", message="\n Preprocessing completed successfully!")
            self.is_preprocess = True

        else:
            messagebox.showinfo(title="K Means Clustering", message="\n You need to select a valid excel file.")


    def check_file(self):
        checker = pp.read_xlsx(self.path)
        is_it = checker.empty
        if is_it is True:
            return False
        return True

    def clustering(self):
        is_it_ok2 = self.check_nums(self.cluster_num, self.run_num)
        if self.is_preprocess is not True:
            # checking if we Preprocessed the data
            messagebox.showinfo(title="K Means Clustering", message="\n You must Preprocess the data first")
        elif is_it_ok2 is not True:
            messagebox.showinfo(title="K Means Clustering", message="\n You must choose number of clusters and number of runs (both bigger then 0 when number of runs is limited to 100 and number of clusters is limited to 40.)")
            return
        else:
            self.cluster_model = cl.Kmeans_clus(self.data, self.cluster_num.get(), self.run_num.get())
            pp.export_to_excel(self.cluster_model) # export the new data set into a new excel file
            figure = cl.scatter_plot(self.cluster_model)
            plot_canvas = FigureCanvasTkAgg(figure, master=root)
            plot_canvas.draw()
            plot_canvas.get_tk_widget().grid(row=10, column=1)

            if cl.horopleth_map(self.cluster_model):
                img = Image.open("choropleth.png")
                im_tk = ImageTk.PhotoImage(img.resize((500, 400)))
                tk_canvas = Label(root, image=im_tk)
                tk_canvas.image = im_tk
                tk_canvas.grid(column=0, row=10)
                messagebox.showinfo(title="K Means Clustering",
                                    message="\n The clustering process was successfully completed!")

    def check_nums(self, cluster_num, run_num):
        try:
            c_num = cluster_num.get()
        except:
            return False
        try:
            r_num = run_num.get()
        except:
            return False
        if c_num > 0 and r_num > 0:
            if r_num < 101:
                if c_num < 41:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    root = Tk()
    root.geometry("950x750")

    my_gui = GUI(root)
    root.mainloop()




