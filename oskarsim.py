#!/usr/bin/env python3

import numpy
import oskar
import scipy.io
import os

def run_oskar_simulation(timeseries, # Flux sequence
    telescope_model, # e.g., "xxx.tm"
    T, # second
    num_snap,
    RA, # deg
    Dec, # deg
    nfreq, # e.g., numpy.array([1,256,512,768,1024])
    start_frequency_hz,
    frequency_inc_hz,
    phase_centre_ra_deg,
    phase_centre_dec_deg,
    start_h,
    precision="single"):

    sky_data = numpy.zeros((num_snap,12))
    sky_data[:,0] = RA
    sky_data[:,1] = Dec
    sky_data[:,2] = timeseries[0,:]

    for indfrq in range(len(nfreq)):
        for t in range(num_snap):
            a = (t*T) % 60
            b = ((t*T-a)/60) % 60
            c = (t*T-a-b*60)/60/60
    
            # Basic settings.
            params1 = {
                "simulator": {
                    "use_gpus": True
                },
                "observation" : {
                    "num_channels": nfreq[indfrq],
                    "start_frequency_hz": start_frequency_hz,
                    "frequency_inc_hz": frequency_inc_hz,
                    "phase_centre_ra_deg": phase_centre_ra_deg,
                    "phase_centre_dec_deg": phase_centre_dec_deg,
                    "num_time_steps": 1,
                    "start_time_utc": "01-01-2000 "+str(int(start_h)+c)+":"+str(b)+":"+str(a),
                    "length": T
                },
                "telescope": {
                    "input_directory": telescope_model,
                    "station_type": "Isotropic beam"
                },
                "interferometer": {
                    "noise/enable": False,
                    "ms_filename": "snap_"+str(nfreq[indfrq])+"_"+str(t)+".ms"
                }
            }

            settings1 = oskar.SettingsTree("oskar_sim_interferometer")
            settings1.from_dict(params1)
    
            if precision == "single":
                settings1["simulator/double_precision"] = False

            sky_data1 = sky_data[t]
            sky1 = oskar.Sky.from_array(sky_data1, precision)

            sim1 = oskar.Interferometer(settings=settings1)
            sim1.set_sky_model(sky1)
            sim1.run()

Data1 = scipy.io.loadmat('J2251_aa2.mat')
timeseries = Data1['sim_flux2']
timeseries = numpy.array(timeseries)
precision = "single"

run_oskar_simulation(timeseries,
    telescope_model="aa2.tm",
    T=0.125, # second
    num_snap=100,
    RA=-17.0667, # deg
    Dec=-37.1967, # deg
    nfreq=numpy.array([1,256,512,768,1024]), # e.g., numpy.array([1,256,512,768,1024])
    start_frequency_hz=1382000000,
    frequency_inc_hz=100000,
    phase_centre_ra_deg=-17.0667,
    phase_centre_dec_deg=-37.1967,
    start_h=19,
    precision="single")
