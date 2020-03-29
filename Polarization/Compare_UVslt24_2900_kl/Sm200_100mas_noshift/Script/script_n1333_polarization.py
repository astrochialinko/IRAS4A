##########################################################
# 2020.Mar.26
# Using CASA version 5.3.0
#
# Purpose:
#     Producing polarization images towards
#     NGC1333 IRAS4A.
#   
# Editor:
#   Baobab, Chia-Lin Ko
###########################################################
import os
import time
###########################################################





###### Work Flow ##########################################
thesteps = []
step_title = {
               0: 'Produce polarization images',
               1: 'Export FITS images'
              }

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mystepsz
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps
###########################################################


##### Global paramters and keywords ######################
outname_b4   = 'n1333iras4a_B4_uv24_2900kl_sm200_100mas_noshift'
outname_b7   = 'n1333iras4a_B7_uv24_2900kl_sm200_100mas_noshift'

outnames = [
             outname_b4, outname_b7
            ]
path_old    = '../Data_images/'
path_new    = '../Data_images/'
##########################################################
rms_I_b4     = 2.3e-4
rms_Q_b4     = 1.2e-5
rms_PI_b4    = 1.2e-5 

rms_I_b7    = 6.4e-4
rms_Q_b7    = 4.2e-5
rms_PI_b7   = 4.2e-5
##########################################################


# Measure time
start_time = time.time()
##### Produce polarization images ########################
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for outname in outnames:

    if outname == outname_b4:
        rms_I=rms_I_b4
        rms_Q=rms_Q_b4

    stokes      = 'I'
    Iimagename = '%s%s_%s.image'%(path_old, outname, stokes)
    stokes      = 'Q'
    Qimagename = '%s%s_%s.image'%(path_old, outname, stokes)
    stokes      = 'U'
    Uimagename = '%s%s_%s.image'%(path_old, outname, stokes)
    stokes      = 'PI'
    PIimagename = '%s%s_%s.image'%(path_old, outname, stokes)
    stokes      = 'Per'
    Perimagename = '%s%s_%s.image'%(path_old, outname, stokes)
    stokes      = 'PA'
    PAimagename = '%s%s_%s.image'%(path_old, outname, stokes)

    # generate the linear polarization intensity image
    command = 'rm -rf ' + PIimagename
    os.system(command)
    
    mode = 'poli'
    imagename = [Qimagename, Uimagename]
    # sigma = rms(of stoke Q, stoke U)
    sigma     = '%sJy/beam'%(str(rms_Q))
    
    immath(
           outfile=PIimagename,
           mode=mode,
           sigma=sigma,
           imagename=imagename
          )

    # derive the polarization position angle
    command = 'rm -rf ' + PAimagename
    os.system(command)
    
    mode = 'pola'
    imagename = [Qimagename, Uimagename]
    # threshold = 2.5*rms(of PI)
    # polithresh = '6.25e-5Jy/beam' 
    
    immath(
           outfile=PAimagename,
           mode=mode,
           #polithresh=polithresh,
           imagename=imagename
          )

    # derive polarization percentage
    command = 'rm -rf ' + Perimagename
    os.system(command)
    
    mode  = 'evalexpr'
    # I > 5*rms(of I)
    expr  = 'IM0*100/IM1[IM1>%s]'%(str(3*rms_I))
    imagename = [PIimagename, Iimagename]
    
    immath(
           outfile=Perimagename,
           mode=mode,
           imagename=imagename,
           expr=expr
          )

##########################################################





##### Export FITS images ################################
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for outname in outnames:
    stokes      = 'PI'
    PIimagename = '%s%s_%s.image'%(path_new, outname, stokes)
    stokes      = 'Per'
    Perimagename = '%s%s_%s.image'%(path_new, outname, stokes)
    stokes      = 'PA'
    PAimagename = '%s%s_%s.image'%(path_new, outname, stokes)

    outimages = [
                  PIimagename,
                  PAimagename,
                  Perimagename
                  ]

    for outcasaimage in outimages:
      exportfits(
                 imagename = outcasaimage,
                 fitsimage = outcasaimage+'.fits',
                 overwrite = True
                )

#########################################################
