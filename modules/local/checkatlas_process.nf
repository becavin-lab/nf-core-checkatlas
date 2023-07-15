process SUMMARY{
    label 'process_summary'

    input:
    val atlas_info
    path samplesheet

    script:
    """
    checkatlas summary ${atlas_info.atlas_name} $samplesheet
    """
}

process QC{
    label 'process_qc'

    input:
    val atlas_info
    path samplesheet

    script:
    """
    checkatlas qc ${atlas_info.atlas_name} $samplesheet
    """
}

process METRIC_CLUST{
    label 'process_metric_clust'

    input:
    val atlas_info
    path samplesheet

    script:
    """
    checkatlas metric_clust ${atlas_info.atlas_name} $samplesheet
    """
}

process METRIC_ANNOT{
    label 'process_metric_annot'

    input:
    val atlas_info
    path samplesheet

    script:
    """
    checkatlas metric_annot ${atlas_info.atlas_name} $samplesheet
    """
}

process METRIC_DIMRED{
    label 'process_metric_dimred'

    input:
    val atlas_info
    path samplesheet

    script:
    """
    checkatlas metric_dimred ${atlas_info.atlas_name} $samplesheet
    """
}

