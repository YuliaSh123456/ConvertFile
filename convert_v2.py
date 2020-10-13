import sys
import argparse
import gzip
import shutil
import tarfile
import rarfile
import patoolib
import unrar

class FilesFamily:

    def __init__(self, list_of_formats):
        """
        This is the constructor function.
        It creates a new instance of the class.
        """
        self.list_of_formats = list_of_formats


    def add_formats(self, list_of_formats):
        self.list_of_formats = list_of_formats

    def add_format(self, str_format_name):
        self.list_of_formats.append(str_format_name)

    def _create_tar_family_archive(self, file_path, suffix_str, w_mode):

        tgz_path = file_path.split(".")[0] + suffix_str
        out_dir = file_path.split(".")[0]
        out_dir = out_dir.split("\\")
        out_dir = out_dir[len(out_dir) - 1] + "\\" + out_dir[len(out_dir) - 1] + suffix_str

        with tarfile.open(file_path.split(".")[0] + suffix_str, mode=w_mode) as tar:
            tar.add(file_path.split(".")[0] + suffix_str, arcname=out_dir)


    def convert(self, file_path, dest_format):
        print '{} {}'.format('Convert to format', dest_format)

        len_l = len(file_path.split("."))
        suffix_of_src_file = file_path.split(".")[len_l-1]

        if (suffix_of_src_file not in self.list_of_formats):
            print ("The file is not part of the family")

        if (suffix_of_src_file == "tar"):
            fp = tarfile.open(file_path, "r")
            fp.extractall()
            fp.close()

        if (suffix_of_src_file == "gz"):
            fp = tarfile.open(file_path, "r")
            fp.extractall()
            fp.close()

        if (suffix_of_src_file == "rar"):
            patoolib.extract_archive(file_path)

        if (dest_format == "tar"):
            self._create_tar_family_archive(file_path, ".tar", "w")

        if (dest_format == "gz"):
            self._create_tar_family_archive(file_path, ".tar.gz", "w:gz")

        if (dest_format == "rar"):
            patoolib.create_archive(file_path.split(".")[0]+".rar", (file_path.split(".")[0],))


    def is_format_compatible(self, format_name):
        if ( format_name in self.list_of_formats):
            return True
        else:
            return False

def build_parser():
    parser = argparse.ArgumentParser(description='This is a File converter')
    parser.add_argument('src_file', action="store", type=str)
    parser.add_argument('format_name', action="store", type=str)

    return parser




def main():
    options = build_parser().parse_args()

    lst_of_txt_formats = ["txt", "pdf", "doc"]
    lst_of_zip_formats = ["gz", "rar", "tar", "zip"]

    txtFamily = FilesFamily(lst_of_txt_formats)
    zipFamily = FilesFamily(lst_of_zip_formats)

    format_to_class_dict = {"rar":zipFamily, "gz":zipFamily, "tar":zipFamily, "txt":txtFamily}
    working_class = None

    if (options.format_name in format_to_class_dict.keys()):
        working_class = format_to_class_dict[options.format_name]
    else:
        print ("Incorrect format")
        exit

    if (working_class.is_format_compatible(options.format_name)):
        working_class.convert(options.src_file, options.format_name)
    else:
        print("Incompatible format")

if __name__ == "__main__":
    main()

