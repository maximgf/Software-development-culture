# Установка и настройка ELK-стека (Elasticsearch, Logstash, Kibana)


## Установка Elasticsearch

### Для Debian/Ubuntu:

1. Импортируйте ключ репозитория:
   ```bash
   wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
   ```

2. Установите необходимые пакеты:
   ```bash
   apt install apt-transport-https
   ```

3. Добавьте репозиторий:
   ```bash
   echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list
   ```

4. Установите Elasticsearch:
   ```bash
   apt update && apt install elasticsearch
   ```

### Для CentOS/RHEL:

1. Импортируйте ключ репозитория:
   ```bash
   rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
   ```

2. Добавьте репозиторий:
   ```bash
   cat > /etc/yum.repos.d/elasticsearch.repo <<EOF
   [elastic-8.x]
   name=Elastic repository for 8.x packages
   baseurl=https://artifacts.elastic.co/packages/8.x/yum
   gpgcheck=1
   gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
   enabled=1
   autorefresh=1
   type=rpm-md
   EOF
   ```

3. Установите Elasticsearch:
   ```bash
   yum install elasticsearch
   ```

### Настройка и запуск Elasticsearch

1. Включите и запустите службу:
   ```bash
   systemctl daemon-reload
   systemctl enable elasticsearch.service
   systemctl start elasticsearch.service
   ```

2. Проверьте статус:
   ```bash
   systemctl status elasticsearch.service
   ```

3. Проверьте работу (используйте пароль, выданный при установке):
   ```bash
   curl -k --user elastic:'your_password' https://127.0.0.1:9200
   ```

## Установка Kibana

### Для Debian/Ubuntu:

```bash
apt install kibana
```

### Для CentOS/RHEL:

```bash
yum install kibana
```

### Настройка и запуск Kibana

1. Настройте подключение к Elasticsearch в `/etc/kibana/kibana.yml`:
   ```yaml
   elasticsearch.hosts: ["https://localhost:9200"]
   elasticsearch.username: "kibana_system"
   elasticsearch.password: "your_kibana_system_password"
   elasticsearch.ssl.certificateAuthorities: [ "/etc/kibana/certs/http_ca.crt" ]
   ```

2. Скопируйте сертификаты:
   ```bash
   cp -R /etc/elasticsearch/certs /etc/kibana
   chown -R root:kibana /etc/kibana/certs
   ```

3. Включите и запустите службу:
   ```bash
   systemctl enable kibana.service
   systemctl start kibana.service
   ```

4. Проверьте статус:
   ```bash
   systemctl status kibana.service
   ```

5. Доступ к веб-интерфейсу: `http://your_server_ip:5601`

## Установка Logstash

### Для Debian/Ubuntu:

```bash
apt install logstash
```

### Для CentOS/RHEL:

```bash
yum install logstash
```

### Настройка Logstash

1. Создайте конфигурационные файлы в `/etc/logstash/conf.d/`:

   - `input.conf`:
     ```conf
     input {
       beats {
         port => 5044
       }
     }
     ```

   - `filter.conf`:
     ```conf
     filter {
      if [type] == "nginx_access" {
         grok {
             match => { "message" => "%{IPORHOST:remote_ip} - %{DATA:user} \[%{HTTPDATE:access_time}\] \"%{WORD:http_method} %{DATA:url} HTTP/%{NUMBER:http_version}\" %{NUMBER:response_code} %{NUMBER:body_sent_bytes} \"%{DATA:referrer}\" \"%{DATA:agent}\"" }
         }
       }
       date {
             match => [ "timestamp" , "dd/MMM/YYYY:HH:mm:ss Z" ]
       }
       geoip {
              source => "remote_ip"
              target => "geoip"
              add_tag => [ "nginx-geoip" ]
       }
     }
     ```

   - `output.conf`:
     ```conf
     output {
             elasticsearch {
                 hosts    => "https://localhost:9200"
                 index    => "websrv-%{+YYYY.MM}"
                 user => "elastic"
                 password => "your_elastic_password"
                 cacert => "/etc/logstash/certs/http_ca.crt"
             }
     }
     ```

2. Скопируйте сертификаты:
   ```bash
   cp -R /etc/elasticsearch/certs /etc/logstash
   chown -R root:logstash /etc/logstash/certs
   ```

3. Включите и запустите службу:
   ```bash
   systemctl enable logstash.service
   systemctl start logstash.service
   ```

## Установка Filebeat

### Для Debian/Ubuntu:

```bash
apt install filebeat
```

### Для CentOS/RHEL:

```bash
yum install filebeat
```

### Настройка Filebeat

1. Настройте `/etc/filebeat/filebeat.yml`:
   ```yaml
   filebeat.inputs:
   - type: log
     enabled: true
     paths:
         - /var/log/nginx/*-access.log
     fields:
       type: nginx_access
     fields_under_root: true
     scan_frequency: 5s

   - type: log
     enabled: true
     paths:
         - /var/log/nginx/*-error.log
     fields:
       type: nginx_error
     fields_under_root: true
     scan_frequency: 5s

   output.logstash:
     hosts: ["localhost:5044"]
   ```

2. Включите и запустите службу:
   ```bash
   systemctl enable filebeat
   systemctl start filebeat
   ```

## Проверка работы

1. В Kibana перейдите в раздел "Discover"
2. Создайте новое представление данных (Data View) для индекса `websrv-*`
3. Убедитесь, что логи поступают и отображаются корректно

 