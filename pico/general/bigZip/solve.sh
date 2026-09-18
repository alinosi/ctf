for file in $(unzip -Z1 big-zip-files.zip); do
    unzip -p big-zip-files.zip "$file" | grep -q "picoCTF{" && echo "Ketemu di: $file"
done
