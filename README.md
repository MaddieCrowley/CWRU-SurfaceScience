# CWRU-SurfaceScience

The python code in this project enables usage of the Surface Science experiment in the CWRU Advanced Labs with a (hopefully) more ledgible and comprehensible code than the old LabView virtual instrument. 

The code contains a large quantity of comments explaining what each line (or set of lines) does and why. However, overall the code should be quite ledgible.

The program is quite dependent on the nidaqmx package which enables commmunication with the National Instruments DAQ used in the experiment. So, I highly recommend reading the documentation for that package for full understanding of that API's function and the code surrounding ite. A large other contributer was the documentation for the matplotlib animation function, which is quite powerful but enables live plotting of functions as the data gets collected. However, it requires the use of iterators in order to function, in particular, the [decay example](https://matplotlib.org/stable/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py) was quite critical for proper writing of the code. I have included a short writeup of both these subjects on the [wiki](https://github.com/LiamCrowley/CWRU-SurfaceScience/wiki) for this project.

The code has some oddities with how it is written predominantly due to me being a physicist and engineer and not a computer scientist. Also, since most of my programming background is Verilog and C++, the code structure is colored by those languages. 

If you have any improvements or questions, feel free to reach out to me! Madeline Crowley (***REMOVED***) 

A previous attempt at this project that was abandoned in favor of completely rewriting the code from scratch can be found [here](https://github.com/LiamCrowley/SurfaceSciencePython). This was were a large amount of the testing of the DAQ code and packages/API was done.
