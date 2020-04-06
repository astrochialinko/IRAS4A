##########################################################
# 2020.Apr.06
# Using CASA version 5.4.0
#
# Purpose:
#     Smooth images to 0.2 arcsec, 0.1 arcsec, 0 deg
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
               0: 'Smooth images',
               1: 'Create subimages',
               2: 'Regard images',
               3: 'Export FITS images'
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
outnames = [
            'n1333iras4a_band4_rob2_uv24_2900kl',
            'n1333iras4a_band7_rob0.5_uv24_2900kl'
            ]

new_outnames = [
            'n1333iras4a_B4_uv24_2900kl_sm200_100mas_noshift',
            'n1333iras4a_B7_uv24_2900kl_sm200_100mas_noshift'
            ]

path_old    = '../../Original_data/UV24_2900_kl/'
path_new    = '../Image_Data/'
parameter   = 'sm200_100mas_noshift'
outname_temp = 'n1333iras4a_band7_rob0.5_uv24_2900kl'
##########################################################



##### Smooth images ########################
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  for outname in outnames:

    stokes      = 'I'
    Iimagename   = '%s%s_%s.image'%(path_old, outname, stokes)
    SmIimagename   = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
    stokes      = 'Q'
    Qimagename   = '%s%s_%s.image'%(path_old, outname, stokes)
    SmQimagename   = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
    stokes      = 'U'
    Uimagename   = '%s%s_%s.image'%(path_old, outname, stokes)
    SmUimagename   = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
  
     
    # smooth the I image
    command = 'rm -rf ' + SmIimagename
    os.system(command)
    
    kernel = 'gaussian'
    major = '0.2arcsec'
    minor = '0.1arcsec'
    pa = '0deg'
    targetres = True
    
    imsmooth(
              imagename=Iimagename,
              kernel=kernel,
              major=major,
              minor=minor,
              pa=pa,
              targetres=targetres,
              outfile=SmIimagename
              )

    # smooth the Q image
    command = 'rm -rf ' + SmQimagename
    os.system(command)
    
    imsmooth(
              imagename=Qimagename,
              kernel=kernel,
              major=major,
              minor=minor,
              pa=pa,
              targetres=targetres,
              outfile=SmQimagename
              )

    # smooth the U image
    command = 'rm -rf ' + SmUimagename
    os.system(command)
    
    imsmooth(
              imagename=Uimagename,
              kernel=kernel,
              major=major,
              minor=minor,
              pa=pa,
              targetres=targetres,
              outfile=SmUimagename
              )
              
    

##########################################################



##### Creat subimages as regrid template ################################
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

stokes          = 'I'
TempImagename   = '%s%s_%s_%s.image'%(path_new, outname_temp, parameter, stokes)
SubImagename    = '%s%s_%s_sub_%s.image'%(path_new, outname_temp, parameter, stokes)
region          = 'box[[1500pix, 1500pix], [4500pix, 4500pix]]'

# Creat a subimage
command = 'rm -rf ' + SubImagename
os.system(command)

imsubimage(
            imagename=TempImagename,
            outfile=SubImagename,
            region=region,
            overwrite=True
            )

##########################################################



##### Regrid images ########################
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for i, outname in enumerate(outnames):
    new_outname = new_outnames[i]

    stokes          = 'I'
    SmIimagename    = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
    RgSmIimagename  = '%s%s_%s.image'%(path_new, new_outname, stokes)
    SubImagename    = '%s%s_%s_sub_%s.image'%(path_new, outname_temp, parameter, stokes)

    stokes          = 'Q'
    SmQimagename    = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
    RgSmQimagename  = '%s%s_%s.image'%(path_new, new_outname, stokes)

    stokes          = 'U'
    SmUimagename    = '%s%s_%s_%s.image'%(path_new, outname, parameter, stokes)
    RgSmUimagename  = '%s%s_%s.image'%(path_new, new_outname, stokes)

    # regrid the I image
    command = 'rm -rf ' + RgSmIimagename
    os.system(command)

    imregrid(
              imagename=SmIimagename,
              template=SubImagename,
              output=RgSmIimagename
              )
    
    command = 'rm -rf ' + SmIimagename
    os.system(command)

    # regrid the Q image
    command = 'rm -rf ' + RgSmQimagename
    os.system(command)

    imregrid(
              imagename=SmQimagename,
              template=SubImagename,
              output=RgSmQimagename
              )

    command = 'rm -rf ' + SmQimagename
    os.system(command)

    # regrid the U image
    command = 'rm -rf ' + RgSmUimagename
    os.system(command)

    imregrid(
              imagename=SmUimagename,
              template=SubImagename,
              output=RgSmUimagename
              )

    command = 'rm -rf ' + SmUimagename
    os.system(command)


# delete the subimage
command = 'rm -rf ' + SubImagename
os.system(command)

##########################################################




##### Export FITS images ################################
mystep = 3
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for i, outname in enumerate(outnames):
    new_outname = new_outnames[i]
    
    stokes      = 'I'
    RgSmIimagename   = '%s%s_%s.image'%(path_new, new_outname, stokes)
    stokes      = 'Q'
    RgSmQimagename   = '%s%s_%s.image'%(path_new, new_outname, stokes)
    stokes      = 'U'
    RgSmUimagename   = '%s%s_%s.image'%(path_new, new_outname, stokes)

  
    outimages = [
                    RgSmIimagename,
                    RgSmQimagename,
                    RgSmUimagename
                ]

    for outcasaimage in outimages:
        exportfits(
                   imagename = outcasaimage,
                   fitsimage = outcasaimage+'.fits',
                   overwrite = True
                     )

#########################################################
