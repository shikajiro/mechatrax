script_dir=$(cd $(dirname $0); pwd)
root_dir=${script_dir}/../

${script_dir}/zip_packages.sh # function.zip
aws lambda update-function-code \
--function-name my-function \
--zip-file fileb://function.zip
rm ${root_dir}/function.zip