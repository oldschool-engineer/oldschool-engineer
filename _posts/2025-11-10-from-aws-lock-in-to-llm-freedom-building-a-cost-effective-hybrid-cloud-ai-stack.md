---
title: "From AWS Lock-In to LLM Freedom: Building a Cost-Effective Hybrid-Cloud AI Stack"
excerpt: "Self-hosting LiteLLM, Langflow, and Khoj on Kubernetes while using AWS Bedrock for inference."
categories:
  - Infrastructure
tags:
  - kubernetes
  - litellm
  - langflow
  - aws
  - bedrock
  - hybrid-cloud
---

***Self-hosting LiteLLM, Langflow, and Khoj for maximum flexibility***

![](/assets/images/posts/from-aws-lock-in-to-llm-freedom-building-a-cost-effective-hybrid-cloud-ai-stack/img-01.png)

Earlier this year, [I wrote about reducing my AWS costs through a hybrid-cloud approach]({% post_url 2025-03-18-using-hybrid-cloud-to-cost-optimize-ai-workloads %}). The core insight: the majority of my AWS costs came from compute (Lambda) usage, while the AI “heavy lifting” performed by AWS Bedrock constituted only 5% of my costs. By moving compute on-premises, I reduced costs significantly. However, maintaining the on-premises software stack proved more expensive than anticipated.

#### **The Solution That Wasn’t**

Problems with the on-premises solution:

* The Bedrock Proxy API implementation is incomplete and does not support all OpenAI API calls. Implementing all missing APIs is non-trivial.
* Dependencies on AWS Secrets Manager, Key Management Services, and Systems Manager Parameter Store cost $0.32 per day.

Replacing AWS dependencies? Easy — maybe a day of work. Implementing full OpenAI API support? That’s a different story. It would require significant upfront development and constant maintenance every time OpenAI updates their API.

I actually started building this, but quickly realized I was signing up for endless maintenance work. That’s a fool’s errand, so I abandoned the approach.

If you’re curious about my implementation before I archived it, you can check out the repos where I split the front-end API and Bedrock adapter: [here](https://github.com/kuhl-haus/kuhl-haus-bedrock-api) and [here](https://github.com/kuhl-haus/kuhl-haus-bedrock-app)

### Back to the drawing board

#### **Defining the Requirements**

What problem am I trying to solve? I want a **self-hosted** piece of software that presents an OpenAI-compatible API while routing requests to arbitrary LLM providers. This would unlock compatibility between OpenAI-only tools (which are numerous) and any LLM — including self-hosted models and Anthropic’s offerings on AWS Bedrock.

**A Note on Motivation**

I maintain an OpenAI account, so this isn’t about avoiding their service. Rather, it’s about architectural flexibility: the ability to choose the best LLM for each use case without being locked into a single provider.

**Why Not Extend Existing Solutions?**

The Bedrock API Gateway sample handles the Bedrock integration but has two limitations:

* It doesn’t support all OpenAI APIs
* It doesn’t support self-hosted models

I considered two options: extend the project and contribute back via pull request, or find an existing solution that already meets my needs. While I’m capable of implementing the missing features, that doesn’t make it the right choice. The maintenance burden and opportunity cost led me to search for existing open-source alternatives instead.

#### Introducing, LiteLLM

LiteLLM solved everything. I genuinely wish I had known about it a year or two ago — it would have saved me from building custom solutions. Their [Docker and Kubernetes deployment docs](https://docs.litellm.ai/docs/proxy/deploy) got me up and running in minutes, and since it checked all my boxes while working perfectly with my existing Kubernetes and Ansible setup, I stopped searching.

[**LiteLLM**  
*LLM Gateway (OpenAI Proxy) to manage authentication, loadbalancing, and spend tracking across 100+ LLMs. All in the…*www.litellm.ai](https://www.litellm.ai/ "https://www.litellm.ai/")

[**LiteLLM - Getting Started | liteLLM**  
*https://github.com/BerriAI/litellm*docs.litellm.ai](https://docs.litellm.ai/docs/ "https://docs.litellm.ai/docs/")

**What Changed?**

My API keys now live on-premises in the LiteLLM database. That means I no longer need:

* AWS Secrets Manager
* Key Management Services
* Systems Manager Parameter Store

Since I am not implementing IAM Roles Anywhere, my AWS footprint consists solely of an IAM user for generating access keys. I added a CDK stack to my [bedrock-access-gateway-cdk repository](https://github.com/kuhl-haus/bedrock-access-gateway-cdk) to automate this one-time provisioning step.

### CDK Deployment Overview

This CDK stack will deploy an IAM user and group with the permissions to call AWS Bedrock APIs. Instructions for generating the AWS Access and Secret Key can be found [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).

CDK source: [bedrock\_api\_user\_stack.py](https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/cdk/stacks/bedrock_api_user_stack.py)

PowerShell Deployment Script: [deploy-bedrock-api-users-stack.ps1](https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/scripts/deploy-bedrock-api-users-stack.ps1)

```python
.\deploy-bedrock-api-users-stack.ps1 `  
    -AwsAccountId "987654321098" `  
    -AwsRegion "us-west-2" `  
    -UserName "BedrockApiUser" `  
    -GroupName "BedrockApiUsers" `  
    -RemovalPolicy "DESTROY"  
  
# Environment variables may be substituted for command-line parameters  
$env:BEDROCK_API_USER_NAME = "BedrockApiUser"  
$env:BEDROCK_API_USERS_GROUP_NAME = "BedrockApiUsers"  
.\deploy-bedrock-api-users-stack.ps1 `  
    -AwsAccountId "987654321098" `  
    -AwsRegion "us-west-2" `  
    -RemovalPolicy "DESTROY"
```

Bash Deployment Script: [deploy-bedrock-api-users-stack.sh](https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/scripts/deploy-bedrock-api-users-stack.sh)

```python
./scripts/deploy-bedrock-api-users-stack.sh \  
    --aws-account-id 0123456789012   
    --aws-region us-west-2   
    --removal-policy RETAIN  
    --user-name "BedrockApiUser"  
    --group-name "BedrockApiUsers"
```

### LiteLLM Deployment Overview

I deployed my LiteLLM stack to Kubernetes using Ansible. The playbook below has been modified from my production configuration to make it suitable for others to adapt.

#### Prerequisites

* Ansible knowledge required
* Alternative: Use the [LiteLLM Helm chart](https://docs.litellm.ai/docs/proxy/deploy#helm-chart) if unfamiliar with Ansible

#### Important Notes

* **This code is provided as-is** and requires modification for your environment
* **DNS Provider:** This example uses Cloudflare. To use AWS Route 53, replace Cloudflare-specific sections with the Route 53 example below

Deployment Commands:

```python
# deploy to dev  
ansible-playbook -vv -i inventory/litellm.yml deploy.yml \  
    --extra-vars="@group_vars/secrets.yml" \  
    --limit dev-cp-1  
  
# deploy to ppe  
ansible-playbook -vv -i inventory/litellm.yml deploy.yml \  
    --extra-vars="@group_vars/secrets.yml" \  
    --limit ppe-cp-1  
  
# deploy to prod
```

Deployment Playbook:

```python
# deploy.yml  
---  
- hosts: all  
  become: yes  
  become_user: ansible  
  pre_tasks:  
    - name: Create directory for manifests  
      file:  
        path: "{{ manifests_dir }}"  
        state: directory  
        mode: '0755'  
    - name: Create namespace manifest  
      copy:  
        dest: "{{ manifests_dir }}/00-app-namespace.yaml"  
        content: |  
          apiVersion: v1  
          kind: Namespace  
          metadata:  
            name: {{ app_namespace }}  
      
    # Database  
    - name: Create PostgreSQL credentials secret  
      copy:  
        dest: "{{ manifests_dir }}/00-database-credentials-secret.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: Secret  
          metadata:  
            name: {{ app_namespace }}-database-credentials  
            namespace: {{ app_namespace }}  
          stringData:  
            POSTGRES_USER: "{{ postgres_user }}"  
            POSTGRES_PASSWORD: "{{ postgres_password }}"  
            POSTGRES_DB: "{{ postgres_db }}"  
            POSTGRES_HOST: "{{ app_name }}-database.{{ app_namespace }}.svc.cluster.local"  
            POSTGRES_PORT: "5432"  
    - name: Create LiteLLM database StatefulSet manifest  
      copy:  
        dest: "{{ manifests_dir }}/00-database-statefulset.yaml"  
        content: |  
          ---  
          # Headless Service for the StatefulSet  
          apiVersion: v1  
          kind: Service  
          metadata:  
            name: {{ app_name }}-database  
            namespace: {{ app_namespace }}  
          spec:  
            clusterIP: None  
            selector:  
              app: {{ app_name }}-database  
            ports:  
            - port: 5432  
              name: tcp  
          ---  
          apiVersion: apps/v1  
          kind: StatefulSet  
          metadata:  
            name: {{ app_name }}-database  
            namespace: {{ app_namespace }}  
          spec:  
            serviceName: {{ app_name }}-database  
            replicas: 1  
            selector:  
              matchLabels:  
                app: {{ app_name }}-database  
            template:  
              metadata:  
                labels:  
                  app: {{ app_name }}-database  
              spec:  
                containers:  
                  - name: {{ app_name }}-database  
                    image: {{ database_container_image }}  
                    resources:  
                      requests:  
                        cpu: 1000m  
                        memory: 1Gi  
                      limits:  
                        cpu: 2000m  
                        memory: 2Gi  
                    ports:  
                      - containerPort: 5432  
                    env:  
                      - name: POSTGRES_DB  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-database-credentials  
                            key: POSTGRES_DB  
                      - name: POSTGRES_USER  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-database-credentials  
                            key: POSTGRES_USER  
                      - name: POSTGRES_PASSWORD  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-database-credentials  
                            key: POSTGRES_PASSWORD  
                      - name: PGDATA  
                        value: /var/lib/postgresql/data/pgdata  
                    readinessProbe:  
                      exec:  
                        command:  
                          - pg_isready  
                          - -U  
                          - postgres  
                      initialDelaySeconds: 30  
                      periodSeconds: 15  
                      timeoutSeconds: 10  
                      successThreshold: 1  
                      failureThreshold: 10  
                    volumeMounts:  
                      - name: database-data  
                        mountPath: /var/lib/postgresql/data/  
            volumeClaimTemplates:  
            - metadata:  
                name: database-data  
              spec:  
                accessModes: [ "ReadWriteOnce" ]  
                storageClassName: {{ db_storage_class }}  
                resources:  
                  requests:  
                    storage: {{ db_storage_size }}  
    - name: Apply Kubernetes manifests  
      shell: "kubectl apply -f {{ manifests_dir }}/{{ item }}"  
      with_items:  
        - 00-app-namespace.yaml  
        - 00-database-credentials-secret.yaml  
        - 00-database-statefulset.yaml  
  
  tasks:  
    # Part 1: Certificate Management  
    ## Cloudflare  
    - name: Create Cloudflare credentials secret  
      copy:  
        dest: "{{ manifests_dir }}/01-cloudflare-credentials-secret.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: Secret  
          metadata:  
            name: {{ app_namespace }}-cloudflare-credentials  
            namespace: {{ app_namespace }}  
          type: Opaque  
          stringData:  
            dns-api-token: "{{ cloudflare_prod_dns_api_token  }}"  
            global-api-key: "{{ cloudflare_prod_global_api_key }}"  
    - name: Create Cloudflare cert-manager staging issuer  
      copy:  
        dest: "{{ manifests_dir }}/01-cloudflare-staging-issuer.yaml"  
        content: |  
          ---  
          apiVersion: cert-manager.io/v1  
          kind: Issuer  
          metadata:  
            name: {{ cloudflare_acme_test_issuer }}  
            namespace: {{ app_namespace }}  
          spec:  
            acme:  
              server: https://acme-staging-v02.api.letsencrypt.org/directory  
              email: "{{ acme_staging_email }}"  
              privateKeySecretRef:  
                name: {{ cloudflare_acme_test_issuer }}  
              solvers:  
              - selector: {}  
                dns01:  
                  cloudflare:  
                    apiTokenSecretRef:  
                      name: {{ app_namespace }}-cloudflare-credentials  
                      key: dns-api-token  
    - name: Create Cloudflare cert-manager production issuer  
      copy:  
        dest: "{{ manifests_dir }}/01-cloudflare-prod-issuer.yaml"  
        content: |  
          ---  
          apiVersion: cert-manager.io/v1  
          kind: Issuer  
          metadata:  
            name: {{ cloudflare_acme_prod_issuer }}  
            namespace: {{ app_namespace }}  
          spec:  
            acme:  
              server: https://acme-v02.api.letsencrypt.org/directory  
              email: "{{ acme_prod_email }}"  
              privateKeySecretRef:  
                name: {{ cloudflare_acme_prod_issuer }}  
              solvers:  
              - selector: {}  
                dns01:  
                  cloudflare:  
                    apiTokenSecretRef:  
                      name: {{ app_namespace }}-cloudflare-credentials  
                      key: dns-api-token  
  
    # Part 2: LiteLLM Configs  
    - name: Create LiteLLM config  
      copy:  
        dest: "{{ manifests_dir }}/02-litellm-config.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: ConfigMap  
          metadata:  
            name: {{ app_name }}-config  
            namespace: {{ app_namespace }}  
          data:  
            config.yaml: |  
              # https://docs.litellm.ai/docs/proxy/config_management  
              # include:  
              #   - model_config.yaml  
  
              router_settings:  
                debug_level: "{{ log_level }}"  
  
              litellm_settings:  
                telemetry: False  
                drop_params: true  # Drop unsupported params https://docs.litellm.ai/docs/completion/drop_params#openai-proxy-usage  
                request_timeout: 600    # raise Timeout error if call takes longer than 600 seconds. Default value is 6000seconds if not set  
                set_verbose: {{ set_verbose }}  
                json_logs: true         # Get debug logs in json format  
  
              general_settings:  
                master_key: os.environ/LITELLM_MASTER_KEY  
                database_url: os.environ/DATABASE_URL  
    
                # Setup slack alerting - get alerts on LLM exceptions, Budget Alerts, Slow LLM Responses  
                alerting: {{ app_alerting }}  
  
                # Batch write spend updates  
                proxy_batch_write_at: {{ proxy_batch_write_at }}  
  
                # limit the number of database connections to = MAX Number of DB Connections/Number of instances of litellm proxy (Around 10-20 is good number)  
                database_connection_pool_limit: {{ database_connection_pool_limit }}   
                allow_requests_on_db_unavailable: {{ allow_requests_on_db_unavailable }} # Allow requests to still be processed even if the DB is unavailable.  
                background_health_checks: {{ background_health_checks }} # enable background health checks  
                health_check_interval: {{ health_check_interval }} # frequency of background health checks  
              
            model_config.yaml: |  
              # https://docs.litellm.ai/docs/proxy/model_management  
              # litellm_params: https://docs.litellm.ai/docs/completion/input#input-params-1  
              model_list:  
                
                # Anthropic Claude Sonnet 4.5 v1  
                - model_name: us.anthropic.claude-sonnet-4-5-20250929-v1:0  
                  litellm_params:  
                    model: us.anthropic.claude-sonnet-4-5-20250929-v1:0  
                    litellm_credential_name: default_bedrock_credential   
                  model_info:  
                    custom_llm_provider: bedrock   
  
                # Anthropic Claude Opus 4.1 v1  
                - model_name: us.anthropic.claude-opus-4-1-20250805-v1:0  
                  litellm_params:  
                    model: us.anthropic.claude-opus-4-1-20250805-v1:0  
                    litellm_credential_name: default_bedrock_credential    
                  model_info:  
                    custom_llm_provider: bedrock  
                  
                # Anthropic Claude Haiku 4.5 v1  
                - model_name: us.anthropic.claude-haiku-4-5-20251001-v1:0  
                  litellm_params:  
                    model: us.anthropic.claude-haiku-4-5-20251001-v1:0  
                    litellm_credential_name: default_bedrock_credential    
                  model_info:  
                    custom_llm_provider: bedrock  
  
                # Stability Stable Image Ultra v1.1  
                - model_name: stability.stable-image-ultra-v1:1  
                  litellm_params:  
                    model: stability.stable-image-ultra-v1:1  
                    litellm_credential_name: default_bedrock_credential    
                  model_info:  
                    custom_llm_provider: bedrock  
                    mode: image_generation  
               
                # Stability Stable Diffusion 3.5 Large v1.0  
                - model_name: stability.sd3-5-large-v1:0  
                  litellm_params:  
                    model: stability.sd3-5-large-v1:0  
                    litellm_credential_name: default_bedrock_credential    
                  model_info:  
                    custom_llm_provider: bedrock  
                    mode: image_generation  
                  
              # https://docs.litellm.ai/docs/proxy/configs#centralized-credential-management  
              credential_list:  
                - credential_name: default_bedrock_credential  
                  credential_values:  
                    aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID  
                    aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY  
                    aws_region_name: os.environ/AWS_REGION_NAME  
                  credential_info:  
                    description: "AWS Bedrock {{ app_env }} credentials"  
                    custom_llm_provider: bedrock  
  
    - name: Create LiteLLM secrets  
      copy:  
        dest: "{{ manifests_dir }}/02-litellm-secrets.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: Secret  
          metadata:  
            name: {{ app_name }}-secrets  
            namespace: {{ app_namespace }}  
          stringData:  
            AWS_REGION_NAME: "{{ aws_region }}"  
            AWS_REGION: "{{ aws_region }}"  
            AWS_ACCESS_KEY_ID: "{{ bedrock_credentials_access_key }}"  
            AWS_SECRET_ACCESS_KEY: "{{ bedrock_credentials_secret_key }}"  
              
            # Your master key for the proxy server. Can use this to send /chat/completion requests etc  
            LITELLM_MASTER_KEY: "{{ litellm_master_key }}"  
            # Can NOT CHANGE THIS ONCE SET - It is used to encrypt/decrypt credentials stored in DB. If value of 'LITELLM_SALT_KEY' changes your models cannot be retrieved from DB  
            LITELLM_SALT_KEY: "{{ litellm_db_salt_key }}"   
            DATABASE_URL: "postgresql://{{ postgres_user }}:{{ postgres_password }}@{{ app_name }}-database.{{ app_namespace }}.svc.cluster.local:5432/{{ postgres_db }}"  
            UI_USERNAME: "{{ litellm_ui_username }}"  
            UI_PASSWORD: "{{ litellm_ui_password }}"  
  
            SLACK_WEBHOOK_URL: "{{ litellm_slack_webhook_url }}"  
            SMTP_USERNAME: "{{ aws_ses_smtp_username }}"  
            SMTP_PASSWORD: "{{ aws_ses_smtp_password }}"  
              
      
    # Part 3: LiteLLM Proxy  
    - name: Create LiteLLM Deployment  
      copy:  
        dest: "{{ manifests_dir }}/03-litellm-deployment.yaml"  
        content: |  
          ---  
          apiVersion: apps/v1  
          kind: Deployment  
          metadata:  
            name: {{ app_name }}  
            namespace: {{ app_namespace }}  
          spec:  
            replicas: {{ desired_replicas }}  
            selector:  
              matchLabels:  
                app: {{ app_name }}  
            strategy:  
              type: RollingUpdate  
              rollingUpdate:  
                maxSurge: 1  
                maxUnavailable: 0  
            template:  
              metadata:  
                labels:  
                  app: {{ app_name }}  
              spec:  
                containers:  
                  - name: {{ app_name }}  
                    image: {{ app_container_image }}  
                    ports:  
                      - containerPort: {{ app_container_port }}  
                    volumeMounts:  
                    - name: config-volume  
                      mountPath: /app/config.yaml  
                      subPath: config.yaml  
                    - name: config-volume  
                      mountPath: /app/model_config.yaml  
                      subPath: model_config.yaml  
                    envFrom:  
                    - secretRef:  
                        name: {{ app_name }}-secrets  
                    env:  
                      - name: CONFIG_FILE_PATH  
                        value: /app/config.yaml  
                      - name: DISABLE_ADMIN_UI  
                        value: "False"  
                      - name: STORE_MODEL_IN_DB  
                        value: "True"   
                      - name: USE_PRISMA_MIGRATE  
                        value: "True"  
                        
                      - name: SMTP_SENDER_EMAIL  
                        value: {{ smtp_sender_email }}  
                      - name: SMTP_HOST  
                        value: {{ smtp_host }}  
                      - name: SMTP_PORT  
                        value: "465"  
                      - name: SMTP_TLS  
                        value: "True"  
                      - name: SMTP_USERNAME  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-secrets  
                            key: SMTP_USERNAME   
                      - name: SMTP_PASSWORD  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-secrets  
                            key: SMTP_PASSWORD   
                      - name: LITELLM_LOG  
                        value: {{ log_level }}  
                        
                      - name: LITELLM_MASTER_KEY  
                        valueFrom:  
                          secretKeyRef:  
                            name: {{ app_name }}-secrets  
                            key: LITELLM_MASTER_KEY   
                      - name: POD_NAME  
                        valueFrom:  
                          fieldRef:  
                            fieldPath: metadata.name  
                    readinessProbe:  
                      httpGet:  
                        path: /health/readiness  
                        port: {{ app_container_port }}  
                      initialDelaySeconds: 30  
                      periodSeconds: 15  
                      timeoutSeconds: 10  
                      successThreshold: 1  
                      failureThreshold: 10  
                    livenessProbe:  
                      httpGet:  
                        path: /health/liveness  
                        port: {{ app_container_port }}  
                      initialDelaySeconds: 30  
                      periodSeconds: 15  
                      timeoutSeconds: 10  
                      successThreshold: 1  
                      failureThreshold: 10  
                    resources:  
                      requests:  
                        cpu: 2000m  
                        memory: 2Gi  
                      limits:  
                        cpu: 4000m  
                        memory: 8Gi  
                volumes:  
                  - name: config-volume  
                    configMap:  
                      name: {{ app_name }}-config  
    - name: Create LiteLLM Service  
      copy:  
        dest: "{{ manifests_dir }}/03-litellm-service.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: Service  
          metadata:  
            name: {{ app_name }}  
            namespace: {{ app_namespace }}  
          spec:  
            type: ClusterIP  
            ports:  
              - port: {{ app_container_port }}  
                targetPort: {{ app_container_port }}  
                protocol: TCP  
            selector:  
              app: {{ app_name }}  
    - name: Create LiteLLM Ingress  
      copy:  
        dest: "{{ manifests_dir }}/03-litellm-ingress.yaml"  
        content: |  
          ---  
          apiVersion: networking.k8s.io/v1  
          kind: Ingress  
          metadata:  
            name: {{ app_name }}  
            namespace: {{ app_namespace }}  
            annotations:  
              cert-manager.io/issuer: {{ app_cert_issuer }}  
          spec:  
            ingressClassName: {{ app_ingress_class }}  
            tls:  
              - hosts:  
  
                {% for host in app_hosts %}  
                - {{ host }}  
                {% endfor %}  
  
                secretName: {{ app_name }}-tls  
            rules:  
  
            {% for host in app_hosts %}  
          - host: {{ host }}  
              http:  
                paths:  
                - path: /  
                  pathType: Prefix  
                  backend:  
                    service:  
                      name: {{ app_name }}  
                      port:  
                        number: {{ app_container_port }}  
            {% endfor %}  
  
    # Part 7: Apply Kubernetes manifests  
    - name: Apply Kubernetes manifests  
      shell: "kubectl apply -f {{ manifests_dir }}/{{ item }}"  
      with_items:  
        # Cloudflare ACME  
        - 01-cloudflare-credentials-secret.yaml  
        - 01-cloudflare-staging-issuer.yaml  
        - 01-cloudflare-prod-issuer.yaml  
  
        # LiteLLM Configs  
        - 02-litellm-config.yaml  
        - 02-litellm-secrets.yaml  
          
        # LiteLLM Proxy  
        - 03-litellm-deployment.yaml  
        - 03-litellm-service.yaml  
        - 03-litellm-ingress.yaml
```

**AWS Route 53 ACME**

If desired, you can replace Cloudflare ACME with Route53.

```python
- hosts: all  
  become: yes  
  become_user: ansible    
  tasks:  
    ## AWS ACME credentials  
    - name: Create ACME AWS credentials secret  
      copy:  
        dest: "{{ manifests_dir }}/02-aws-credentials-secret.yaml"  
        content: |  
          ---  
          apiVersion: v1  
          kind: Secret  
          metadata:  
            name: {{ acme_route53_credentials_secret_name }}  
            namespace: {{ app_namespace }}  
          stringData:  
            access-key-id: "{{ acme_route53_access_key_id }}"  
            secret-access-key: "{{ acme_route53_secret_access_key }}"  
    - name: Create cert-manager test issuer  
      copy:  
        dest: "{{ manifests_dir }}/02-cert-manager-test-issuer.yaml"  
        content: |  
          ---  
          apiVersion: cert-manager.io/v1  
          kind: Issuer  
          metadata:  
            name: {{ acme_aws_test_issuer }}  
            namespace: {{ app_namespace }}  
          spec:  
            acme:  
              server: https://acme-staging-v02.api.letsencrypt.org/directory  
              email: "{{ acme_staging_email }}"  
              privateKeySecretRef:  
                name: {{ acme_aws_test_issuer }}  
              solvers:  
              - selector: {}  
                dns01:  
                  route53:  
                    region: {{ acme_aws_region }}  
                    accessKeyIDSecretRef:  
                      name: {{ acme_route53_credentials_secret_name }}  
                      key: access-key-id  
                    secretAccessKeySecretRef:  
                      name: {{ acme_route53_credentials_secret_name }}  
                      key: secret-access-key  
    - name: Create cert-manager production issuer  
      copy:  
        dest: "{{ manifests_dir }}/02-cert-manager-prod-issuer.yaml"  
        content: |  
          ---  
          apiVersion: cert-manager.io/v1  
          kind: Issuer  
          metadata:  
            name: {{ acme_aws_prod_issuer }}  
            namespace: {{ app_namespace }}  
          spec:  
            acme:  
              server: https://acme-v02.api.letsencrypt.org/directory  
              email: "{{ acme_prod_email }}"  
              privateKeySecretRef:  
                name: {{ acme_aws_prod_issuer }}  
              solvers:  
              - selector: {}  
                dns01:  
                  route53:  
                    region: {{ acme_aws_region }}  
                    accessKeyIDSecretRef:  
                      name: {{ acme_route53_credentials_secret_name }}  
                      key: access-key-id  
                    secretAccessKeySecretRef:  
                      name: {{ acme_route53_credentials_secret_name }}  
                      key: secret-access-key  
- name: Apply Kubernetes manifests  
      shell: "kubectl apply -f {{ manifests_dir }}/{{ item }}"  
      with_items:  
        # AWS Route 53 ACME  
        - 02-aws-credentials-secret.yaml  
        - 02-cert-manager-test-issuer.yaml  
        - 02-cert-manager-prod-issuer.yaml
```

Secrets

```python
#The following variables need to be defined in an Ansible Vault secrets file  
  
# All Environments  
litellm_ui_admin  
litellm_ui_password  
postgres_user   
postgres_db  
  
# Cloudflare ACME  
cloudflare_prod_dns_api_token  
cloudflare_prod_global_api_key   
  
# AWS Route 53 ACME  
acme_route53_access_key_id  
acme_route53_secret_access_key  
  
# Slack notifications  
litellm_slack_webhook_url  
  
# Dev Environment  
bedrock_test_aws_access_key  
bedrock_test_aws_secret_key  
litellm_dev_master_key  
litellm_dev_postgres_password  
litellm_dev_replication_password  
  
# Preproduction Environment  
bedrock_gamma_aws_access_key  
bedrock_gamma_aws_secret_key  
litellm_ppe_master_key  
litellm_ppe_postgres_password  
litellm_ppe_replication_password  
  
# Production Environment  
bedrock_prod_aws_access_key  
bedrock_prod_aws_secret_key  
litellm_prod_master_key  
litellm_prod_postgres_password  
litellm_prod_replication_password
```

Inventory

```python
# inventory/litellm.yml  
  
all:  
  vars:  
    ansible_user: ansible  
    manifests_dir: /home/ansible/litellm  
    app_namespace: litellm  
    app_name: litellm  
    app_ingress_class: nginx  
    app_container_port: 4000  # LiteLLM default port  
    app_storage_class: csi-rbd-sc  
    app_container_image: ghcr.io/berriai/litellm:v1.79.1-stable  
    aws_region: us-west-2  
    default_model: us.anthropic.claude-sonnet-4-5-20250929-v1:0  
    acme_staging_email: "YOUR_EMAIL@YOUR_DOMAIN"  
    acme_prod_email: "YOUR_EMAIL@YOUR_DOMAIN"  
    cloudflare_acme_prod_issuer: acme-cloudflare  
    cloudflare_acme_test_issuer: test-cloudflare  
    database_container_image: docker.io/pgvector/pgvector:pg15  
    db_storage_size: 10Gi  
    db_storage_class: csi-rbd-sc  
    postgres_user: litellm  
    postgres_db: litellm  
    litellm_ui_username: "{{ litellm_ui_admin }}"  
    litellm_ui_password: "{{ litellm_ui_password }}"  
    allow_requests_on_db_unavailable: "True"  
    health_check_interval: 300  
    database_connection_pool_limit: 10  
    proxy_batch_write_at: 60  
    smtp_host: email-smtp.us-west-2.amazonaws.com  
    smtp_sender_email: "YOUR_EMAIL@YOUR_DOMAIN"  
  
dev:  
  hosts:  
    dev-cp-1:  
      ansible_host: REPLACEME  
  vars:  
    app_cert_issuer: "{{ cloudflare_acme_prod_issuer }}"  
    app_hosts:  
      - litellm.dev.example.com  
    app_env: dev  
    desired_replicas: 1  
    log_level: DEBUG  
    set_verbose: "True"  
    background_health_checks: "False"  
    app_alerting: ["slack"]  
    bedrock_credentials_access_key: "{{ bedrock_test_aws_access_key }}"  
    bedrock_credentials_secret_key: "{{ bedrock_test_aws_secret_key }}"  
    litellm_master_key: "{{ litellm_dev_master_key }}"  
    postgres_password: "{{ litellm_dev_postgres_password }}"  
    replication_password: "{{ litellm_dev_replication_password }}"  
  
ppe:  
  hosts:  
    ppe-cp-1:  
      ansible_host: REPLACEME  
  vars:  
    app_cert_issuer: "{{ cloudflare_acme_prod_issuer }}"  
    app_hosts:  
      - litellm.ppe.example.com  
    app_env: ppe  
    desired_replicas: 1  
    log_level: DEBUG  
    set_verbose: "True"  
    background_health_checks: "False"  
    app_alerting: ["slack"]  
    bedrock_credentials_access_key: "{{ bedrock_gamma_aws_access_key }}"  
    bedrock_credentials_secret_key: "{{ bedrock_gamma_aws_secret_key }}"  
    litellm_master_key: "{{ litellm_ppe_master_key }}"  
    postgres_password: "{{ litellm_ppe_postgres_password }}"  
    replication_password: "{{ litellm_ppe_replication_password }}"  
  
prod:  
  hosts:  
    prod-cp-1:  
      ansible_host: REPLACEME  
  vars:  
    app_cert_issuer: "{{ cloudflare_acme_prod_issuer }}"  
    app_hosts:  
      - litellm.example.com  
    app_env: prod  
    desired_replicas: 3  
    log_level: INFO  
    set_verbose: "False"  
    background_health_checks: "False"  
    app_alerting: ["slack", "email"]  
    bedrock_credentials_access_key: "{{ bedrock_prod_aws_access_key }}"  
    bedrock_credentials_secret_key: "{{ bedrock_prod_aws_secret_key }}"  
    litellm_master_key: "{{ litellm_prod_master_key }}"  
    postgres_password: "{{ litellm_prod_postgres_password }}"  
    replication_password: "{{ litellm_prod_replication_password }}"
```

### But wait, there’s more!

LangFlow — OMG, this is exactly what I needed! This is definitely worth checking out if you’re into building Agentic workflow. The easiest way to get started (in my opinion) is with [Langflow for Desktop](https://www.langflow.org/desktop).

[**Langflow | Low-code AI builder for agentic and RAG applications**  
*Langflow is a low-code AI builder for agentic and retrieval-augmented generation (RAG) apps. Code in Python and use any…*www.langflow.org](https://www.langflow.org/ "https://www.langflow.org/")

[**What is Langflow? | Langflow Documentation**  
*Langflow is an open-source, Python-based, customizable framework for building AI applications.*docs.langflow.org](https://docs.langflow.org/ "https://docs.langflow.org/")

Deploying Langflow is significantly more involved, however, because my flows depend on additional services: a vector database, external chat memory, and similar infrastructure components. I deploy everything as containers via Kubernetes, managing the deployment through a GitHub repository — no custom Langflow code or components, just a collection of Ansible manifests and bash scripts orchestrated by a GoCD pipeline-as-code setup. The deployment code isn’t useful to share since it’s specific to my infrastructure configuration.

### Self-Hosted Chat Bot

Earlier this year, I made a post about [my asinine conversations with “fake Spock” on my self-hosted Mattermost server]({% post_url 2025-03-10-live-long-and-prompt-tales-from-the-ai-enterprise %}). While the copilot AI plug-in is cool, there’s a prompt embedded in its logic that is a challenge to overcome. Rather than fight with a chatbot designed for Mattermost, I found an open-source, self-hostable service for a personal chat bot. Now I have two personal chatbots! Perfect! 2 > 0 > 1 (Amazon employees will recognize that mathematically inaccurate expression as “**Two is better than none, and none is better than one”.**)

Following the same pattern as LiteLLM, Khoj’s documentation made self-hosting remarkably easy. Khoj functions as an AI-powered personal assistant that indexes and searches across notes, documents, and files.

The killer feature for my workflow is its native [Obsidian integration](https://docs.khoj.dev/clients/obsidian). Since Obsidian is my primary knowledge management tool, having AI-assisted search and contextual chat built directly into my note-taking environment significantly enhances productivity. I can now query my entire knowledge base conversationally and surface relevant information without leaving my editor.

[**Khoj AI**  
*Your open, personal AI. Get answers from your docs or the web. Build custom agents. Schedule automations. Chat in your…*khoj.dev](https://khoj.dev/ "https://khoj.dev/")

[**Overview | Khoj AI**  
*Your Second Brain*docs.khoj.dev](https://docs.khoj.dev/ "https://docs.khoj.dev/")

### Conclusion

With LiteLLM deployed, I have two options: point my tools directly at providers like OpenAI, Anthropic, or AWS Bedrock, or route everything through LiteLLM for maximum flexibility. I chose the latter, connecting Mattermost, Khoj, and Langflow to my LiteLLM instance. This approach provides centralized AI spending tracking across all applications, with daily reports delivered automatically via Mattermost. The result? A simple, flexible, and cost-effective architecture that gives me provider independence without sacrificing functionality.
