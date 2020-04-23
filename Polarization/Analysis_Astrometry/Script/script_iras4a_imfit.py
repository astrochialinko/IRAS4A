###########################################################
# 2020.Apr.22
# Using CASA version 5.4.0
#
# Purpose:
#     Fit 2D elliptical Gaussian components on
#     JVLA K, Ka, Q, and ALMA B6, B7 images
#     towards NGC1333 IRAS4A.
#   
# Editor:
#   Chia-Lin Ko
###########################################################
import os
###########################################################


###### Work Flow ##########################################
thesteps = []
step_title = {
               0: 'Imfit images'
               #1: 'Export FITS images'
              }

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps
###########################################################



##### Global paramters and keywords ######################
outnames  = [
            'n1333iras4a_Q_rob-2_uvAll_2014_10_13',
            'n1333iras4a_K_rob-2_uvAll_2016_06_04',
            'n1333iras4a_K_rob-2_uvAll_2016_08_06',
            'n1333iras4a_Ka_rob-2_uvAll_2016_09_04',
            'n1333iras4a_B7_rob-2_uvAll_2016_09_06',
            'n1333iras4a_B6_rob-2_uvAll_2016_11_04',
            'n1333iras4a_B3_rob-2_uvAll_2017_08_17',
            'n1333iras4a_B4_rob-2_uvAll_2019_07_20',
             ]

new_outnames = [
               'iras4a2_Q_2014_10_13',
               'iras4a2_K_2016_06_04',
               'iras4a2_K_2016_08_06',
               'iras4a2_Ka_2016_09_04',
               'iras4a2_B7_2016_09_06',
               'iras4a2_B6_2016_11_04',
               'iras4a2_B3_2017_08_17',
               'iras4a2_B4_2019_07_20'
               ]

path_data  = '../Data_NoSelfCal/Data_NoSelfCal_Rg/'
path_log   = '../File_Log_imfit/'
path_reg   = '../File_Region/'
##########################################################



##### Imfit images ########################
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for i, outname in enumerate(outnames):

    new_outname = new_outnames[i]

    stokes       = 'I'
    Iimagename   = '%s%s_%s.image'%(path_data, outname, stokes)
    logfile      = '%s%s.log'%(path_log, new_outname)
    region       = '%s%s.crtf'%(path_reg, new_outname)


    # regrid the I image
    command = 'rm -rf ' + logfile
    os.system(command)

    imfit(
              imagename=Iimagename,
              region=region,
              logfile=logfile
              )


##########################################################




'''
##### Export FITS images ################################
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for outname in outnames:
    stokes = 'I'
    RgSmIimagename = '%s%s_%s_%s_%s.image'%(path_new, outname, smooth, regrid, stokes)
  
    outimages = [
                  RgSmIimagename
                  ]

    for outcasaimage in outimages:
      exportfits(
                 imagename = outcasaimage,
                 fitsimage = outcasaimage+'.fits',
                 overwrite = True
                )

#########################################################
'''

