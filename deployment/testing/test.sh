# #!/bin/bash

# # Get old version for be used as cache
# docker pull $CI_REGISTRY_IMAGE:$STAGE_ENVIRONMENT || true

# # Build it from cache
# docker build --cache-from $CI_REGISTRY_IMAGE:$STAGE_ENVIRONMENT \
# --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
# --tag $CI_REGISTRY_IMAGE:$STAGE_ENVIRONMENT \
# -f $DOCKER_FILE .

# # Push images
# docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
# docker push $CI_REGISTRY_IMAGE:$STAGE_ENVIRONMENT
# #
# #
# ## Running tests and save reports
# mkdir reports
# docker run --mount type=bind,src=$(pwd)/reports,dst=/app/reports $CI_REGISTRY_IMAGE:$STAGE_ENVIRONMENT
