"""
Downloading NeuroImaging datasets: Shen268 atlas
"""
import os

import nibabel as nb
import numpy as np
import pandas as pd
from numpy.lib import recfunctions
import re
from sklearn.utils import Bunch
from nilearn import datasets
from nilearn.datasets.utils import _get_dataset_dir, _fetch_files, _get_dataset_descr
from nilearn._utils import check_niimg, fill_doc
from nilearn.image import new_img_like, get_data, reorder_img

_TALAIRACH_LEVELS = ['hemisphere','lobe','gyrus','tissue','ba']

_LEGACY_FORMAT_MSG = (
    "`legacy_format` will default to `False` in release 0.11. "
    "Dataset fetchers will then return pandas dataframes by default "
    "instead of recarrarys."
)

@fill_doc
def fetch_atlas_shen(n_rois=268, resolution_mm=1, data_dir=None, verbose=1):
    """ Return file names for the Shen 2013 Parcellation.

    The Provided images are in MNI152 space.

    Parameters
    ----------
    n_rois : {268}, optional, it will probably break if you put in any other number
        Number of regions of interest. Default = 268.

    resolution_mm : {1, 2}, optional
        Spatial resolution of atlas image in mm
        Default=1mm.

    %(data_dir)s
    %(verbose)s

    Returns
    _______
    data : :func:`sklearn.utils.Bunch`
        Dictionary-like object, contains:

            - 'maps': :obj:`str`, path to nifti file containing the
              3D :class:`~nibabel.nifti1.Nifti1Image` (its shape is
              ``()``). The values are consecutive integers
              between 0 and ``n_rois`` which can be interpreted as indices
              in the list of labels.
            - 'labels': :class:`numpy.ndarray` of :obj:`str`, array
              containing the ROI labels including Shen-network annotation.
            - 'description': :obj:`str`, short description of the atlas
              and some references.

    References
    ----------
    .. footbibliography::


    Notes
    -----

    License: MIT.

    """
    valid_n_rois = [268]
    valid_resolution_mm = [1, 2]

    if n_rois not in valid_n_rois:
        raise ValueError("Requested n_rois={} not available. Valid "
                         "options: {}".format(n_rois, valid_n_rois))
    if resolution_mm not in valid_resolution_mm:
        raise ValueError("Requested resolution_mm={} not available. Valid "
                         "options: {}".format(resolution_mm, valid_resolution_mm))

    labels_file_template = 'shen_{}_parcellation_networklabels.csv'
    img_file_template = 'shen_{}mm_{}_parcellation.nii.gz'
    
    files = [labels_file_template.format(n_rois),
             img_file_template.format(resolution_mm, n_rois)]
    
    if data_dir is None:
        data_dir = '/home/wr178/src/ShenExtraction/shen_data'
        
    dataset_name = 'shen_2011'
    #data_dir = _get_dataset_dir(dataset_name, data_dir=data_dir, verbose=verbose)
    labels_file = os.path.join(data_dir, files[0])
    atlas_file = os.path.join(data_dir, files[1])

    csv_data = pd.read_csv(labels_file)
    labels = csv_data['Network'].tolist()

    return Bunch(maps=atlas_file,
                 labels=labels,
                 description=None)
