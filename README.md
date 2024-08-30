# FocusOne 

Focus in one thing at the time for a period of time.

## Features 

- add new blocks and set info such as 
 - name 
 - duration
 - date
 - helpful programs (programs that will be used while the block is active)
 - helpful websites (websites that will be used while the block is active)
 - description

- list blocks 

-  show current block active: show current task and remaining task either in the
   status bar, or just overlaying the info in top of other windows.

## requirements 

This project only uses the python standard library, the only requirement is a working
python installation which comes in most linux distros

## Usage

name and duration is required
```console
add block 45m -d 05/20/2024 06:00  -desc "description"  -p neovim, chromium, -w "github.com","stack overflow"
```

by default it will show the blocks of today
```console
list 
```

```console
block 45m 06/20/2025  description 
    programs: nbeovim, chromium  
    websites: github.com, stack overflow 
```
shows the blocks in a calendar
```console
list -cal
````
