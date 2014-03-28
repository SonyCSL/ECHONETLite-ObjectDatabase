#!/usr/bin/env python
#coding:utf-8

import csv
import string
import argparse
import os

class Validator:
    @classmethod
    def check_header(self,imag,real):
        for i,d in enumerate(imag):
            if d != real[i]:
                return False
        return True

    @classmethod
    def is_valid_bytes_string(self,s):
        if len(s) != 4:
            return False
        if s[0:2] != "0x":
            return False
        return all([c in string.hexdigits for c in s[2:]])

    @classmethod
    def is_valid_unit_string(self,s):
        return True

    @classmethod
    def is_valid_data_size(self,s):
        return s.isdecimal()

    @classmethod
    def is_valid_access_rule(self,s):
        return s in ["mandatory","optional","-"]

    @classmethod
    def is_valid_announcement(self,s):
        return s in ["mandatory","-"]
    
    @classmethod
    def check(self,data):
        return False

    @classmethod
    def check_devicelist(self,data):
        return False

    @classmethod
    def check_valid_text(self,s):
        return not "_x000a_" in s
    

class ValidatorEn(Validator):
    @classmethod
    def check_valid_class_header(self,header):
        imag = ["Class name","Remarks","Group code","Class code",
                "Whether or not detailed requirements are provided"]
        ok = self.check_header(imag,header)
        if not ok:
            print("Invalid class header " + str(header))
        return ok

    @classmethod
    def check_valid_epc_header(self,header):
        imag = ["EPC","Property name","Contents of property",
                "Value range(decimal notation)","Unit","Data type",
                "Data size","Access rule(Anno)","Access rule(Set)",
                "Access rule(Get)","Announcement at status change",
                "Remark"]
        ok = self.check_header(imag,header)
        if not ok:
            print("Invalid class header " + str(header))
        return ok

    @classmethod
    def check_valid_class_description(self,row):
        ret = True
        is_valid_group_code = self.is_valid_bytes_string(row[2])
        is_valid_class_code = self.is_valid_bytes_string(row[3])
        if not is_valid_group_code:
            print("Invalid group code " + row[2])
        if not is_valid_class_code:
            print("Invalid class code " + row[3])

        ret = ret and is_valid_group_code
        ret = ret and is_valid_class_code
        return ret

    @classmethod
    def check_valid_epc_row(self,row,i):
        valid = True
        is_valid_epc = self.is_valid_bytes_string(row[0])
        is_valid_unit = self.is_valid_unit_string(row[4])
        is_valid_data_size = self.is_valid_data_size(row[6])
        is_valid_access_rule_anno = self.is_valid_access_rule(row[7])
        is_valid_access_rule_set  = self.is_valid_access_rule(row[8])
        is_valid_access_rule_get  = self.is_valid_access_rule(row[9])
        is_valid_announcement_at_change = self.is_valid_announcement(row[10])

        if not is_valid_epc:
            print("Invalid EPC %s (%d,0)"%(row[0],i))
        if not is_valid_unit:
            print("Invalid Unit %s (%d,4)"%(row[4],i))

        if not is_valid_data_size:
            print("Invalid datasize %s (%d,6)"%(row[6],i))
        if not is_valid_access_rule_anno:
            print("Invalid Rule %s (%d,7)"%(row[7],i))
        if not is_valid_access_rule_set:
            print("Invalid Rule %s (%d,8)"%(row[8],i))
        if not is_valid_access_rule_get:
            print("Invalid Rule %s (%d,9)"%(row[9],i))
        if not is_valid_announcement_at_change:
            print("Invalid Rule %s (%d,10)"%(row[10],i))

        valid = valid and is_valid_epc
        valid = valid and is_valid_unit
        valid = valid and is_valid_data_size
        valid = valid and is_valid_access_rule_anno
        valid = valid and is_valid_access_rule_set
        valid = valid and is_valid_access_rule_get
        valid = valid and is_valid_announcement_at_change

        return valid

    @classmethod
    def check(self,data):
        ret = True
        ret = self.check_valid_class_header(data[0])      and ret
        ret = self.check_valid_epc_header(data[5])        and ret
        ret = self.check_valid_class_description(data[1]) and ret
        for i,row in enumerate(data[6:]):
            ret = self.check_valid_epc_row(row,i+6)         and ret
        return ret

class ValidatorJa(Validator):
    @classmethod
    def check_valid_class_header(self,header):
        imag = ["クラス名","備考"]
        ok = self.check_header(imag,header)
        if not ok:
            print("Invalid class header " + str(header))
        return ok

    @classmethod
    def check_valid_epc_header(self,header):
        imag = ["EPC","Property name","Contents of property",
                  "Value range(decimal notation)"]
        ok = self.check_header(imag,header)
        if not ok:
            print("Invalid class header " + str(header))
        return ok

    @classmethod
    def check_valid_epc_row(self,row,i):
        valid = True
        is_valid_epc = self.is_valid_bytes_string(row[0])

        if not is_valid_epc:
            print("Invalid EPC %s (%d,1)"%(row[0],i))

        valid = valid and is_valid_epc
        return valid

    @classmethod
    def check(self,data):
        ret = True
        ret = self.check_valid_class_header(data[0]) and ret
        ret = self.check_valid_epc_header(data[5])   and ret
        return ret

def listdir_dironly(dir):
    return [os.path.join(dir,f) for f in os.listdir(dir)
            if os.path.isdir(os.path.join(dir,f))]

def list_csv_files(dir):
    return [os.path.join(dir,f) for f in os.listdir(dir)
            if not os.path.isdir(os.path.join(dir,f))
               and os.path.splitext(f)[1] == ".csv"]

def scan_top(dir):
    langs = listdir_dironly(dir)
    for lang in langs:
        base = os.path.basename(lang)
        print(base + " (" + lang + ")")
        files = list_csv_files(lang)
        print(" cnt:" + str(len(files)))
        files.sort()
        checked = 0
        passed = 0
        for f in files:
            print(f)
            csv_file_name = os.path.basename(f)
            group_class,ext = os.path.splitext(csv_file_name)
            is_devicelist = group_class == "DeviceList"
            with open(f) as csv_file:
                reader = csv.reader(csv_file)
                ret = True
                if base == "ja":
                    if is_devicelist:
                        ret = ValidatorJa.check_devicelist(list(reader))
                    else:
                        ret = ValidatorJa.check(list(reader))
                elif base == "en":
                    if is_devicelist:
                        ret = ValidatorEn.check_devicelist(list(reader))
                    else:
                        ret = ValidatorEn.check(list(reader))
                else:
                    print("There is no Validator for " + base)
                    ret = False
                if ret:
                    passed += 1
                    print("\033[0;32m -> passed \033[0;39m")
                else:
                    print("\033[0;31m -> failed \033[0;39m")
                checked += 1

        if checked == passed:
            print("\033[0;32mAll %d test Passed!! \033[0;39m"%(checked))
        else:
            print("\033[0;31mSome test failed.Number of failed count is (%d/%d)\033[0;39m"
                  %(checked-passed,checked))
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_directory",
                        help="directory that contains csv directory(ja,en,..).")
    args = parser.parse_args()
    scan_top(args.target_directory)


if __name__ == "__main__":
    main()
