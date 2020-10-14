import os
import sys
import argparse
import gzip
import shutil
import tarfile
import patoolib


def _create_tar_family_archive(file_path, suffix_str, w_mode):
    out_dir = file_path.split(".")[0]
    out_dir = out_dir.split("\\")
    out_dir = out_dir[len(out_dir) - 1] + "\\" + out_dir[len(out_dir) - 1] + suffix_str

    with tarfile.open(file_path.split(".")[0] + suffix_str, mode=w_mode) as tar:
        tar.add(file_path.split(".")[0] + suffix_str, arcname=out_dir)


class FilesFamily(object):

    def __init__(self, list_of_formats):
        """
            Args:
                list_of_formats (list[str]): List of formats that the class supports, represented by
                                             strings of file suffixes
        """

        self.list_of_formats = list_of_formats

    def convert(self, file_path, dest_format):
        print 'Convert to format {}'.format(dest_format)

        suffix_of_src_file = file_path.split(".")[-1]

        if suffix_of_src_file not in self.list_of_formats:
            print ("The file is not part of the family")

        if suffix_of_src_file in ("tar", "gz"):
            fp = tarfile.open(file_path, "r")
            fp.extractall()
            fp.close()

        if suffix_of_src_file == "rar":
            patoolib.extract_archive(file_path)

        if dest_format == "tar":
            _create_tar_family_archive(file_path, ".tar", "w")

        if dest_format == "gz":
            _create_tar_family_archive(file_path, ".tar.gz", "w:gz")

        if dest_format == "rar":
            patoolib.create_archive(file_path.split(".")[0] + ".rar", (file_path.split(".")[0],))

    def is_format_compatible(self, format_name):
        return format_name in self.list_of_formats


def build_parser():
    parser = argparse.ArgumentParser(description='This is a File converter')
    parser.add_argument('src_file', action="store", type=str)
    parser.add_argument('format_name', action="store", type=str)

    return parser


def main():
    options = build_parser().parse_args()

    lst_of_zip_formats = ["gz", "rar", "tar", "zip"]

    zip_family = FilesFamily(lst_of_zip_formats)

    format_to_class_dict = {"rar": zip_family, "gz": zip_family, "tar": zip_family}
    working_class = None

    if options.format_name in format_to_class_dict.keys():
        working_class = format_to_class_dict[options.format_name]
    else:
        raise RuntimeError("Incorrect format")
        exit

    if working_class.is_format_compatible(options.format_name):
        working_class.convert(options.src_file, options.format_name)
    else:
        raise RuntimeError("Incompatible format")


if __name__ == "__main__":
    main()
