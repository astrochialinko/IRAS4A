###########################################################
# 2020.Apr.22
# Using CASA version 5.4.0
#
# Purpose:
#     Regrid VLA K, Ka, Q, and ALMA band 6 images onto
#     ALMA band 7 image (new coordinate)
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
               0: 'Create subimages',
               1: 'Regrid images',
               2: 'Export FITS images'
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
            'n1333iras4ab_Qband_rob-2_uvAll_th20uJy_interact_2014Oct13_noselfcal',
            'n1333iras4ab_Kband_rob-2_uvAll_th8uJy_cell0d01_interact_2016Jun04_noselfcal',
            'n1333iras4ab_Kband_rob-2_uvAll_th8uJy_cell0d01_interact_2016Aug06_noselfcal',
            'n1333iras4ab_Kaband_rob-2_uvAll_th15uJy_interact_cell0d01_noselfcal',
            'n1333iras4a_band7_rob-2_uvAll_th270uJy_hogbom_interact',
            'n1333iras4a_band6_rob-2_uvAll_th30uJy_cell0d02_interact',
            'n1333iras4a_band3_rob-2_uvAll_th50uJy_cell0d01_interact',
            'n1333iras4a_band4_rob-2_uvAll_th10uJy_hogbom_mask_cell0d01'
            ]

new_outnames = [
                'n1333iras4a_Q_rob-2_uvAll_2014_10_13',
                'n1333iras4a_K_rob-2_uvAll_2016_06_04',
                'n1333iras4a_K_rob-2_uvAll_2016_08_06',
                'n1333iras4a_Ka_rob-2_uvAll_2016_09_04',
                'n1333iras4a_B7_rob-2_uvAll_2016_09_06',
                'n1333iras4a_B6_rob-2_uvAll_2016_11_04',
                'n1333iras4a_B3_rob-2_uvAll_2017_08_17',
                'n1333iras4a_B4_rob-2_uvAll_2019_07_20',
                ]

outname_temp = 'n1333iras4a_band4_rob-2_uvAll_th10uJy_hogbom_mask_cell0d01'

path_old    = '../Data_NoSelfCal/Original_NoSelfCal/'
path_new    = '../Data_NoSelfCal/Data_NoSelfCal_Rg/'
path_temp   = '../Data_NoSelfCal/Original_NoSelfCal/'

##########################################################




##### Creat subimages as regrid template #################
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]



stokes          = 'I'
Iimagename      = '%s%s_%s.image'%(path_old, outname_temp, stokes)
SubImagename    = '%s%s_sub_%s.image'%(path_new, outname_temp, stokes)
region          = 'box[[3000pix, 3000pix], [3350pix, 3350pix]]'

# Creat a subimage
command = 'rm -rf ' + SubImagename
os.system(command)

imsubimage(
            imagename=Iimagename,
            outfile=SubImagename,
            region=region,
            overwrite=True
            )

##########################################################




##### Regrid images ########################
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for i, outname in enumerate(outnames):
    new_outname = new_outnames[i]

    stokes         = 'I'
    Iimagename     = '%s%s_%s.image'%(path_old, outname, stokes)
    RgIimagename   = '%s%s_%s.image'%(path_new, new_outname, stokes)
    TempIimagename = '%s%s_sub_%s.image'%(path_new, outname_temp, stokes)


    # regrid the I image
    command = 'rm -rf ' + RgIimagename
    os.system(command)

    imregrid(
              imagename=Iimagename,
              template=TempIimagename,
              output=RgIimagename
              )

# delete the subimage
command = 'rm -rf ' + TempIimagename
os.system(command)

##########################################################





##### Export FITS images ################################
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for new_outname in new_outnames:
    stokes = 'I'
    RgIimagename   = '%s%s_%s.image'%(path_new, new_outname, stokes)
  
    outimages = [
                  RgIimagename
                  ]

    for outcasaimage in outimages:
      exportfits(
                 imagename = outcasaimage,
                 fitsimage = outcasaimage+'.fits',
                 overwrite = True
                )

#########################################################


