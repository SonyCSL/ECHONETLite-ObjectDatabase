#!/usr/bin/env ruby
#coding:utf-8

# you need google_drive gem before use this.
#  $ gem install google_drive

require "rubygems"
require "io/console"
require "google_drive"

def main
  if ARGV.size < 2 then
    puts "usage: ruby downloader.rb dist_dir"
    return 1
  end
  print "Input usermail: "
  username = STDIN.gets.chomp
  print "Input password: "
  password = STDIN.noecho(&:gets).chomp

  session = GoogleDrive.login(username,password)
  keys = ARGV[0]
  csv_dir = ARGV[1]
  # FIXME:rename worksheet name from jp to ja in google_drive.
  #  We don't want create following constant.
  lang_dir = ["en","ja"]

  puts "keyfile: " + keys
  puts "dist: " + csv_dir

  Dir::mkdir(csv_dir) unless FileTest.exist?(csv_dir)
  for lang in lang_dir
    new_dir = File.join(csv_dir,lang)
    Dir::mkdir(new_dir) unless FileTest.exist?(new_dir)
  end

  open(keys) {|file|
    while l = file.gets
      key = l.chomp
      sp = session.spreadsheet_by_key(key)
      sheet_title = sp.title

      is_device_list = sp.worksheets[0][6,1] != "EPC"
      class_name = sp.worksheets[0][2,1]
      group_code = sp.worksheets[0][2,3]
      class_code = sp.worksheets[0][2,4]

      csv_name = ""
      if is_device_list
        csv_name = "DeviceList"
      else
        if class_name == "" # it is device object.
          csv_name = "DeviceObject"
        else
          csv_name = group_code + class_code[2..-1]
        end
      end

      printf "%s -> %s (%s)\n",sheet_title,csv_name,key

      for i in 0..lang_dir.length-1
        dist_file = File.join(csv_dir,lang_dir[i],csv_name+".csv")
        sp.export_as_file(dist_file,nil,i)
      end
    end
  }

end

if __FILE__ == $0
  main()
end

