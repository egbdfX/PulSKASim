#!/usr/bin/env python3

import numpy
import oskar
import scipy.io
import os
import yaml
from astropy.time import Time
import copy
import subprocess
from pathlib import Path

def run_pyuvsim_simulation(timeseries, # Flux sequence
    telescope_model, # e.g., "MeerKAT_pyuvsim_tm.csv"
    catalog_name,
    telescope_config_name, # e.g. "MeerKAT-gauss-fwhm1.0.yml"
    outdir,
    outfile_template,
    meerkat_yml_file_template, # e.g. "./meerkat_yml/MeerKAT_test_VS_"
    T, # second
    num_snap,
    RA, # deg
    Dec, # deg
    nfreq, # e.g., numpy.array([1,256,512,768,1024])
    start_frequency_hz=1400000000.0,
    frequency_inc_hz=100000.,
    phase_centre_ra_deg = 0.0,
    phase_centre_dec_deg = 0.0,
    start_h=19,
    ncores=4):
    
    
    sky_data = numpy.zeros((num_snap,12))
    sky_data[:,0] = RA
    sky_data[:,1] = Dec
    sky_data[:,2] = timeseries[0,:]

    for indfrq in range(len(nfreq)):
        print(indfrq, nfreq[indfrq])
        for t in range(num_snap):
           a = (t*T) % 60
           b = ((t*T-a)/60) % 60
           c = (t*T-a-b*60)/60/60
    
           # Yaml dictionary for pyuvsim
           number_of_frequency = int(nfreq[indfrq])
           # Convert Datetime into JD
#           print("Date: 2000-01-01 "+str(int(19+c))+":"+str(int(b))+":"+str(a))
           print("Date: 2000-01-01 {:02d}:{:02d}:{:02.4f}".format(int(19+c), int(b), a))

           start_time_utc = Time("2000-01-01T"+str(int(start_h+c))+":"+str(int(b))+":"+str(a), format='isot')
           start_time_utc_jd = float(start_time_utc.jd)
           print("JD:", start_time_utc_jd)
           output_fname = outfile_template + str(nfreq[indfrq])+"_"+str(t)
           meerkat_yml_dict = {'filing':{'outdir':outdir,
                                      'outfile_name':output_fname,
                                      'output_format':'uvh5',
                                      'clobber':True}, 
                            'freq':{'Nfreqs':number_of_frequency, 
                                    'start_freq':start_frequency_hz, 
                                    'channel_width':frequency_inc_hz},
                            'sources':{'catalog':catalog_name},
                            'telescope':{'array_layout':telescope_model,
                                         'telescope_config_name':telescope_config_name},                              
                            'time':{'Ntimes':1,
                                   'integration_time':T,
                                   'start_time':start_time_utc_jd}
                           }
        
           meerkat_yml_file = meerkat_yml_file_template+str(nfreq[indfrq])+"_"+str(t)+".yml"
           print("MeerKAT yml file: ", meerkat_yml_file)
           with open(meerkat_yml_file, 'w') as yaml_file:
                yaml.dump(meerkat_yml_dict, yaml_file, default_flow_style=False)
            
           sky_data1 = sky_data[t]

           # Create a sky model file for pyuvsim
           with open(catalog_name, "w") as myfile:
               myfile.write("SOURCE_ID	RA_J2000 [deg]	Dec_J2000 [deg]	Flux [Jy]	Frequency [Hz]\n")
           with open(catalog_name, "a") as myfile:
               myfile.write("TRANSIENT0 " + str(sky_data1[0]) + " " + str(sky_data1[1]) + " "+ str(sky_data1[2]) +" " + str(start_frequency_hz) +"\n")
    
           command = ['mpirun', '-n', str(int(ncores)), 'python', 'scripts/run_param_pyuvsim.py', meerkat_yml_file]
           result = subprocess.run(command, stdout=subprocess.PIPE)
           result_str = result.stdout.decode('utf-8')
           idx_start = result_str.find("Run uvdata uvsim took")
           idx_end = result_str.find("min\n", idx_start, -1)
           elapsed_time_no_overhead = float(result_str[idx_start:idx_end+4].split()[4])*60 # in secs
           print("UV simulation took", round(elapsed_time_no_overhead, 4), "sec\n")
           

# Usage Example:
Data1 = scipy.io.loadmat('J2251_aa2.mat')
timeseries = Data1['sim_flux2']
timeseries = numpy.array(timeseries)
homedir = Path.home()
telescope_model       = str(homedir) + '/software/X2V/settings_MeerKAT/MeerKAT_62/telescope_config/MeerKAT_pyuvsim_tm.csv'
catalog_name          = str(homedir) + '/software/X2V/settings_MeerKAT/catalog_files/transient_example.txt'
telescope_config_name = str(homedir) + '/software/X2V/settings_MeerKAT/MeerKAT_62/telescope_config/MeerKAT-gauss-fwhm1.0.yml'
outdir                = str(homedir) + '/software/SKA/pyuvsim_tests/pyuvsim_tests_QG/results_data_MeerKAT/'
outfile_template      = 'gleam-field-1-MeerKAT_test_pulsar-pyuvsim-sm_VS_'
meerkat_yml_file_template = "./meerkat_yml/MeerKAT_test_VS_"

run_pyuvsim_simulation(timeseries,
    telescope_model       = telescope_model,
    catalog_name          = catalog_name,
    telescope_config_name = telescope_config_name, # e.g. "MeerKAT-gauss-fwhm1.0.yml"
    outdir                = outdir,
    outfile_template      = outfile_template,
    meerkat_yml_file_template = meerkat_yml_file_template, # e.g. "./meerkat_yml/MeerKAT_test_VS_"
    T=2, # second
    num_snap=100,
    RA=-17.0667, # deg
    Dec=-37.1967, # deg
    nfreq=numpy.array([1,256]), # e.g., numpy.array([1,256,512,768,1024])
    start_frequency_hz=1382000000.,
    frequency_inc_hz=100000.,
    phase_centre_ra_deg=-17.0667,
    phase_centre_dec_deg=-37.1967,
    start_h=19,
    ncores=10)
