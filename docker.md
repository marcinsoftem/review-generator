```bash

# build docker image
docker build -t adm-tool:0.1.1 .

# run docker image
docker run -p 8503:8501 -d adm-tool:0.1.1

```