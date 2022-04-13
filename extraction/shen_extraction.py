import os
from utils import roi
import pandas as pd
import shen_atlas as sa
import re

"""
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
"""
# Alright so we're gonna do things a little bit differently this time
# This is basically an exploded view of roi.get_fmriprep_timeseries
# TODO: Pass the fmriprep path in as an arg
fmriprep_path = 'C:\\Users\\wr178\\Documents\\ZALD_TTS\\BIDS\\derivatives\\'
source_path = 'C:\\Users\\wr178\\Documents\\ZALD_TTS\\BIDS\\'
out_dir = 'C:\\Users\\wr178\\Documents\\SRC\\ShenExtraction\\timeSeries'
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

# We only want to include a subset of confounds
confounds_to_include = ['framewise_displacement', 'a_comp_cor_00',
                        'a_comp_cor_01', 'a_comp_cor_02', 'a_comp_cor_03',
                        'a_comp_cor_04', 'a_comp_cor_05',
                        'rot_x', 'rot_y', 'rot_z']

for func, confounds, meta in roi.get_func_and_confounds(fmriprep_path,
                                                         source_path):
    # For now, this will only extract from the MNI152 space preproc files
    print("Extracting signal from {}...".format(func.filename))
    confounds = pd.read_table(confounds.path).fillna(method='bfill')
    meta = func.entities

    if meta is None:
        t_r = 2
    else:
        t_r = meta["RepetitionTime"]

    # Load shen atlas based on resolution
    if "res" in func.get_entities():
        res = int(func.entities["res"])
    else:
        res = 2

    # Use the Shen 2013 atlas
    atlas_shen = sa.fetch_atlas_shen(resolution_mm=res)

    ts = roi.extract_timecourse_from_nii(atlas_shen,
                                         func.path,
                                         confounds=confounds[confounds_to_include].values,
                                         t_r=t_r,
                                         high_pass=1./128,
                                         )
    print("Saving data...")
    sv_dir = os.path.join(out_dir, 'sub-%s' % meta["subject"])
    if not os.path.isdir(sv_dir):
        os.mkdir(sv_dir)

    svname = 'sub-%s_task-%s_run-%d_desc-%s_bold' % (meta["subject"],
                                                     meta["task"],
                                                     meta["run"],
                                                     meta["desc"])

    ts.to_csv(os.path.join(sv_dir, '%s.csv' % svname))
    # ts.to_pickle(os.path.join(base_dir, 'shen_data', '%s.pkl' % svname))

    print("DONE!")