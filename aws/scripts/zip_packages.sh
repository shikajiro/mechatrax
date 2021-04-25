script_dir=$(cd $(dirname $0); pwd)
root_dir=${script_dir}/../

cd ${root_dir}/.direnv/python-3.9.2/lib/python3.9/site-packages
zip -r ${root_dir}/function.zip .
cd ${root_dir}
zip -g function.zip main.py