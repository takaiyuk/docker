#!/bin/bash
docker_run () {
    docker run --runtime=nvidia -it -d --name test_ml-multimodal-ja-gpu -v ${PWD}:/workspace takaiyuk/ml-multimodal-ja-gpu
}
docker_exec () {
    docker exec -it test_ml-multimodal-ja-gpu /bin/bash
}
run_test () {
    . /venv/bin/activate
    python tests/test_cudf.py
    python tests/test_lightgbm.py
    python tests/test_tensorflow.py
}
docker_kill () {
    docker stop test_ml-multimodal-ja-gpu
    docker rm test_ml-multimodal-ja-gpu
}

docker_run
docker_exec
# run_test
docker_kill
