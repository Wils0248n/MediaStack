docker build -t mediastack-image .
docker create \
  --name=mediastack \
  -e PUID=1000 \
  -e PGID=1000 \
  -p 8000:5000 \
  -v $(pwd):/app \
  --restart unless-stopped \
  mediastack_image
