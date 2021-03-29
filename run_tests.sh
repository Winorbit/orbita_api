CURRENT_COMMIT=$(git rev-parse --short HEAD)
TEST_IMAGE_TAG=api:$CURRENT_COMMIT
sudo docker build -t $TEST_IMAGE_TAG .
sudo docker run --env tesmode=true $TEST_IMAGE_TAG
