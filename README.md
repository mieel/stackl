![Stackl](docs/website/static/img/logos/logo.png)

# Stackl

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code-of-conduct.md)
![](https://github.com/Stacklio/Stackl/workflows/Upload%20Python%20Package/badge.svg) [![](https://img.shields.io/pypi/v/Stackl-cli.svg?label=PyPI%20Stackl-cli)](https://pypi.python.org/pypi/Stackl-cli/)
[![quay image Stackl-cli](https://quay.io/repository/Stackl/Stackl-cli/status "quay image Stackl-cli")](https://quay.io/repository/Stackl/Stackl-cli)
[![quay image Stackl-core](https://quay.io/repository/Stackl/Stackl-core/status "quay image Stackl-core")](https://quay.io/repository/Stackl/Stackl-core)
[![quay image Stackl-agent](https://quay.io/repository/Stackl/Stackl-agent/status "quay image Stackl-agent")](https://quay.io/repository/Stackl/Stackl-agent)


**Stackl** is an open-source software platform that provides a flexible method to create, model, describe, and automate application deployments.
Stackl enables autonomous configuration, coordination, and management of applications and IT infrastructure.

Stackl achieves this by:

* forming a **single source of truth** (SSOT) configuration data store for your IT environment: infrastructure resources, application definitions, and their characteristics and services

* **decoupling** configuration data, automation strategy, and deployment targets, to **simplify** and increase **re-usability** infrasctructure as code components.

* providing **pluggable modules** for backend systems, such as processing and data storage, to support different scalability and performance requirements and enable users to **choose their preferred tools**

In essence, it allows you to model, describe, and automate your application orchestration workflow, using a **version control system** (Git) to track and trigger changes, and provides a CLI interface for easy integrating with **any CI/CD** platform.
# Stackl Components

In a nutshell, Stackl consist out of these components:
- Stackl Host/Core: The controller component which controls the state and orchestrates the agents
- Stackl Agent: Carries out deployments jobs, ensuring stack inst
- Stackl CLI
- Stackl Documents
```mermaid
flowchart LR;
  %% Components
  subgraph Infrastructure Components
    acceptance_env
    production_env
    development_env

    security_zone
    public_zone

    azure_loc
    vware_loc
  end

  subgraph Infrastructure Templates
    AZURE_ACC_Infra
    AZURE_PROD_Infra
    VMWARE_DEV_Infra
  end

  subgraph Application Templates
    WikiApp_Template
    TicketingApp_Template
  end

  subgraph Functional Requirements
  setup_resourcegroup
  setup_vnet
  apply_security
  deploy_cloud_vm
  apply_database_role
  apply_wiki_app_role
  apply_wiki_web_role
  end

  subgraph Services
  base_service
  frontend_service
  backend_service
  database_service
  end

  %% relationships
  WikiApp_Template-->  base_service & frontend_service & backend_service &  database_service

  AZURE_ACC_Infra---acceptance_env;
  AZURE_ACC_Infra---azure_loc;
  AZURE_ACC_Infra---security_zone;
  AZURE_PROD_Infra---production_env;
  AZURE_PROD_Infra---azure_loc;
  AZURE_PROD_Infra---security_zone;

  StackInstance_ACC---AZURE_ACC_Infra & WikiApp_Template;
  StackInstance_PROD---AZURE_PROD_Infra & WikiApp_Template;

  base_service---setup_resourcegroup & setup_vnet & apply_security
  frontend_service---deploy_cloud_vm & apply_wiki_web_role
  backend_service---deploy_cloud_vm & apply_database_role
  database_service---deploy_cloud_vm & apply_wiki_app_role

```

## :rocket:Installation

This section includes a quick guide to what is required, how to install, and how to do a first test run.

### Prerequisites

* Kubernetes environment
* Helm 3
* Kubectl

### Installing

* Clone the Helm repository `git clone git@github.com:Stacklio/Stackl-helm.git`
* Create a namespace that will house the Stackl deployment `kubectl create namespace Stackl`
* Execute the following command to deploy Stackl in the active K8s context: `helm install Stackl -n Stackl --generate-name`
* Execute the following command to deploy Stackl agent in the active K8s context: `helm install Stackl -n Stackl-agent --generate-name`

You can see all the pods with the following command: `watch kubectl get pods -n Stackl`

![helm install](docs/static/media/helm-install.gif)

## More info about Stackl

### Core goals

* Open-source and community-oriented
  * Based on coding best practices
  * Consistent use of standards and guidelines
  * Documented
* Adaptable, flexible, general-purpose, and extensible
  * Integrates with a variety of pluggable modules including custom and no critical technology dependencies
  * Focus on working with current known and popular tools and software
  * Internally/externally uniform and accessible by using universal standards and terminology
  * Driven by specifiable policies to enable flexible orchestration
* Scalable, lightweight, and performant
  * Distributable across infrastructure and easy to scale
  * Able to make trade-offs to match different quality-of-service requirements
* End-to-end support for microservices and infrastructure management in a DevOps workflow (interesting read: [What is DevOps?](https://www.atlassian.com/devops))

### Features

* Stackl works with YAML or JSON documents to allow  for easy Key/Value management and future-proof cross-system compatibility
* Stackl provides a REST API with a web interface
* Users supply Stack Application Templates (SATs), which model and describe the desired applications, and Stack Infrastructure Templates (SITs), which specify the IT infrastructure available for use for the application. SITs and SATs can be processed and matched according to specified policies and result in a Stack Template, a Key/Value document that describes the desired state of an application on the infrastructure and can be deployed in the users IT environment by orchestration tools
* Stackl supports pluggable modules to allow users to use their desired technological backends. For instance, the used datastore and task processing solutions can be specified by the user
* Stackl is engineered to allow easy extensions for new technological backends through providing interfaces that enable transparent interaction
* Entities, i.e., workers, automation platforms, agents, … ,  are fully decoupled and can be distributed to improve fault-tolerance and scalability.
* The deployment and use of Stackl works with popular DevOps technologies and platforms: Docker, Kubernetes, Ansible, Azure, AWS, and is oriented towards the future, for instance, for serverless computing (FaaS/SaaS).
* Autonomous operation is a key focus: as much as possible, after deployment of Stackl, the system and its entities will self-manage and self-discover
* To allow rapid use of Stackl, it provides a minimal and fast setup on a regular computer for a normal user. Button-press fire-and-forget deployment of Stackl enables users to take it for a quick spin.

### Even more information

* See [Stackl.io](https://www.Stackl.io) to get started with documentation and tutorials.
* See [Stackl slides](https://drive.google.com/open?id=10ZmqGU3pOc6EJyZpED4fMgav5pD01RztLkfSn3Jl9EA) for a short presentation about Stackl.

## Contributing

Contributions, issues, and feature requests are always more than welcome! Feel free to check [issues page](https://github.com/Stacklio/Stackl/issues) if you want to contribute.

Stackl is programmed mainly in Python 3 and meant to follow best-practice coding guidelines.
As a point-of-reference, we use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for coding and the [Google developer documentation style guide](https://developers.google.com/style) for documentation.

See [CONTRIBUTING](CONTRIBUTING.md) to get started.
Please also read the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md).

For a list of changes, see [Changelog](CHANGELOG.md).
For the releases, see [Github Releases](https://github.com/Stacklio/Stackl/releases).

## Security

### Reporting Security Vulnerabilities

Please report vulnerabilities by email to [Stackl-security](mailto:Stackl-security@Stackl.io).
We will send a confirmation message to acknowledge that we have received the report and we will inform you once the issue has been investigated.

## License

The code in this project is licensed under the [GLPv3](LICENSE) license.

## Acknowledgments

Stackl was initially created for in-house use by [Nubera](https://www.nubera.eu/), a DevOps consultancy company who saw the need for a platform to better provide services to clients. After some time, it became clear that Stackl could be useful to the general DevOps community as well so the decision was made to spin it off as an open source project.
Hence, thanks to [Nubera](https://www.nubera.eu/)  and [Yannick Struyf](https://github.com/yannickstruyf3) who put in much of the hard initial work.
