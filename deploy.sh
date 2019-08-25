#!/bin/bash


# Directories structure of deployment
# /var
# ├── lib
# │   ├── local_settings	
# │   │   ├── project
# │   │   ├── project-staging
# │   │   └── project-test
# │   └── venv
# │       ├── project
# │       ├── project-staging
# │       └── project-test
# ├── log
# │   ├── project
# │   └── project-staging
# ├── media
# │   ├── project
# │   └── project-staging
# ├── static
# │   ├── project
# │   └── project-staging
# └── www
#     ├── project
#     └── project-staging


ret=0
_pwd=`pwd`
cwd=`dirname $_pwd/$0`
production_name=dian_recruit
staging_name=dian_recruit-staging


config() {
    name=$1
    user=www-data
    group=www-data

    prefix=/var/www
    logging_prefix=/var/log
    media_prefix=/var/media
    static_prefix=/var/static
    venv_prefix=/var/lib/venv
    local_settings_prefix=/var/lib/local_settings


    if [ -d "/etc/supervisor" ]; then
        supervisor_prefix=/etc/supervisor/conf.d
        supervisor_config=$supervisor_prefix/$name.conf
    else
        supervisor_prefix=/etc/supervisord.d
        supervisor_config=$supervisor_prefix/$name.ini
    fi

    gitrev=$(git rev-parse --short HEAD)

    dest=$prefix/$name
    logging_path=$logging_prefix/$name
    media_path=$media_prefix/$name
    static_path=$static_prefix/$name

    venv_name=$name-$gitrev
    venv_path=$venv_prefix/$venv_name
    venv_python=$venv_path/bin/python
    venv_gunicorn=$venv_path/bin/gunicorn

    local_settings_path=$local_settings_prefix/$name
}


print_info() {
    echo "name: $name"
    echo "user: $user"
    echo "group: $group"
    echo "prefix: $prefix"
    echo "logging_prefix: $logging_prefix"
    echo "media_prefix: $media_prefix"
    echo "static_prefix: $static_prefix"
    echo "venv_prefix: $venv_prefix"
    echo "local_settings_prefix: $local_settings_prefix"
    echo "supervisor_prefix: $supervisor_prefix"
    echo "gitrev: $gitrev"
    echo "dest: $dest"
    echo "logging_path: $logging_path"
    echo "media_path: $media_path"
    echo "static_path: $static_path"
    echo "venv_name: $venv_name"
    echo "venv_path: $venv_path"
    echo "venv_python: $venv_python"
    echo "local_settings_path: $local_settings_path"
    echo "supervisor_config: $supervisor_config"
}


print_full_info() {
    echo -e "cwd: $cwd\n"

    echo "[staging] info"
    config dian_recruit-staging
    print_info
    echo "staging_db: $staging_db"

    echo

    echo "[production] info"
    config dian_recruit
    print_info
    echo "production_db: $production_db"
}


local_settings() {
    echo 'retrive local settings'
    # -n option means no override
    cp -r -n $local_settings_path/* $cwd
}


install() {
    mkdir -p $dest
    rsync -av --del --progress --exclude .git/ $cwd/ $dest/
    chown -R $user:$group $dest
}


create_venv() {
    mkdir -p $venv_prefix
    virtualenv -p python3 $venv_path
    $venv_python -m pip install -r $dest/requirements.txt
}


pre_run() {
    cd $dest
    mkdir -p $logging_path
    mkdir -p $media_path
    mkdir -p $static_path
    chown -R $user:$group $logging_prefix $media_path $static_path
    $venv_python manage.py migrate --noinput
    $venv_python manage.py collectstatic --noinput
    cat << EOF | tee $supervisor_config
[program:$name]
command=$venv_gunicorn -c gunicorn.conf.py Dian.wsgi:application
directory=$dest
EOF
}



run() {
    if supervisorctl reread | grep -q $name; then
        # update when configuration changed
        supervisorctl update
        ret=$?
    else
        # restart or just start when configuration unchanged
        if supervisorctl status | grep -q "$name "; then
            if supervisorctl status | grep "$name " | grep -q RUNNING; then
                echo "restarting $name"
                supervisorctl restart $name
                ret=$?
            else
                echo "starting $name"
                supervisorctl start $name
                ret=$?
            fi
        fi
    fi
}


clean_run() {
    cd $venv_prefix
    # 删除其它虚拟环境
    find . -maxdepth 1 -regextype sed -regex "./$name-\S\{7\}" ! -name $venv_name | xargs rm -rf
    # 如果运行失败，则删除当前虚拟环境
    if [ $ret -ne 0 ]; then rm -rf $venv_name; fi
}


staging() {
    config $staging_name

    local_settings

    install

    create_venv

    pre_run

    run

    clean_run
}


production() {
    config $production_name

    local_settings

    install

    create_venv

    pre_run

    run

    clean_run
}


help() {
  echo "Usage:"
  echo "$0 info: Show variables"
  echo "$0 staging: Deploy this application in staging environment"
  echo "$0 production: Deploy this application in production environment"
}


case "$1" in
  info)
    print_full_info
    ;;
  staging)
    staging
    ;;
  production)
    production
    ;;
  *)
    help
    ;;
esac

exit $ret