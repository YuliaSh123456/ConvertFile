import sys
import argparse
import gzip
import shutil
import tarfile
import rarfile

class clFilesFamily:

    def __init__(self, list_of_formats):
        """
        This is the constructor function.
        It creates a new instance of the class.
        """
        self.list_of_formats = list_of_formats


    def AddFormats(self, list_of_formats):
        self.list_of_formats = list_of_formats

    def AddFormat(self, str_format_name):
        self.list_of_formats.append(str_format_name)

    def Convert(self, file_path, dest_format):
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
            fp = rarfile.open(file_path, "r:gz")
            fp.extractall()
            fp.close()

        if (dest_format == "tar"):
            suffix_str = ".tar"
            w_mode = "w"

        if (dest_format == "gz"):
            suffix_str = ".tar.gz"
            w_mode = "w:gz"

        if (dest_format == "rar"):
            suffix_str = ".tar.gz"
            w_mode = "w:gz"

        tgz_path = file_path.split(".")[0] + suffix_str
        out_dir = file_path.split(".")[0]
        out_dir = out_dir.split("\\")
        out_dir = out_dir[len(out_dir) - 1] + "\\" + out_dir[len(out_dir) - 1] + suffix_str

       # with tarfile.open(file_path.split(".")[0]+".tar.gz", mode="w:gz") as tar:
       #     tar.add(file_path.split(".")[0] + ".tar.gz", arcname='backup\\backup.tar.gz')
        with tarfile.open(file_path.split(".")[0] + suffix_str, mode=w_mode) as tar:
            tar.add(file_path.split(".")[0] + suffix_str, arcname=out_dir)

        #if (dest_format == "rar"):


    def IsFormatCompatible(self, format_name):
        if ( format_name in self.list_of_formats):
            return True
        else:
            return False

def build_parser():
    parser = argparse.ArgumentParser(description='This is a File converter')
    parser.add_argument('src_file', action="store", type=str)
    parser.add_argument('format_name', action="store", type=str)

    parse_results = parser.parse_args()

    return parse_results


def main():
    parser = build_parser()
    lst_of_txt_formats = ["txt", "pdf", "doc"]
    lst_of_zip_formats = ["gz", "rar", "tar", "zip"]

    txtFamily = clFilesFamily(lst_of_txt_formats)
    zipFamily = clFilesFamily(lst_of_zip_formats)

    format_to_class_dict = {"rar":zipFamily, "gz":zipFamily, "tar":zipFamily, "txt":txtFamily}
    working_class = None

    if (parser.format_name in format_to_class_dict.keys()):
        working_class = format_to_class_dict[parser.format_name]
    else:
        print ("Incorrect format")
        exit

    if (working_class.IsFormatCompatible(parser.format_name)):
        working_class.Convert(parser.src_file, parser.format_name)
    else:
        print("Incompatible format")

if __name__ == "__main__":
    main()

