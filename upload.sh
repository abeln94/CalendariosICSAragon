TAG=ics

# update tag
git tag --force $TAG
git push --force origin tag $TAG

# upload
# Note: sending one by one fails due to upload limits,
# so instead I upload them one by one, which works but it's too slow
# consider uploading in batches
for file in ics/*; do
  echo "Uploading $file"
  until gh release upload $TAG "$file" --clobber; do
    echo "Error, let's wait..."
    sleep 60
    echo "...and retry again"
  done
done