TAG=ics

# update tag
git tag --force $TAG
git push --force origin tag $TAG

# upload
upload () {
  file=$*

  echo "Uploading $file"
  until gh release upload $TAG $file --clobber; do
    echo "Error, let's wait..."
    sleep 60
    echo "...and retry again"
  done
}
export -f upload

# Note: sending everything at one go fails due to upload limits, so instead I upload them in batches
cd ics
ls | xargs -L 50 bash -c 'upload $@' _
