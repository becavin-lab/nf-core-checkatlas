import argparse  # pragma: no cover
import logging

import yaml

from . import nfcheckatlas  # pragma: no cover
from checkatlas import checkatlas_arguments
from checkatlas.metrics import annot, cluster, dimred


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m checkatlas` and `$ checkatlas `.

    This is checkatlas entry point.

    Arguments are managed here
    Search fo atlases is managed here
    Then checkatlas is ran with the list of atlases found

    Returns:
        None

    """
    # Set up logging
    logger = logging.getLogger("checkatlas")
    logging.basicConfig(format="|--- %(levelname)-8s %(message)s")

    parser = checkatlas_arguments.create_parser()

    # Parse all args
    args = parser.parse_args()
    
    # Validate TEST_ALLMETRICS
    if args.TEST_ALLMETRICS:
        args.metric_cluster = cluster.__all__
        args.metric_annot = annot.__all__
        args.metric_dimred = dimred.__all__

    # If a config file was provided, load the new args
    if args.config != "":
        logger.info(
            "Read config file {} to get new checkatlas configs".format(
                args.config
            )
        )
        args = checkatlas_arguments.load_arguments(args, args.config)

    # Set logger level
    if args.debug:
        logger.setLevel(getattr(logging, "DEBUG"))
    else:
        logger.setLevel(getattr(logging, "INFO"))

    logger.debug(f"Program arguments: {args}")

    # Save all arguments to yaml (only run it when
    # generating example file config.yaml
    # save_arguments(args, 'nfcheckatlas/config/default_config.yaml')

    #   ######    Run Checkatlas   #########
    nfcheckatlas.run(args)


if __name__ == "__main__":  # pragma: no cover
    main()
