import os
from nilearn import datasets
# from nideconv.utils import roi
from utils import roi
import pandas as pd
from nilearn import plotting
from nilearn.input_data import NiftiLabelsMasker, NiftiMapsMasker
import shen_atlas as sa
import re

base_dir = 'C:\\Users\\wr178\\PycharmProjects\\ShenExtraction'

# Locate the data of the first subject
#func = 'fmriprep\\sub-108768\\func\\sub-108768_task-gonogo_run-2_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz'
#func = 'fmriprep/sub-108768/func/sub-108768_task-gonogo_run-1_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz'
#func = 'fmriprep/sub-108768/func/sub-108768_task-gonogo_run-2_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz'
#func = 'fmriprep/sub-212291/func/sub-212291_task-gonogo_run-1_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz'
#func = 'fmriprep/sub-212291/func/sub-212291_task-mid_run-2_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz'
#func = 'fmriprep/sub-212291/func/sub-212291_task-mid_run-2_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz'
#func = 'fmriprep/sub-212291/func/sub-212291_task-gonogo_run-1_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz'
func = 'fmriprep/sub-212291/func/sub-212291_task-cap_run-2_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz'

# Get meta data for this file
p = re.compile(r'sub-(?P<sub>\d+)_task-(?P<task>\w+)_run-(?P<run>\d+)_space-\w+(_res-(?P<res>\d+))*_desc-(?P<desc>\w+)_bold')
m = p.search(func)
sub = m.group('sub')
task = m.group('task')
run = m.group('run')
desc = m.group('desc')
if m.group('res') is None:
    res = 2
else:
    res = int(m.group('res'))

if 'AROMA' in desc:
    desc = 'AROMA'

# ... and confounds extracted by fmriprep
#confounds_fn = 'fmriprep\\sub-108768\\func\\sub-108768_task-gonogo_run-1_desc-confounds_timeseries.tsv'
confounds_fn = 'fmriprep/sub-%s/func/sub-%s_task-%s_run-%s_desc-confounds_timeseries.tsv' % (sub,sub,task,run)
#confounds_fn = 'fmriprep/sub-212291/func/sub-212291_task-mid_run-2_desc-confounds_timeseries.tsv'

func = os.path.join(base_dir, func)
confounds_fn = os.path.join(base_dir, confounds_fn)

# We need to load the confounds and fill nas

confounds = pd.read_table(confounds_fn).fillna(method='bfill')

# We only want to include a subset of confounds
confounds_to_include = ['framewise_displacement', 'a_comp_cor_00',
                        'a_comp_cor_01', 'a_comp_cor_02', 'a_comp_cor_03',
                        'a_comp_cor_04', 'a_comp_cor_05',
                        'rot_x', 'rot_y', 'rot_z']
confounds = confounds[confounds_to_include]


# Use the Shen 2013 atlas
atlas_shen = sa.fetch_atlas_shen(resolution_mm=res)
#plotting.plot_prob_atlas(atlas_shen.maps)
#plotting.plot_roi(atlas_shen.maps)

#masker = NiftiLabelsMasker(labels_img=atlas_shen.maps, standardize=True)
#time_series = masker.fit_transform(func, confounds=confounds_fn)

ts = roi.extract_timecourse_from_nii(atlas_shen,
                                     func,
                                     confounds=confounds.values,
                                     t_r=2,
                                     high_pass=1./128,
                                     )


print(ts)

svname = 'sub-%s_task-%s_run-%s_desc-%s_bold' % (sub,task,run,desc)

ts.to_csv(os.path.join(base_dir,'shen_data','%s.csv' % svname))
ts.to_pickle(os.path.join(base_dir,'shen_data','%s.pkl' % svname))
#print("DONE!")