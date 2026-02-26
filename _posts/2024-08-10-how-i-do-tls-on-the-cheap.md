---
title: "How I do TLS on the cheap"
excerpt: "Free TLS certificates with automated renewal using Certbot, Route 53, and GoCD."
categories:
  - Infrastructure
tags:
  - tls
  - certbot
  - aws
  - route53
  - automation
---

TLS certificates can get expensive. However, I can obtain as many TLS certificates as I want, for free, simply by automating the process. The only catch — the certificates expire in 90 days. I can live with that.

![](/assets/images/posts/how-i-do-tls-on-the-cheap/img-01.png)

*Photo by AltumCode on Unsplash*

***Caveat****: This solution is for on-premises hosting. If you’re running in AWS, use AWS Certificate Manager. It costs the same but it is easier to implement.*

### Ingredients

1. [Certbot Route 53 plugin](https://certbot-dns-route53.readthedocs.io/en/stable/)
2. [Route53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html) — cheap domain names
3. [GoCD](https://docs.gocd.org/current/)
4. Bash

My approach depends on: AWS Route53 to host DNS; the Route 53 certbot plugin to handle the ACME DNS challenge; and GoCD to orchestrate the automation. Add a little dash of bash and… voilà! Free certs!

Let’s examine each of the items, one by one.

### Certbot Route 53 Plugin

The [default instructions for using certbot](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal&tab=standard) requires an already running webserver, exposed to the Internet, on port 80. I have services running inside my firewall that I have no intention of exposing to the Internet so that’s a non-starter for me. However, the [wildcard instructions](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal&tab=wildcard) only requires DNS. That, I can do. Awesome! I’m a huge fan of [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) for this reason.

*Refer to the* [*Challenge Types*](https://letsencrypt.org/docs/challenge-types/) *page at letsencrypt.org for more information.*

I chose to use the [Route 53 plugin](https://certbot-dns-route53.readthedocs.io/) because that is where I host my external DNS. Other DNS providers are supported so while this solution is specific for Route 53, I’m sure it would be trivial to adapt to other providers.

*Refer to the* [*DNS Plugins*](https://eff-certbot.readthedocs.io/en/latest/using.html#dns-plugins) *page at eff-certbot.readthedocs.io for more information.*

The benefits and constraints with the Route53 (or any DNS) plugin:

Benefits:

* Your web server/host does not need to be exposed to the Internet.
* You can request wildcard certificates.
* You can request certificates with multiple domain names (subject alternate names).
* Simpler to automate across multiple web servers.

Constraints:

* Your DNS provider must offer an API.
* Your DNS provider’s propagation times cannot suck.
* Keeping API credentials on your web server is risky.

I dealt with the first two constraints by using Route 53. The third one… that’s where GoCD comes in. More on that in a bit. First, let’s address the elephant in the room. AWS isn’t free and neither is DNS registration. How much is this going to cost?

### Route53 — Cheap Domain Names

Most DNS domains cost less than $100/year to register but for my purposes, I’m looking for as cheap as possible. According to the [Route 53 Domain Registration Pricing Sheet](https://d32ze2gidvkk54.cloudfront.net/Amazon_Route_53_Domain_Registration_Pricing_20140731.pdf), the following domains cost less than $10/year:

* `.be`: $9
* `.casa`: $9
* `.click`: $3
* `.co.uk`: $9
* `.de`: $9
* `.link`: $5
* `.me.uk`: $8
* `.org.uk`: $9
* `.uk`: $9

For doing things on the cheap, `.click` and `.link` at $3 and $5, respectively, is where it’s at. Now how about that Route 53 hosted zone?

Route 53 Authoritative DNS charges for storage (i.e., the zone and its records) and queries. According to the [Route 53 pricing page](https://aws.amazon.com/route53/pricing/), it costs $0.50 per hosted zone for the first 25 zones and $0.40 per million queries for the first 1 billion queries.

> The following query prices are prorated; for example, a public hosted zone with 100,000 standard queries per month would be charged $0.04, and a public hosted zone with 100,000 latency-based routing queries per month would be charged $0.06.

OK, so it is a good assumption that will be less than a $1 a month, for me, so I’ll just go with $12/year for DNS hosting.

Bottom line cost:

* $15/year for `.click`
* $18/year for `.link`

After including tax, that’s less $20/year for either option. To me, that’s pretty cheap considering that the price is not affected by the number of certificates requested/issued.

### Automation via GoCD

I use GoCD, an open-source Continuous Integration and Continuous Delivery (CI/CD) system, combined with GitHub to orchestrate the majority of my automation tasks. GoCD’s Pipeline As Code (PAC) feature and custom Bash scripts are the two main components that power my implementation.

The PAC approach allows me to define my pipelines, stages, and jobs in a declarative YAML configuration. This makes it easy to version control and replicate my CI/CD workflows across different projects and environments. The YAML configuration also supports the use of GoCD’s encryption capabilities, which I leverage to securely store sensitive information like API credentials.

Complementing the PAC approach, I also utilize custom Bash scripts to handle the more granular aspects of my automation. These scripts are responsible for tasks such as obtaining and renewing TLS certificates, managing application deployments, and running smoke tests. By separating the high-level pipeline orchestration from the low-level script execution, I’m able to maintain a modular and maintainable automation system.

The combination of GoCD’s PAC and my Bash scripts gives me a powerful and flexible platform to automate a wide range of tasks, from infrastructure provisioning to application deployments, all while keeping my sensitive data secure and my workflows version-controlled.

#### Handling API Credentials

The GoCD encryption API allows users with administrative privileges to obtain the ciphertext (encrypted text) corresponding to any plaintext value. You can then use this ciphertext in other APIs that allow you to configure pipelines and templates.

For example, to encrypt a plaintext value, you use the following command:

```python
$ curl 'https://your.gocd.sever/go/api/admin/encrypt' \  
-u 'username:password' \  
-H 'Accept: application/vnd.go.cd.v1+json' \  
-H 'Content-Type: application/json' \  
-X POST -d '{  
  "value": "badger"  
}'
```

Which would return JSON that is structured like this:

```python
HTTP/1.1 200 OK  
Content-Type: application/vnd.go.cd.v1+json; charset=utf-8  
{  
  "_links": {  
    "self": {  
      "href": "http://your.gocd.server/go/api/admin/encrypt"  
    },  
    "doc": {  
      "href": "https://api.gocd.org/#encryption"  
    }  
  },  
  "encrypted_value": "AES:AgaHG9eA+Hi3KMTWh+cxsQ==:w3jGeSN6sLKJDsd85SdqNBTsTWaZpv23W7dXoELsY/TLkZZSCLRqk278EI96vUwz/zViWq1p="  
}
```

Use the value of encrypted\_value in your YAML configuration.

#### Pipeline As Code (PAC)

I utilize the YAML config plugin for my implementation. While it may not be the most expressive language, it gets the job done, and it is free and open-source. The key is using GoCD’s encryption to securely store the API credentials. There are other options available, such as using Secrets Management plugins, but this approach is simple and relatively secure, especially when used with private repositories.

In the example configuration, I’m using the encryption for GitHub (encrypted\_password) and the AWS API credentials (secure\_variables). These are obviously not the real values, but you can follow the example to generate your own.

```python
format_version: 10  
common:  
  # Attributes  
  certbot_group: &certbot_group "Lets_Encrypt"  
  certbot_label_template: &certbot_label_template ${COUNT}  
  certbot_lock_behavior: &certbot_lock_behavior unlockWhenFinished  
    
  # Materials  
  certbot_repo: &certbot_repo  
    git: https://github.com/your-username/certbot  
    username: your-username  
    shallow_clone: true  
    auto_update: false  
    branch: main  
    encrypted_password: AES:Aga..Rl==:ikd..p  
    destination: certbot    
  your_app_repo: &your_app_repo  
    git: https://github.com/your-username/your_app  
    username: your-username  
    shallow_clone: true  
    auto_update: false  
    branch: main  
    encrypted_password: AES:Aga...sQ==:w3j...p  
    destination: your_app  
  
  # Certbot Stages  
  update_cert: &update_cert  
    fetch_materials: true  
    keep_artifacts: false  
    clean_workspace: true  
    environment_variables:  
      CERTBOT_EMAIL: your-email@domain.name  
    approval:  
      type: success  
      allow_only_on_success: true  
    jobs:  
      run-script:  
        timeout: 0  
        run_instances: all  
        tasks:  
        - exec:  
            command:  sudo  
            arguments:  
            - -EHn  
            - ./certbot/scripts/update-cert.sh  
            run_if: passed  
  
  # Smoke Test Stages - Defines the app-specific smoke tests to run.  
  smoke_test_your_app: &smoke_test_your_app  
    fetch_materials: false  
    keep_artifacts: false  
    clean_workspace: false  
    approval:  
      type: success  
      allow_only_on_success: true  
    jobs:  
      run-script:  
        timeout: 0  
        run_instances: all  
        tasks:  
        - exec:  
            command: ./your_app/scripts/smoke-test.sh  
            run_if: passed  
# AWS API Credentials injected via environment variables at script run-time  
environments:  
  your-app-env:  
    pipelines:  
      - your_app_update_certs  
    environment_variables:  
      AWS_REGION: us-west-2  
      GO_BASE_DIR: "/var/lib/go-agent"  
    secure_variables:  
      AWS_ACCESS_KEY_ID: AES:oO..O0Q==:lw..g=  
      AWS_SECRET_ACCESS_KEY: AES:LC..BaQ==:k0/..Ao  
pipelines:  
  # Your App  
  your_app_update_certs:  
    group: *certbot_group  
    label_template: *certbot_label_template  
    lock_behavior: *certbot_lock_behavior  
    display_order: -1  
    environment_variables:  
      INSTALL_DIR: "/opt/containers/your_app"    
      TLS_DOMAIN: "app.domain.name,alt.domain.name"  
      SIDE_CAR_CONTAINER: "your_side_car_reverse_proxy_container_name"  
    materials:  
      certbot_repo: *certbot_repo  
      your_app_repo: *your_app_repo  
    stages:  
    - update_cert: *update_cert  
    - smoke_test: *smoke_test_your_app
```

For more details, refer to the following resources:

* **Encrypting a plain text value**: <https://api.gocd.org/current/?shell#encrypt-a-plain-text-value>
* **YAML Config Plugin**: [tomzo/gocd-yaml-config-plugin](https://github.com/tomzo/gocd-yaml-config-plugin)
* **Configuration Reference**: <https://docs.gocd.org/current/configuration/configuration_reference.html>

### A Dash of Bash

To complement the Pipeline As Code (PAC) orchestration, I leverage custom Bash scripts for the granular automation tasks.

The key is using PAC-injected environment variables to make the certificate scripts portable across hosts and sites. This allows me to employ the same scripts consistently, without duplicating or maintaining separate versions.

After the certificate update, I run application-specific smoke tests as part of the pipeline. This ensures the updated certificates are properly configured and the app is functioning as expected after deploying the changes.

By bridging the high-level pipeline and low-level system tasks with Bash, I automate the end-to-end certificate lifecycle — from initial provisioning to periodic renewal — while verifying application health. This approach allows me to update certificates independently from application code while using the same smoke test scripts that I use when I deploy the application.

```python
#!/bin/bash  
  
set -exu  
  
if [ -z $INSTALL_DIR ]; then  
  echo "INSTALL_DIR environment variable is not set."  
  exit 1  
fi  
  
if [ -z $AWS_ACCESS_KEY_ID ]; then  
  echo "AWS_ACCESS_KEY_ID environment variable is not set."  
  exit 1  
fi  
  
if [ -z $AWS_SECRET_ACCESS_KEY ]; then  
  echo "AWS_SECRET_ACCESS_KEY environment variable is not set."  
  exit 1  
fi  
  
if [ -z $TLS_DOMAIN ]; then  
  echo "TLS_DOMAIN environment variable is not set."  
  exit 1  
fi  
  
if [ -z $CERTBOT_EMAIL ]; then  
  echo "CERTBOT_EMAIL environment variable is not set."  
  exit 1  
fi  
  
if [ -z $SIDE_CAR_CONTAINER ]; then  
  echo "SIDE_CAR_CONTAINER environment variable is not set."  
  exit 1  
fi  
  
  
if [ -d "${INSTALL_DIR}" ]; then  
    cd "${INSTALL_DIR}" || exit 1  
else  
    echo "${INSTALL_DIR} doesn't exist."  
    exit 1  
fi  
  
  
export CERTBOT_ROOT_DIR="${INSTALL_DIR}/volumes/certbot"  
export CERTBOT_CONFIG_DIR="${CERTBOT_ROOT_DIR}/conf"  
export CERTBOT_WORK_DIR="${CERTBOT_ROOT_DIR}/var"  
export CERTBOT_LOGS_DIR="${CERTBOT_ROOT_DIR}/log"  
if [ -d "${CERTBOT_CONFIG_DIR}" ]; then  
  sudo mkdir -pv "${CERTBOT_CONFIG_DIR}"  
fi  
if [ -d "${CERTBOT_WORK_DIR}" ]; then  
  sudo mkdir -pv "${CERTBOT_WORK_DIR}"  
fi  
if [ -d "${CERTBOT_LOGS_DIR}" ]; then  
  sudo mkdir -pv "${CERTBOT_LOGS_DIR}"  
fi  
  
sudo chown -R 0:0 "${CERTBOT_ROOT_DIR}"  
  
if ! which certbot 1>/dev/null; then  
  echo "Certbot is not installed. Installing now..." >&2  
  sudo snap install --classic certbot && \  
  sudo ln -s /snap/bin/certbot /usr/bin/certbot && \  
  sudo snap set certbot trust-plugin-with-root=ok && \  
  sudo snap install certbot-dns-route53  
fi  
  
# Create certificates  
echo "Calling certbot to create certificates"  
sudo -E certbot certonly -n \  
--dns-route53 \  
--email "${CERTBOT_EMAIL}" \  
--rsa-key-size 4096 \  
--agree-tos \  
--config-dir "${CERTBOT_CONFIG_DIR}" \  
--work-dir "${CERTBOT_WORK_DIR}" \  
--logs-dir "${CERTBOT_LOGS_DIR}" \  
-v \  
-d "${TLS_DOMAIN}" || exit 1  
echo "DONE"  
  
export NGINX_CERTBOT_CONFIG_DIR="${INSTALL_DIR}/volumes/nginx/certbot"  
if [ -d "${NGINX_CERTBOT_CONFIG_DIR}" ]; then  
  echo "Creating directory: ${NGINX_CERTBOT_CONFIG_DIR}"  
  sudo mkdir -pv "${NGINX_CERTBOT_CONFIG_DIR}"  
fi  
  
echo "Copying certbot certs to nginx config"  
sudo cp -af "${CERTBOT_CONFIG_DIR}/." "${NGINX_CERTBOT_CONFIG_DIR}"  
sudo chown -R 0:0 "${NGINX_CERTBOT_CONFIG_DIR}"  
echo "DONE"  
  
echo "Restarting ${SIDE_CAR_CONTAINER} to bind new certificate."  
docker container restart "${SIDE_CAR_CONTAINER}" || exit 1  
echo "DONE"  
  
echo "EOF"
```

### Final Thoughts

I run almost everything in containers, which provides process-level isolation between my web server and the processes running on the host. This keeps the API credentials out of the web server’s environment, though it doesn’t protect against a container breakout scenario where the container is compromised — a different problem to address.

By leveraging the Certbot Route 53 plugin, AWS Route 53 for cheap domain registration and DNS hosting, and the GoCD automation platform, I’m able to automate the entire TLS certificate lifecycle — from initial provisioning to periodic renewal.

The key aspects of my solution include:

1. Leveraging the Certbot Route 53 plugin: This allows me to handle the ACME DNS challenge, keeping my web servers safely behind a firewall without direct internet exposure.
2. Selecting inexpensive domains from Route 53: By choosing top-level domains like .click and .link, I’m able to minimize the annual costs for domain registration, with each costing less than $20 per year.
3. Implementing a GoCD pipeline using Pipeline as Code (PAC): This allows me to orchestrate the certificate management tasks in a version-controlled and secure manner, leveraging GoCD’s encryption capabilities to store sensitive API credentials.
4. Complementing the GoCD pipeline with custom Bash scripts: I use these scripts to handle the granular certificate provisioning and renewal tasks, as well as running application-specific smoke tests to validate the TLS configuration after updates.

By integrating the certificate management with my application deployment workflows, I ensure a reliable and secure TLS implementation for my on-premises infrastructure. This comprehensive solution allows me to obtain and manage TLS certificates in a fully automated and cost-effective manner, without the need to expose my web servers to the public internet.
