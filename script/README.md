# Helper Scripts
This directory contains some scripts for database managements.
These scripts written in ruby require following packages.

- google_drive (https://github.com/gimite/google-drive-ruby)

To install these packages,use gem.
```
$ gem install google_drive
```

I checked ruby 1.9.3,2.1.1 on Linux.
Maybe, 1.9.2 or upper is OK.(nokogiri require 1.9.2)

## Downloader (downloader.rb)
Download csv files to local.

### Usage

```
$ ruby script/downloader.rb key/20140321.txt data/csv
```

Key file contains key for file on google_drive.
Each device and list has key,so number of key is 91.(2014/03/24)

## Validator (validator.rb)

Check file data on google drive.

### Usage

```
$ ruby script/validator.rb key/20140321.txt
```

See script source for info.
