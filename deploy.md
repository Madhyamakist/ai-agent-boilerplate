# CI/CD using Github Actions
Steps to get this repo ready for CI/CD

## Tools
- GCP – For cloud deployment
- Github - For automation pipeline

## Features
- Auto-deploy when pushed to the repo
- Need to setup only once
---
## Setting up GCP for Deployment
### Steps

   - Create a new project
   - Enable compute engine API
   - Create a VM instance for your project
   - Set up external IP for VM (If not using load balancer)
   - Create a service account for github with roles as compute admin, service account user and compute instance admin (v1)
   - Save service account key in Json format
   - Install Gcloud CLI (it will allow you to run gcloud commands in your local machine)
   - Open your local terminal and ssh into your VM instance using gcloud command (it will open VM's terminal)
   - In VM's terminal, download required dependencies and packages (here we need to install python and Postgresql)
   - Create a directory and clone the repo
   - (Temp) Save API keys and Password in root user's .bashrc file 
---
## Setting up Github for Deployment

### Steps
   - Go to Environments in your repo's setting and create a new environment
   - Save the information like service account key, VM external IP, project Id etc. in Environment secrets
   - Mention the branch name, which you want to test in deploy.yml
---
## Final Deployment

Push the changes in your selected repo, and deployment will be automated using github action. You can go to Actions in your repo and check the deployment status. Also you can see the logs of your scripts by going to VM's terminal.

