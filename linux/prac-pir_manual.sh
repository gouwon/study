#!/usr/bin/sh

## THIS FOR TEMP PIR SHELL SCRIPT.
echo "START Periodic Inspection Reporting Program"

echo "SERVERNAME : "`hostname`
echo "==========================================="
echo "UPTIME"
UPTIME_RESULT=`uptime | awk '{print $1}'`
echo $UPTIME_RESULT
echo "==========================================="
echo "Firewalld"
FIREWALLD_RESULT=`sudo systemctl status firewalld | grep Active | awk '{print $2}'`
echo $FIREWALLD_RESULT
echo "==========================================="
echo "Selinux"
SELINUX_RESULT=`sestatus | grep -E "SELinux status" | awk '{print $3}'`
echo $SELINUX_RESULT
echo "==========================================="
echo "Filesystem Mount(/etc/fstab)"
FSTAB_RESULT=`awk '$3 == "xfs" {print $1}' /etc/fstab`
for SUB_RESULT in $FSTAB_RESULT
do
     echo $SUB_RESULT
done
echo "==========================================="
echo "CPU(idle)"
## procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
## r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
## 1  2      3      4      5      6    7    8     9    10   11   12 13 14 15 16 17
CPU_RESULT=`vmstat | awk 'match($15, /[0-9].*/) {print $15}'`
echo $CPU_RESULT"%"
echo "==========================================="
echo "MEMORY(free)"
##               total        used        free      shared  buff/cache   available
## Mem:        1882072      468612      860384       20828      553076     1217432
## Swap:       1679356           0     1679356
## 1                 2           3           4           5           6           7
MEMORY_RESULT=`free | grep "Mem:" | awk '{print $4/$2*100}'`
echo $MEMORY_RESULT"%"
echo "==========================================="
echo "PROCESS"
PROCESS_RESULT=`cat /proc/*/status | grep State | sort -u`
echo $PROCESS_RESULT
echo "==========================================="
echo "Filesystem Usage"
## Filesystem              Type      Size  Used Avail Use% Mounted on
## devtmpfs                devtmpfs  903M     0  903M   0% /dev
## 1                       2         3        4     5    6          7
FILESYSTEM_RESULT=`df -hT | awk '$2 == "xfs" {printf("%s(%s):%d%\n", $1, $7, $6)}'`
for SUB_RESULT in $FILESYSTEM_RESULT
do
    echo $SUB_RESULT
done
echo "==========================================="
echo "NIC"
ip addr
echo "==========================================="
echo "Routing Table"
netstat -rn
echo "==========================================="
echo "Booting Error"
dmesg | grep -E "fail|Fail"
echo "==========================================="

echo "END Periodic Inspection Reporting Program"
