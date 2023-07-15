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
include { READ_SAMPLESHEET } from './read_samplesheet'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN Checkatlas seurat WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow CHECKATLAS_SEURAT{
    take:
    samplesheet // file: /path/to/samplesheet.csv

    main:
    // Create a channel from list_seurat samplesheet
    READ_SAMPLESHEET ( samplesheet )
    atlas_info = READ_SAMPLESHEET.out.atlas_info

    // Run all checkatlas processes
    SUMMARY(atlas_info, params.path)
    QC(atlas_info, params.path)
    METRIC_CLUST(atlas_info, params.path)
    METRIC_ANNOT(atlas_info, params.path)
    METRIC_DIMRED(atlas_info, params.path)

}