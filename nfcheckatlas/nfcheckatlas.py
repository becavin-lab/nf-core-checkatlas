import argparse
import logging
import os
from checkatlas import checkatlas
from checkatlas import atlas
from checkatlas import seurat
from checkatlas.utils import folders
from checkatlas.metrics import cluster
from checkatlas.metrics import annot
from checkatlas.metrics import dimred


logger = logging.getLogger("checkatlas")

def run(args: argparse.Namespace) -> None:
    """
    Main function of checkatlas
    Run all functions for all atlases:
    - Clean files list by getting only Scanpy atlas (converted from Seurat
    if necessary)
    - Extract summary tables
    - Create UMAP and T-sne figures
    - Calculate every metrics

    Args:
        args: List of args for checkatlas program
    Returns:
        None
    """

    logger.debug(f"Transform path to absolute:{args.path}")
    args.path = os.path.abspath(args.path)
    logger.debug(f"Check checkatlas folders in:{args.path}")
    folders.checkatlas_folders(args.path)

    logger.info("Searching Seurat, Cellranger and Scanpy files")
    checkatlas.list_all_atlases(args.path)
    (
        clean_scanpy_list, clean_cellranger_list, clean_seurat_list
    ) = checkatlas.read_list_atlases(args.path)
    clean_scanpy_list = clean_scanpy_list.to_dict('index')
    logger.info(
        f"Found {len(clean_scanpy_list)} potential "
        f"scanpy files with .h5ad extension"
    )
    logger.info(
        f"Found {len(clean_seurat_list)} potential "
        f"seurat files with .rds extension"
    )
    logger.info(
        f"Found {len(clean_cellranger_list)} cellranger "
        f"file with .h5 extension"
    )

    if len(clean_cellranger_list) > 0:
        logger.debug("Install Seurat if needed")
        seurat.check_seurat_install()

    if len(clean_scanpy_list) != 0:
        run_checkatlas(clean_scanpy_list, args)
    if len(clean_cellranger_list) != 0:
        run_checkatlas(clean_cellranger_list, args)
    if len(clean_seurat_list) != 0:
        run_checkatlas_seurat(clean_seurat_list, args)



def run_checkatlas(clean_atlas, args) -> None:
    """
    Run Checkatlas pipeline for all Scanpy and Cellranger objects
    Args:
        clean_atlas: List of atlas
        args: List of args for checkatlas program
    Returns:
        None
    """
    # Go through all atlas
    for atlas_name, atlas_info in clean_atlas.items():
        for process in checkatlas.PROCESS_TYPE:
            checkatlas_cmd = f"checkatlas {process} {atlas_name} {args.path}"
            logger.debug(f"Execute: {checkatlas_cmd}")
            # Run Process
            os.system(checkatlas_cmd)


def run_checkatlas_seurat(clean_atlas, args) -> None:
    """
    Run Checkatlas pipeline for all Scanpy and Cellranger objects
    TO DO: FRO the moment run_checkatlas_seurat and run_checkatlas are
    the same; it will change in final nextflow. Because one will run python code,
     the other R code
    Args:
        clean_atlas: List of atlas
        args: List of args for checkatlas program
    Returns:
        None
    """
    # Go through all atlas
    for atlas_name, atlas_info in clean_atlas.items():
        for process in checkatlas.PROCESS_TYPE:
            checkatlas_cmd = f"checkatlas {process} {atlas_name} {args.path}"
            logger.debug(f"Execute: {checkatlas_cmd}")
            # Run Process
            os.system(process)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="checkatlas",
        usage="checkatlas [OPTIONS] your_search_folder/",
        description="CheckAtlas is a one liner tool to check the "
        "quality of your single-cell atlases. For "
        "every atlas, it produces the quality control "
        "tables and figures which can be then processed "
        "by multiqc. CheckAtlas is able to load Scanpy, "
        "Seurat, and CellRanger files.",
        epilog="Enjoy the checkatlas functionality!",
    )

    parser.add_argument(
        "path",
        type=str,
        help="Required argument: Your folder containing "
        "Scanpy, CellRanger and Seurat atlasesv",
        default=".",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print out all debug messages.",
    )

    # Arguments linked to QC
    qc_options = parser.add_argument_group("QC options")
    qc_options.add_argument(
        "--qc_display",
        nargs="+",
        type=str,
        default=[
            "violin_plot",
            "total_counts",
            "n_genes_by_counts",
            "pct_counts_mt",
        ],
        help="List of QC to display. "
        "Available qc = violin_plot, total_counts, "
        "n_genes_by_counts, pct_counts_mt. "
        "Default: --qc_display violin_plot total_counts "
        "n_genes_by_counts pct_counts_mt",
    )
    qc_options.add_argument(
        "--plot_celllimit",
        type=int,
        default=10000,
        help="Set the maximum number of cells"
        "to plot in QC, UMAP, t-SNE, etc...."
        "If plot_celllimit=0, no limit will"
        "be applied.",
    )

    # Arguments linked to metric
    metric_options = parser.add_argument_group("Metric options")
    metric_options.add_argument(
        "--obs_cluster",
        nargs="+",
        type=str,
        default=atlas.OBS_CLUSTERS,
        help="List of obs from the adata file to "
        "use in the clustering metric calculus."
        "Example: --obs_cluster celltype leuven seurat_clusters",
    )
    metric_options.add_argument(
        "--metric_cluster",
        nargs="+",
        type=str,
        # default=["silhouette", "davies_bouldin"],
        default=["davies_bouldin"],
        help="Specify the list of clustering metrics to calculate.\n"
        "   Example: --metric_cluster silhouette davies_bouldin\n"
        f"   List of cluster metrics: {cluster.__all__}",
    )
    metric_options.add_argument(
        "--metric_annot",
        nargs="+",
        type=str,
        # default=[],
        default=["rand_index"],
        help=f"Specify the list of clustering metrics to calculate."
        f"   Example: --metric_annot rand_index"
        f"   List of annotation metrics: {annot.__all__}",
    )
    metric_options.add_argument(
        "--metric_dimred",
        nargs="+",
        type=str,
        default=["kruskal_stress"],
        # default=[],
        help="Specify the list of dimensionality reduction "
        "metrics to calculate.\n"
        "   Example: --metric_dimred kruskal_stress\n"
        f"   List of dim. red. metrics: {dimred.__all__}",
    )
    return parser

if __name__ == "__main__":
    # folders.checkatlas_folders(path)
    # atlas_list = list_atlases(path)
    print("main")
