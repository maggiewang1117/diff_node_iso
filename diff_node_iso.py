__author__ = 'huiwa'


#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import difflib
import sys
import re
import os
import logging

class DiffManifest(object):
    def __init__(self, iso1, iso2):
        self.iso1 = iso1
        self.iso2 = iso2

    def setup_logger(self):
        self.logger = logging.getLogger("DiffISO")
        ch = logging.StreamHandler()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        return self.logger
        

    def mount_iso_to_local_dir(self, iso, logger):
        base_iso_name = os.path.basename(iso)
        dir_name = "/home/huiwa/test/%s" % base_iso_name
        if os.path.exists(dir_name):
            os.system("mount -o loop %s %s" % (iso, dir_name))
        else:
            os.system("mkdir -p %s" % dir_name)
            os.system("mount -o loop %s %s" % (iso, dir_name))
        self.logger.info("mount %s to %s succeed!" % (iso, dir_name))
        return dir_name

    def write_srpm_to_list(self, dirpath, logger):
        rpm_path = "isolinux/manifest-srpm.txt"
        filepath = "%s/%s" % (dirpath, rpm_path)
        if os.path.exists(filepath):
            f = open(filepath, "r")
            f1 = f.readlines()
        list1 = []
        for i in xrange(len(f1)):
            list1.append(re.sub("\(.*\)", "", f1[i]))
        f.close()
        return list1

    def diff_manifest(self,list1, list2, logger):
        diff = difflib.ndiff(list1, list2)
        write_to_file = "/home/huiwa/manifest_diff1.txt"
        f = open(write_to_file, "w")
        for i in diff:
            f.writelines(i)
        return write_to_file

    def deal_the_result(self,filename, logger):
        f2 = open("/home/huiwa/manifest_diff.txt", "w+")
        f2.writelines("-%s\n" % self.iso1)
        f2.writelines("+%s\n" % self.iso2)
        with open(filename, "r") as f:
            for i in f.readlines():
                if i.startswith("-"):
                    f2.writelines(i)
                elif i.startswith("+"):
                    f2.writelines(i)
                else:
                    pass
        self.logger.info("write diff result to /home/huiwa/manifest_diff.txt")
        f2.close()

    def umount_iso(self, iso, logger):
        base_iso_name = os.path.basename(iso)
        dir_name = "/home/huiwa/test/%s" % base_iso_name
        if os.path.exists(dir_name):
            os.system("umount %s" % dir_name)
        else:
            pass
        self.logger.info("umount %s succeed!" % dir_name)

    def remove_dir(self, dirname):
        os.system("rm -rf %s" % dirname)

    def clear_env(self, iso1, iso2,dirname1, dirname2,logger):
        self.umount_iso(iso1, logger)
        self.umount_iso(iso2, logger)
        self.remove_dir(dirname1)
        self.remove_dir(dirname2)
        os.system("rm -rf /home/huiwa/manifest_diff1.txt")

    def run(self):
        logger = self.setup_logger()
        dirname1 = self.mount_iso_to_local_dir(self.iso1, logger)
        dirname2 = self.mount_iso_to_local_dir(self.iso2, logger)
        list1 = self.write_srpm_to_list(dirname1, logger)
        list2 = self.write_srpm_to_list(dirname2, logger)
        file1 = self.diff_manifest(list1, list2, logger)
        self.deal_the_result(file1, logger)
        self.clear_env(self.iso1, self.iso2, dirname1, dirname2, logger)

if __name__ == "__main__":
    iso_name1 = os.path.basename(sys.argv[1])
    iso_name2 = os.path.basename(sys.argv[2])
    diff_manifest = DiffManifest(sys.argv[1], sys.argv[2])
    diff_manifest.run()





