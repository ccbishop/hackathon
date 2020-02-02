import numpy as np
import math
import matplotlib.pyplot as plt
import scipy as sp
import tkinter as tk
from matplotlib import ticker, cm

def electricfield(qs, rs, p, eps=9e9, siunits=False):
  """
  only 2d. who needs a realistic number of dimensions?? not this code.
  qs is a list of charges.
  rs is the location of the charges relative to the origin. 2d vectors.
  p is where the field is being measured.
  the eps and siunits are the same deal as in the rest of this stuff.
  """

  #I don't like wonky units. going to normalize.
  #!!!!fix later
  if siunits==True:
    #q1 = q1/(1.6e-19) #charges in units of electron charge
    #q2 = q2/(1.6e-19)
    eps = eps/9e9 #constant = 1
  elif siunits==False:
    eps = 1
    #use what you want idc but like this gives easier numbers
    pass

  rs = np.asarray(rs)
  p = np.asarray(p)
  field = [0, 0]

  for i in range(len(rs)):
    r = p - rs[i]
    rmag = np.sqrt(r[0]**2+r[1]**2)
    field += eps * qs[i] * r /(rmag**3)
  return field

def plotelectricfieldmag(qs, rs, width = 2, res= 50):
  """

  """
  x, y = np.meshgrid(np.linspace(-width, width, res), np.linspace(-width, width, res))
  fieldgrid = np.zeros((res,res))
  field = 0
  for i in range(len(x)):
    for j in range(len(y)):
      p = [x[i][j], y[i][j]]
      field = electricfield(qs, rs, p)
      fieldmag = np.sqrt(field[0]**2+field[1]**2)
      fieldgrid[i][j] = fieldmag
  plt.contourf(x, y, fieldgrid, locator=ticker.LogLocator(), cmap="Blues")
  plt.colorbar()
  plt.show()

def plotelectricfieldvec(qs, rs, width =2, res=50):
  """
  uses electric field to plot the magnitude of the electric field for a list of particles with charges qs at locations rs. 
  """
  x, y = np.meshgrid(np.linspace(-width, width, res), np.linspace(-width, width, res))
  fieldgrid = np.zeros((res, res))
  field = 0
  gridx = np.zeros((res, res))
  gridy = np.zeros((res, res))
  for i in range(len(x)):
    for j in range(len(y)):
      if [i, j] != [0, 0]:
        p = [x[i][j], y[i][j]]
        field = electricfield(qs, rs, p)
        gridx[i][j] = field[0]
        gridy[i][j] = field[1]

  plt.quiver(x, y, gridx, gridy)
  plt.show()

root = tk.Tk()
root.configure(background = "LightGoldenrod1")

# create a dictionary of key:value pair as radiobutton_value: str_name_to_print
values = {1: "proton", 2: "electron"}
distvalues = {1: [-1, 0], 2: [1, 0], 3: [0, 1], 4: [0, -1], 5: [1, 1], 6: [-1, 1], 7: [-1, -1], 8:[1, -1], 9: [0,0]}

qs = []
rs = []

def choosecharge():
  # update the label widgets using the dictionary
  charge = values[var.get()]
  global qs
  if charge == "proton":
    qs.append(1)
  elif charge == "electron":
    qs.append(-1)
  print(qs)

def plotting():
  global qs
  global rs
  print("q", qs)
  print("r", rs)
  return plotelectricfieldmag(qs, rs)

def vecplotting():
  global qs
  global rs
  print("q", qs)
  print("r", rs)
  return plotelectricfieldvec(qs, rs)

def clear():
  global qs
  global rs
  qs = []
  rs = []
  plt.clf()

def choosedistance():
  global rs
  r = distvalues[var2.get()]
  rs.append(r)
  print(rs)


# define an IntVar
var = tk.IntVar()
var2 = tk.IntVar()

explain = tk.Text(root, width="100", height="7", font=("Century Gothic", 12, "bold"), fg="dark slate gray",bg="LightGoldenrod1")
explain.insert(tk.END, "Select a particle (proton or electron) then select the position of that particle.\nYou can select as many particles as there are position options.\nYou must select a particle for every position you select, and vice versa.\nDo not try to put two particles in the same position.\nTo keep track of what you have clicked, a list of your current charges and positions displays in the command window.\nClicking the 'Clear' button will remove the particles and positions you have selected thus far, and they will not be\nincluded if you click a 'Graph' button again.")
explain.pack(anchor=tk.N)


proton = tk.Radiobutton(root, text="proton", fg="purple4",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var, value=1, command=choosecharge)
proton.pack()

electron = tk.Radiobutton(root, text="electron", fg="green4",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var, value=2, command=choosecharge)
electron.pack()

left = tk.Radiobutton(root, text="[-1, 0]", fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=1, command=choosedistance)
left.pack()

right = tk.Radiobutton(root, text="[1, 0]", fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=2, command=choosedistance)
right.pack()

up = tk.Radiobutton(root, text="[0, 1]",fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=3, command=choosedistance)
up.pack()

down = tk.Radiobutton(root, text="[0, -1]",fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=4, command=choosedistance)
down.pack()

quad1= tk.Radiobutton(root, text="[1, 1]", fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=5, command=choosedistance)
quad1.pack()

quad2 = tk.Radiobutton(root, text="[-1, 1]",fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=6, command=choosedistance)
quad2.pack()

quad3 = tk.Radiobutton(root, text="[-1, -1]",fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=7, command=choosedistance)
quad3.pack()

quad4= tk.Radiobutton(root, text="[1, -1]", fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=8, command=choosedistance)
quad4.pack()

center= tk.Radiobutton(root, text="[0, 0]", fg="dark slate gray",font=("Century Gothic", 12, "bold"), bg = "LightGoldenrod1", variable=var2, value=9, command=choosedistance)
center.pack()

graph = tk.Button(root, text="Graph Scalar E-Field", fg="snow",font=("Century Gothic", 16, "bold"), bg = "dark slate gray", command = plotting)
graph.pack()

vector = tk.Button(root, text="Graph Vector E-Field", fg="snow",font=("Century Gothic", 16, "bold"), bg = "dark slate gray", command = vecplotting)
vector.pack()

clear = tk.Button(root, text="Clear Particles and Graphs", fg="snow",font=("Century Gothic", 16, "bold"), bg = "dark slate gray", command = clear)
clear.pack()

root.mainloop()