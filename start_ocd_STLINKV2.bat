cd openocd-0.10.0/bin-x64/
openocd -f interface/stlink-v2.cfg -c "transport select hla_swd" -f target/stm32f1x.cfg
pause