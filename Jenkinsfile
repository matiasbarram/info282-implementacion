pipeline {
    agent none
    stages{
        stage('Archive') {
            agent {
                label 'master'
            }
                steps {
                    archiveArtifacts '**'
                }
        }
        stage('Deploy') {
            agent {
                label 'master'
            }
            options {
                skipDefaultCheckout()
            }
            steps {
                sh 'rm -rf /var/www/tent'
                sh 'mkdir /var/www/tent'
                sh 'cp -Rp ** /var/www/tent'
                sh 'docker stop tent || true && docker rm tent || true'
                sh 'docker run -dit --name tent -p 8008:80 -v /var/www/tent/:/var/www/tent srittau/wsgi-base:latest'
                sh 'docker cp /var/www/tent/tent.conf tent:/etc/apache2/sites-available/'
                sh 'docker exec tent pip install -r /var/www/tent/requirements.txt'
                sh 'docker exec tent a2dissite 000-default.conf'
                sh 'docker exec tent a2ensite tent.conf'
                sh 'docker exec tent /etc/init.d/apache2 reload'
                // sh 'docker exec tent service apache2 restart'
            }
        }
    }
}