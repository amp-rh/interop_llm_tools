podman run --rm --replace --device nvidia.com/gpu=0 --security-opt=label=disable -v ollama:/root/.ollama:z -p 11434:11434 --name ollama ollama/ollama
