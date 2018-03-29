    
## “One Button Replace FSGUI”
### /home/jzhan107/spFSGUI
    the tool is placed in lsslogin1 server /home/jzhan107/bin/ folder
    the tool is used to package DB binary and fsgui binary and XSD files, ship to lab and replace the fsgui associating binary. 
#### option for the command ?
    /home/jzhan107/bin/spFSGUI -h 
    -d : escape packaging DB binary
    -D : escape shipping DB binary
    -f : escape packaging FSGUI binary
    -F : escape shipping FSGUI binary
    -x : escape shipping XSD files
    -h : get help

#### How to use ?
    /home/jzhan107/bin/spFSGUI -h 
    -d : escape packaging DB binary
    -D : escape shipping DB binary
    -f : escape packaging FSGUI binary
    -F : escape shipping FSGUI binary
    -x : escape shipping XSD files
    -h : get help
##### Notice:
    before use, you must in the ROOT of your fsgui development directory
##### /home/jzhan107/bin/spFSGUI qa24c
    will package below files and ship to LSP1 server, then to qa24c to replace fsgui in qa24c
    BLZDBlsspkg.zip
    DBCLIENTpkg.zip
    LCPDBlsspkg.zip
    fsguibin.tar(including host_manager .....)
##### /home/jzhan107/bin/spFSGUI qa24c
    will package below files and ship to LSP1 server, then to qa24c to replace fsgui in qa24c
    BLZDBlsspkg.zip
    DBCLIENTpkg.zip
    LCPDBlsspkg.zip
    $ROOT/fsgui/config/cfgschema/*.xsd
    fsguibin.tar(including host_manager .....)
##### /home/jzhan107/bin/spFSGUI -d qa24c
    if you want to escape package DB file because it has already been packaged in the build folder , will ship the binary to LSP1 server
##### /home/jzhan107/bin/spFSGUI -dD qa24c
    if you don't want to send DB file to LSP1 server, because there is binary in the server(the binary is under /home/jzhan107/fsgui/ folder in lsp1 server)
##### /home/jzhan107/bin/spFSGUI -dDfF qa24c
    if you want to escape DB & fsgui file(host_manager....) ship to LSP1 server, because there is binary in the server
##### /home/jzhan107/bin/spFSGUI -dDfFx qa24c
    if you want to escape DB & fsgui file(host_manager....) ship to LSP1 server, because there is binary in the server
##### and so on.......

## “One Button take your RCC & FScmd & MIcmd prim state back"
### /home/jzhan107/bin/PrimUp qa24c
  
## "One Button to package IMS/CFED/PFED and replace it to lab"
### /home/jzhan107/bin/sB CFED qa24c
### /home/jzhan107/bin/sB IMS qa24c
### /home/jzhan107/bin/sB PFED qa24c

## there are some shortcommings, I will continuously enhance the tool... 