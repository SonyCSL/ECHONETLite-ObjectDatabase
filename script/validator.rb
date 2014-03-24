#!/usr/bin/env ruby
#coding:utf-8

# you need google_drive gem before use this.
#  $ gem install google_drive

require "rubygems"
require "io/console"
require "google_drive"

# check epc or groupcode or classcode is valid.
# ex. 0x80 -> true
#     0x8 0 -> false
#     0x80\n -> false

def is_valid_bytes_string(s)
  if not s.length == 4
    return false
  end
  if not s[0,2] == "0x"
    return false
  end
  !s[2..-1][/\H/]
end

def is_valid_unit_string(s)
  not s.include?("—")
end

def check_valid_en(ws)
  def is_valid_header(ws)
    valid = true
    header = ["Class name","Remarks","Group code","Class code",
              "Whether or not detailed requirements are provided"]
    for c in 1..(header.length)
      if not ws[1,c] == header[c-1]
        valid = false
        printf "Invalid header %s (1,%d)\n",ws[1,c],c
      end
    end
    return valid
  end

  def is_valid_epc_header(ws)
    valid = true
    header = ["EPC","Property name","Contents of property",
              "Value range(decimal notation)","Unit","Data type",
              "Data size","Access rule(Anno)","Access rule(Set)",
              "Access rule(Get)","Announcement at status change",
              "Remark"]
    for c in 1..(header.length)
      if not ws[6,c] == header[c-1]
        valid = false
        printf "Invalid header %s (6,%d)\n",ws[6,c],c
      end
    end
    return valid
  end

  def is_valid_group_code(ws)
    valid = is_valid_bytes_string ws[2,3]
    if not valid
      printf "Invalid groupcode %s (2,3)\n",ws[2,3]
    end
    return valid
  end

  def is_valid_class_code(ws)
    valid = is_valid_bytes_string ws[2,4]
    if not valid
      printf "Invalid classcode %s (2,4)\n",ws[2,4]
    end
    return valid
  end

  def is_valid_epc_row(ws,r)
    valid = true
    is_valid_epc = is_valid_bytes_string ws[r,1]
    if not is_valid_epc
      printf "Invalid epc notation %s (%d,1)\n",ws[r,1],r
    end
    valid = valid && is_valid_epc

    is_valid_unit = is_valid_unit_string ws[r,2]
    if not is_valid_unit
      printf "Invalid unit notation %s (%d,1)\n",ws[r,2],r
    end
    valid = valid && is_valid_unit
    return valid
  end


  ret = true # is_all_test_passed
  ret = (is_valid_header ws)     && ret
  ret = (is_valid_epc_header ws) && ret
  ret = (is_valid_group_code ws) && ret
  ret = (is_valid_class_code ws) && ret

  ret = (is_valid_header ws)     && ret
  for r in 7..ws.num_rows
    ret = (is_valid_epc_row ws,r) && ret
  end
  return ret
end

def check_valid_ja(ws)
  def is_valid_header(ws)
    valid = true
    header = ["クラス名","備考"]
    for c in 1..(header.length)
      if not ws[1,c] == header[c-1]
        valid = false
        printf "Invalid header %s (1,%d)\n",ws[1,c],c
      end
    end
    valid
  end

  def is_valid_epc_header(ws)
    valid = true
    header = ["EPC","Property name","Contents of property",
              "Value range(decimal notation)"]
    for c in 1..(header.length)
      if not ws[6,c] == header[c-1]
        valid = false
        printf "Invalid header %s (6,%d)\n",ws[6,c],c
      end
    end
    valid
  end

  def is_valid_epc_row(ws,r)
    valid = is_valid_bytes_string ws[r,1]
    if not valid
      printf "Invalid epc notation %s (%d,1)\n",ws[r,1],r
    end
    valid
  end

  ret = true
  ret = (is_valid_header ws)     && ret
  ret = (is_valid_epc_header ws) && ret
  for r in 7..ws.num_rows
    ret = (is_valid_epc_row ws,r) && ret
  end
  ret
end


def main
  if ARGV.size < 1 then
    puts "usage ruby validator.rb keys"
    return 1
  end
  print "Input usermail: "
  username = STDIN.gets.chomp
  print "Input password: "
  password = STDIN.noecho(&:gets).chomp

  session = GoogleDrive.login(username,password)
  keys = ARGV[0]
  puts "\nkeyfile: " + keys
  allcnt = 0
  success = 0
  open(keys) {|file|
    while l = file.gets
      key = l.chomp
      sp = session.spreadsheet_by_key(key)
      dev_name = sp.worksheets[0][11,3]
      printf "%s / %s\n",sp.title,key
      if sp.title == "Device List"
      else
        allcnt += 1
        valid = true
        valid = (check_valid_en sp.worksheets[0]) && valid
        valid = (check_valid_ja sp.worksheets[1]) && valid
        if valid
          printf "\033[0;32m -> passed \033[0;39m \n"
          success += 1
        else
          printf "\033[0;31m -> failed \033[0;39m \n"
        end
      end
    end
  }
  printf "Test done.\n"
  if allcnt == success
    printf "\033[0;32mAll %d test Passed!! \033[0;39m\n",allcnt
  else
    printf "\033[0;31mSome test failed.Number of failed count is (%d/%d)\033[0;39m\n",allcnt-success,allcnt
  end
end

if __FILE__ == $0
  main()
end

