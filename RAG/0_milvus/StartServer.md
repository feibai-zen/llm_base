启动进程</br>
nohup milvus-lite server --data-dir ./milvus_demo.db --host 0.0.0.0 --port 19530 > milvus.log 2>&1 &

查找进程 ID</br>
pgrep -f "milvus-lite"

停止进程（替换 <PID> 为实际进程号）</br>
kill <PID>

或者强制停止</br>
kill -9 <PID>