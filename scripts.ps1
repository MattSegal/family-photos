param([String]$choice)

# Activate virtualenv
./env/Scripts/activate

function requirements {
    pip3 install -r ./photos/requirements/dev.txt
    pip3 install -r ./photos/requirements/deploy.txt
}

function lint {
    Write-Host "`nRunning isort`n"
    pushd links;isort -y;popd
    pushd api;isort -y;popd
    Write-Host "`nRunning Flake8`n"
    flake8 links
    flake8 api
}

function setup {
    vagrant up
    bash -c "ansible-playbook -i ./deploy/hosts-dev ./deploy/site.yml --vault-password-file ~/.vault-pass.txt"
}

function deploy {
    bash -c "ansible-playbook -i ./deploy/hosts-prod ./deploy/site.yml --vault-password-file ~/.vault-pass.txt"
}

function runserver {
    vagrant ssh -c 'sudo -i /srv/app/scripts/runserver.sh'
}

function gunicorn {
    vagrant ssh -c 'sudo -i /srv/app/scripts/start_gunicorn.sh staging'
}

function ssh {
    vagrant ssh -c 'sudo -i'
}

function sync {
    # sync prod/dev s3 buckets
}

function fetch {
    # fetch data from prod
}

switch ($choice) {
    'setup' {setup}
    'runserver' {runserver}
    'gunicorn' {gunicorn}
    'ssh' {ssh}
    'deploy' {deploy}
    'lint' {lint}
    Default {
        Write-Host "`n===== Scripts ====="
        Write-Host "setup       Setup dev environment"
        Write-Host "deploy      Deploy to prod"
        Write-Host "ssh         SSH into vagrant box"
        Write-Host "lint        Run linter"
        Write-Host "runserver   Run dev server on port 8080"
        Write-Host "gunicorn    Run gunicorn server on port 80"
    }
}
