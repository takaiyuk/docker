#!/bin/bash
docker_run () {
    sudo docker run --runtime=nvidia -d --name test_ml-table-gpu -v ${PWD}:/workspace takaiyuk/ml-table-gpu
}
docker_exec () {
    sudo docker exec -it test_ml-table-gpu /bin/bash
}
run_test () {
    . /venv/bin/activate
    python tests/test_cudf.py
    python tests/test_lightgbm.py
    python tests/test_tensorflow.py
}
docker_kill () {
    sudo docker stop test_ml-table-gpu
    sudo docker rm test_ml-table-gpu
}

docker_run
docker_exec
run_test
docker_kill