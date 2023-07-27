#! /bin/sh

#curPath=$(readlink -f "$(dirname "$0")")
curPath=/home/data/ns_state


for ns in ns1 ns2 ns3 ns4;
do
  ssh $ns "sar -P ALL 1 2" > $curPath/sar_p_$ns
  ssh $ns "sar -r 3 2" > $curPath/sar_r_$ns
done

