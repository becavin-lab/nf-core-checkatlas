workflow READ_SAMPLESHEET {
    take:
    samplesheet // file: /path/to/samplesheet.csv

    main:
    myFileChannel = Channel.fromPath(samplesheet)
    myFileChannel.splitCsv ( header:true, sep:',' )
        .map { create_atlas_info(it) }
        .set { atlas_info }

    emit:
    atlas_info                                     // channel: [ val(meta), [ reads ] ]
}

// Function to get list of [ meta, [ fastq_1, fastq_2 ] ]
def create_atlas_info(LinkedHashMap row) {
    // create meta map
    
    // Atlas_name,Atlas_type,Atlas_extension,Atlas_path
    def meta = [:]
    meta.atlas_name = row.Atlas_name
    meta.atlas_type = row.Atlas_type
    meta.atlas_extension = row.Atlas_extension
    meta.atlas_path = row.Atlas_path
    
    return meta
}