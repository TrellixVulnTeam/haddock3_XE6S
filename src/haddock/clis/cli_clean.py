#!/usr/bin/env python3
"""
Clean the output of an HADDOCK3 run directory.

The clean process performs file archiving and file compressing
operations. File with extension `seed`, `inp`, `out`, and `con` are
compressed and archived into `.tgz` files. While files with `.pdb` and
`.psf` extension are compressed to `.gz` files. The original files are
deleted.

The <run_directory> can either be a whole HADDOCK3 run folder or a
specific folder of the workflow step.

Usage::

    haddock3-clean -h
    haddock3-clean <run_directory>
    haddock3-clean run1
    haddock3-clean run1/1_rigidbody
"""
import argparse
import sys

from haddock.libs.libcli import add_rundir_arg, add_version_arg


# Command line interface parser
ap = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

add_rundir_arg(ap)
add_version_arg(ap)


def _ap():
    return ap


def load_args(ap):
    """Load argument parser args."""
    return ap.parse_args()


def cli(ap, main):
    """Command-line interface entry point."""
    cmd = load_args(ap)
    main(**vars(cmd))


def maincli():
    """Execute main client."""
    cli(ap, main)


def main(run_dir, ncores=None):
    """
    Clean a HADDOCK3 directory.

    Usually, this concerns compressing and archiving files (see below).

    Parameters
    ----------
    run_dir : str or :external:py:class:`pathlib.Path`.
        The path to the run directory or to a folder of a specific step
        of the workflow.

    ncores : int, or None
        The number of cores to use. If ``None``, use all possible threads.
        Defaults to ``None``.

    See Also
    --------
    :py:module:`haddock.gear.clean_steps`
    """
    # anti-pattern to speed up CLI initiation
    from pathlib import Path

    from haddock import log
    from haddock.gear.clean_steps import clean_output
    from haddock.libs.libtimer import log_time
    from haddock.libs.libutil import parse_ncores
    from haddock.modules import get_module_steps_folders, is_step_folder

    log.info(f"Compressing {str(run_dir)!r} folder")
    ncores = parse_ncores(ncores)

    if is_step_folder(run_dir):
        with log_time("compressing took"):
            clean_output(run_dir, ncores)

    else:
        step_folders = get_module_steps_folders(run_dir)
        for folder in step_folders:
            with log_time("compressing took"):
                clean_output(Path(run_dir, folder), ncores)

    return


if __name__ == "__main__":
    sys.exit(maincli())
