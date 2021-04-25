script_dir=$(cd $(dirname $0); pwd)
root_dir=${script_dir}/../

${script_dir}/zip_packages.sh # function.zip
aws lambda create-function \
--function-name my-function \
--zip-file fileb://function.zip \
--handler main.handler \
--runtime python3.8 \
--role arn:aws:iam::304683766238:role/lambda-ex
rm ${root_dir}/function.zip
