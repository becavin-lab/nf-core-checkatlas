/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { SUMMARY } from '../../modules/local/checkatlas_process'
include { QC } from '../../modules/local/checkatlas_process'
include { METRIC_CLUST } from '../../modules/local/checkatlas_process'
include { METRIC_ANNOT } from '../../modules/local/checkatlas_process'
include { METRIC_DIMRED } from '../../modules/local/checkatlas_process'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN Checkatlas cellranger WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow CHECKATLAS_CELLRANGER{
    take:
    atlas_info // dict: atlas_info
    
    main:
    // Run all checkatlas processes
    SUMMARY(atlas_info, params.path)
    QC(atlas_info, params.path)
    METRIC_CLUST(atlas_info, params.path)
    METRIC_ANNOT(atlas_info, params.path)
    METRIC_DIMRED(atlas_info, params.path)

    // Mix all out channels
    cellranger_out = SUMMARY.out.out_info
    cellranger_out = cellranger_out.mix(QC.out.out_info, METRIC_CLUST.out.out_info)
    cellranger_out = cellranger_out.mix(METRIC_ANNOT.out.out_info, METRIC_DIMRED.out.out_info)
    
    emit:
    cellranger_out    

}