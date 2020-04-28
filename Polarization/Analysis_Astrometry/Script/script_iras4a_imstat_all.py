###########################################################
# 2020.Apr.28
# Using CASA version 5.4.0
#
# Purpose:
#     Displays statistical information from 
#     JVLA K, Ka, Q, and ALMA B3, B4, B6, B7 images
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
               0: 'Imstat images'
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
            'n1333iras4a_2013_10_21_Ka_Tobin',
            'n1333iras4a_2014_02_24_Ka_Tobin',
            'n1333iras4a_2014_10_13_Q_Liu',
            'n1333iras4a_2015_06_13_B6_Sakai',
            'n1333iras4a_2015_09_27_B6_Tobin',
            'n1333iras4a_2016_06_04_K_Liu',
            'n1333iras4a_2016_07_23_B7_Su',
            'n1333iras4a_2016_08_06_K_Liu',
            'n1333iras4a_2016_09_04_Ka_Liu',
            'n1333iras4a_2016_09_06_B7_Lai',
            'n1333iras4a_2016_11_04_B6_Tao',
            'n1333iras4a_2016_12_14_B7_Su',
            'n1333iras4a_2017_08_17_B3_Cox',
            'n1333iras4a_2017_08_28_B6_Maury',
            'n1333iras4a_2017_12_17_B6_Tobin',
            'n1333iras4a_2018_10_16_B4_Francesco',
            'n1333iras4a_2019_07_20_B4_Lai',
             ]

new_outnames = [
                'iras4a2_2013_10_21_Ka_Tobin',
                'iras4a2_2014_02_24_Ka_Tobin',
                'iras4a2_2014_10_13_Q_Liu',
                'iras4a2_2015_06_13_B6_Sakai',
                'iras4a2_2015_09_27_B6_Tobin',
                'iras4a2_2016_06_04_K_Liu',
                'iras4a2_2016_07_23_B7_Su',
                'iras4a2_2016_08_06_K_Liu',
                'iras4a2_2016_09_04_Ka_Liu',
                'iras4a2_2016_09_06_B7_Lai',
                'iras4a2_2016_11_04_B6_Tao',
                'iras4a2_2016_12_14_B7_Su',
                'iras4a2_2017_08_17_B3_Cox',
                'iras4a2_2017_08_28_B6_Maury',
                'iras4a2_2017_12_17_B6_Tobin',
                'iras4a2_2018_10_16_B4_Francesco',
                'iras4a2_2019_07_20_B4_Lai',
                 ]

path_data  = '../Data_NoSelfCal/Data_NoSelfCal_Rg/'
path_log   = '../File_Log_imstat/'
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
    logfile      = '%s%s_imstat.log'%(path_log, new_outname)
    region       = '%s%s.crtf'%(path_reg, new_outname)


    # regrid the I image
    command = 'rm -rf ' + logfile
    os.system(command)

    imstat(
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

