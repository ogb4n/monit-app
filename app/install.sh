#!/bin/bash

USER=$(logname)
APP_USER="monit"
GROUP="monitgroup"

LOG_DIRECTORY="/var/log/monit"
REPORT_DIRECTORY="/var/monit/reports"
CONF_DIRECTORY="/etc/monit"
APP_DIRECTORY="/var/monit"

SERVICE_DESCRIPTION="Monit app written with flask"
CRON_TIMER=$(jq -r '.cron_timer' /etc/monit/config.json)

CONFIG_JSON=$(<config.json.example)


if [ -f /etc/os-release ] && grep -q 'Rocky Linux' /etc/os-release; then
    echo "Installing jq on Rocky Linux..."
    dnf install -y jq
fi

dnf install -y pip

if [ "$EUID" -ne 0 ]; then  
    echo "Erreur : Ce script doit être exécuzté avec sudo."
    exit 1
fi

if id "$APP_USER" &>/dev/null; then
    echo "L'utilisateur $APP_USER existe déjà."
else
    useradd -M -s /sbin/nologin $APP_USER
    echo "Utilisateur $APP_USER créé avec succès."
fi

if grep -q "^$GROUP:" /etc/group; then
    echo "Le groupe $GROUP existe déjà."
else
    # Créer le groupe s'il n'existe pas
    sudo groupadd $GROUP
    echo "Le groupe $GROUP a été créé avec succès."
fi

usermod -aG $GROUP $USER
usermod -aG $GROUP $APP_USER

configure_paths() {

    echo "Configuration des permissions pour le dossier log..."
    mkdir -p "$LOG_DIRECTORY"
    chown -R "$APP_USER":"$GROUP" "$LOG_DIRECTORY"
    echo "Permissions configurées avec succès pour $LOG_DIRECTORY"

    echo "Configuration des permissions pour le dossier de l'application..."
    mkdir -p "$APP_DIRECTORY"
    chown -R "$APP_USER":"$GROUP" "$APP_DIRECTORY"
    echo "Permissions configurées avec succès pour $APP_DIRECTORY"

    echo "Configuration des permissions pour le dossier de configuration..."
    mkdir -p "$CONF_DIRECTORY"
    chown -R "$APP_USER":"$GROUP" "$CONF_DIRECTORY"
    echo "Permissions configurées avec succès pour $CONF_DIRECTORY"

    echo "Configuration des permissions pour le dossier de rapport..."
    mkdir -p "$REPORT_DIRECTORY"
    chown -R "$APP_USER":"$GROUP" "$REPORT_DIRECTORY"
    echo "Permissions configurées avec succès pour $REPORT_DIRECTORY"

    echo "Création du fichier de configuration"
    echo "$CONFIG_JSON" > "/etc/monit/config.json"
    echo "Fichier de configuration copié avec succès dans $CONF_DIRECTORY"

    echo "Configuration des chemins terminée."
 
}

configure_paths

if grep -q '"local_api_mode": true' "/etc/monit/config.json"; then

    echo "local_api_mode = true | Configuration de l'API locale..."
    cp -r ../api $APP_DIRECTORY/api 
    echo "API locale copiée avec succès dans $APP_DIRECTORY/api"
    chown -R "$APP_USER":"$GROUP" "$APP_DIRECTORY/api"
    echo "Permissions configurées avec succès pour $APP_DIRECTORY/api"
    cp -r ../app/ $APP_DIRECTORY/app
    echo " "

    pip install flask pymongo dnspython psutil requests
    cat <<EOF > /etc/systemd/system/monit-api.service
[Unit]
Description=$SERVICE_DESCRIPTION
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIRECTORY/api
ExecStart=/usr/bin/python3 /var/monit/api/monit-api.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    echo "Service API configuré avec succès."
    echo " "

    systemctl daemon-reload

    echo "Démarrage du service API"
    systemctl enable monit-api
    systemctl start monit-api

    systemctl status monit-api | grep active 
    echo 'q'
    echo "Service API démarré avec succès."
else
    echo "local_api_mode = false | Configuration sans l'API locale..."
    cp ../app/ $APP_DIRECTORY/app
    echo "Application copiée avec succès dans $APP_DIRECTORY/app"
    echo " "
    pip install flask pymongo dnspython psutil requests
fi

echo "alias monit='python /var/monit/app/monit.py'" >> /home/$USER/.bashrc
source /home/$USER/.bashrc
echo "Configuration des alias terminée."
echo " "

echo "*/5 * * * * monit -c" >> /tmp/cron_temp
crontab -u monit /tmp/cron_temp
rm /tmp/cron_temp

echo "Configuration de la routine terminée."
echo " "

chown -R $USER /var/monit
chown -R $USER /var/log/monit
bash



echo "Configuration terminée. Vous pouvez maintenant utiliser le programme."
echo "Pour avoir une liste des commandes disponibles, tapez 'monit -h'."