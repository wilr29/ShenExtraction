import extraction.shen_extraction as se

print("Starting Extraction for ZALD_TTS fMRIPrep data.")

f_dir = '/projects/f_dz268_1/ZALD_TTS/BIDS/derivatives/fmriprep-20.2.6/fmriprep/'
s_dir = '/projects/f_dz268_1/ZALD_TTS/BIDS/'
o_dir = '/scratch/wr178/ZALD_TTS/ShenTimeSeries/'

print("fMRIPrep data: {} ".format(f_dir))
print("BIDS (raw) data: {}".format(s_dir))
print("Output directory: {}".format(o_dir))

se.shen_extraction(f_dir, s_dir, o_dir)
