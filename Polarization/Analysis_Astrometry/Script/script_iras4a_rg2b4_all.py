###########################################################
# 2020.Apr.26
# Using CASA version 5.4.0
#
# Purpose:
#     Regrid VLA K, Ka, Q, and ALMA band 6 images 
#     and other archive data
#     onto ALMA band 7 image (new coordinate)
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
                'n1333iras4a_2014_10_13_Q_Liu',
                'n1333iras4a_2016_06_04_K_Liu',
                'n1333iras4a_2016_08_06_K_Liu',
                'n1333iras4a_2016_09_04_Ka_Liu',
                'n1333iras4a_2016_09_06_B7_Lai',
                'n1333iras4a_2016_11_04_B6_Tao',
                'n1333iras4a_2017_08_17_B3_Cox',
                'n1333iras4a_2019_07_20_B4_Lai',
                ]

outnames_arc = [
                'n1333iras4a_Ka_archive_2013Oct21_Tobin',
                'n1333iras4a_Ka_archive_2014Feb24_Tobin',
                'n1333iras4a_band4_archive_2018Oct16_Francesco',
                'n1333iras4a_band6_archive_2015Jun13_Sakai',
                'n1333iras4a_band6_archive_2015Sep27_Tobin',
                'n1333iras4a_band6_archive_2017Aug28_Maury',
                'n1333iras4a_band6_archive_2017Dec17_Tobin',
                'n1333iras4a_band7_archive_2016Dec14_Su',
                'n1333iras4a_band7_archive_2016Jul23_Su'
                ]

new_outnames_arc = [
                     'n1333iras4a_2013_10_21_Ka_Tobin',
                     'n1333iras4a_2014_02_24_Ka_Tobin',
                     'n1333iras4a_2018_10_16_B4_Francesco',
                     'n1333iras4a_2015_06_13_B6_Sakai',
                     'n1333iras4a_2015_09_27_B6_Tobin',
                     'n1333iras4a_2017_08_28_B6_Maury',
                     'n1333iras4a_2017_12_17_B6_Tobin',
                     'n1333iras4a_2016_12_14_B7_Su',
                     'n1333iras4a_2016_07_23_B7_Su'
                    ]
outname_temp = 'n1333iras4a_band4_rob-2_uvAll_th10uJy_hogbom_mask_cell0d01'

path_old    = '../Data_NoSelfCal/Original_NoSelfCal/'
path_arc    = '../Data_NoSelfCal/Original_archive/'
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

  # regrid the Archive data
  for i, outname_arc in enumerate(outnames_arc):
    new_outname_arc = new_outnames_arc[i]

    stokes         = 'I'
    Iimagename     = '%s%s_%s.image'%(path_arc, outname_arc, stokes)
    RgIimagename   = '%s%s_%s.image'%(path_new, new_outname_arc, stokes)
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


  # export archive images
  for new_outname_arc in new_outnames_arc:
    stokes = 'I'
    RgIimagename   = '%s%s_%s.image'%(path_new, new_outname_arc, stokes)

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


