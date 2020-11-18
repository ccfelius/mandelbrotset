# mandelbrotset

### Required Packages:
numpy<br>
matplotlib<br>
random<br>
time<br>
math<br>
scipy<br>

### Instructions:

Clone the files and make sure you have all required packages installed. Run simulations.py if you want to see the outcomes of simulations for Random Sampling, LHS and Orthogonal sampling.
<b>Note:</b> It may occur that you have to delete the line 'from mandelbrotset.monte import *' and change it to 'from monte import *'. However, some IDE'S require 'from monte import *' (e.g. visual studio) and other 'from mandelbrotset.monte import *' (e.g. pycharm). In any case, make sure that all files are stated in the same folder. This is important as you will need to use functions stated in monte.py.

### Explanations per file
- monte.py <br>
This file contains all functions for estimating the Mandelbrot area: The brute-force estimate of the mandelbrot area, 
the random sampling method, the Latin Hypercube sampling (LHS) method and the orthogonal sampling method.

- plot_mandelbrot.py<br>
When running this file we get the results of figure 2, a visualisation of the mandelbrotset (if we change maxiter on line 14 to 20 we get fig 2a, otherwise with maxiter 100 we get fig 2b) 

- simulation.py <br>
This file contains a set-up for the simulations that are used to determine the values in table 2. It prints the values for every simulation, the total variance, STD and the corresponding confidence intervals.

- plot_samplemethods.py<br>
For figure 3a, b and c run plot_samplemethods.py. To run faster/prevent overloading your computer the file is split into 3 parts and one is meant to run the code per figure and comment out the rest of the code. This is also mentioned in the file itself. 

- Orthogonal.py<br>
This file is intended to test the orthogonal sampling method, if desired. It enables to print the determined blocks and can give a graph of the specified samples.
- LatinHS.py<br>
This file is intended to test the LHS method, if desired. Also it has the ability to print a plot to visualise which samples are taken.
- antithetic.py<br>
This file is intended for the use of antithetic variables. It prints the outcomes for random sampling with antithetic variables as well as the outcomes of all other sampling methods.
- plot_an.py<br>
When running this file we get figure 4. 

- CV.py<br>
This file was intended for control variates. However, this you can neglect this file.
