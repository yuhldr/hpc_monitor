#! /bin/sh

curPath=$(readlink -f "$(dirname "$0")")

for node in node1 node2 node3 node4 node5 node6 node7 node8;
do
  ssh $node "top -b -n 1" > $curPath/top$node
done
