module example.com/main

go 1.21

replace example.com/external => ../external-module

require example.com/external v0.1.0
