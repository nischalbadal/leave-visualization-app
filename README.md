<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="20%" alt="LEAVE-VISUALIZATION-APP-logo">
</p>
<p align="center">
    <h1 align="center">LEAVE-VISUALIZATION-APP</h1>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/nischalbadal/leave-visualization-app?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/nischalbadal/leave-visualization-app?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/nischalbadal/leave-visualization-app?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/nischalbadal/leave-visualization-app?style=flat&color=0080ff" alt="repo-language-count">
</p>
<p align="center">
		<em>Built with the tools and technologies:</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
	<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style=flat&logo=Plotly&logoColor=white" alt="Plotly">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<br>
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
	<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
</p>

<br>

#####  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
    - [ Prerequisites](#-prerequisites)
    - [ Installation](#-installation)
    - [ Usage](#-usage)
    - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

The Employee Leave Visualization System is a comprehensive application designed to manage and visualize employee leave data. It consists of a Flask backend to handle API requests, a PostgreSQL database for data storage, and a Streamlit frontend for data visualization.

---

##  Repository Structure

```sh
└── leave-visualization-app/
    ├── .github
    │   └── workflows
    ├── README.md
    ├── __pycache__
    │   └── config.cpython-311.pyc
    ├── alembic
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    ├── alembic.ini
    ├── app
    │   ├── __init__.py
    │   ├── backend
    │   └── frontend
    ├── docker
    │   └── pgsql
    ├── docker-compose.yml
    ├── pipeline
    │   ├── Dockerfile
    │   ├── Makefile
    │   ├── files
    │   ├── requirements.txt
    │   ├── schedule.sh
    │   └── src
    └── run.py
```

---

##  Modules

<details closed><summary>.</summary>

| File | Summary |
| --- | --- |
| [run.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/run.py) |  |
| [docker-compose.yml](https://github.com/nischalbadal/leave-visualization-app/blob/main/docker-compose.yml) |  |

</details>

<details closed><summary>.github.workflows</summary>

| File | Summary |
| --- | --- |
| [ci.yml](https://github.com/nischalbadal/leave-visualization-app/blob/main/.github/workflows/ci.yml) |  |

</details>

<details closed><summary>docker.pgsql</summary>

| File | Summary |
| --- | --- |
| [docker-compose.yml](https://github.com/nischalbadal/leave-visualization-app/blob/main/docker/pgsql/docker-compose.yml) |  |

</details>

<details closed><summary>pipeline</summary>

| File | Summary |
| --- | --- |
| [requirements.txt](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/requirements.txt) |  |
| [Makefile](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/Makefile) |  |
| [schedule.sh](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/schedule.sh) |  |
| [Dockerfile](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/Dockerfile) |  |

</details>

<details closed><summary>pipeline.src</summary>

| File | Summary |
| --- | --- |
| [api_loader.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/api_loader.py) |  |
| [utils.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/utils.py) |  |
| [config.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/config.py) |  |
| [extraction.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/extraction.py) |  |
| [transformation.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/transformation.py) |  |
| [data_loader.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/data_loader.py) |  |
| [validation.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/validation.py) |  |
| [bulk_upload.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/bulk_upload.py) |  |
| [payload.json.example](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/payload.json.example) |  |
| [data-transfer.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/data-transfer.py) |  |

</details>

<details closed><summary>pipeline.src.sql</summary>

| File | Summary |
| --- | --- |
| [load_leave_requests.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/load_leave_requests.sql) |  |
| [load_fiscal_years.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/load_fiscal_years.sql) |  |
| [load_leave_types.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/load_leave_types.sql) |  |
| [load_designations.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/load_designations.sql) |  |
| [load_users.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/load_users.sql) |  |

</details>

<details closed><summary>pipeline.src.sql.dw</summary>

| File | Summary |
| --- | --- |
| [load_dim_fiscal_periods.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_dim_fiscal_periods.sql) |  |
| [load_dim_designations.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_dim_designations.sql) |  |
| [load_dim_leave_types.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_dim_leave_types.sql) |  |
| [load_fact_leave_requests.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_fact_leave_requests.sql) |  |
| [load_dim_users.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_dim_users.sql) |  |
| [load_dim_leave_issuer.sql](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/src/sql/dw/load_dim_leave_issuer.sql) |  |

</details>

<details closed><summary>pipeline.files</summary>

| File | Summary |
| --- | --- |
| [vyaguta-api-response.json](https://github.com/nischalbadal/leave-visualization-app/blob/main/pipeline/files/vyaguta-api-response.json) |  |

</details>

<details closed><summary>alembic</summary>

| File | Summary |
| --- | --- |
| [script.py.mako](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/script.py.mako) |  |
| [env.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/env.py) |  |

</details>

<details closed><summary>alembic.versions</summary>

| File | Summary |
| --- | --- |
| [9c3de66d8283_create_user_accounts_table.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/9c3de66d8283_create_user_accounts_table.py) |  |
| [d57c4911a2c2_add_normalized_tables.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/d57c4911a2c2_add_normalized_tables.py) |  |
| [6a1ed01895db_create_pipeline_logs_table.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/6a1ed01895db_create_pipeline_logs_table.py) |  |
| [ac84fec986a5_create_qc_reports_table.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/ac84fec986a5_create_qc_reports_table.py) |  |
| [19e9f181c726_add_raw_data_from_api.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/19e9f181c726_add_raw_data_from_api.py) |  |
| [759ad2a9c833_add_data_warehouse_tables.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/alembic/versions/759ad2a9c833_add_data_warehouse_tables.py) |  |

</details>

<details closed><summary>app.backend</summary>

| File | Summary |
| --- | --- |
| [app.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/app.py) |  |
| [config.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/config.py) |  |
| [requirements.txt](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/requirements.txt) |  |
| [routes.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/routes.py) |  |
| [util.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/util.py) |  |
| [Dockerfile](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/Dockerfile) |  |
| [models.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/backend/models.py) |  |

</details>

<details closed><summary>app.frontend</summary>

| File | Summary |
| --- | --- |
| [app.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/app.py) |  |
| [config.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/config.py) |  |
| [requirements.txt](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/requirements.txt) |  |
| [Dockerfile](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/Dockerfile) |  |

</details>

<details closed><summary>app.frontend.page</summary>

| File | Summary |
| --- | --- |
| [custom.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/page/custom.py) |  |
| [employee.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/page/employee.py) |  |
| [top_visualization.py](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/page/top_visualization.py) |  |

</details>

<details closed><summary>app.frontend..streamlit</summary>

| File | Summary |
| --- | --- |
| [config.toml](https://github.com/nischalbadal/leave-visualization-app/blob/main/app/frontend/.streamlit/config.toml) |  |

</details>

---

##  Getting Started

###  Prerequisites

**Python**: `version x.y.z`

###  Installation

Build the project from source:

1. Clone the leave-visualization-app repository:
```sh
❯ git clone https://github.com/nischalbadal/leave-visualization-app
```

2. Navigate to the project directory:
```sh
❯ cd leave-visualization-app
```

3. Install the required dependencies:
```sh
❯ pip install -r requirements.txt
```

###  Usage

To run the project, execute the following command:

```sh
❯ python main.py
```

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/nischalbadal/leave-visualization-app/issues)**: Submit bugs found or log feature requests for the `leave-visualization-app` project.
- **[Submit Pull Requests](https://github.com/nischalbadal/leave-visualization-app/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/nischalbadal/leave-visualization-app/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/nischalbadal/leave-visualization-app
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/nischalbadal/leave-visualization-app/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=nischalbadal/leave-visualization-app">
   </a>
</p>
</details>

---

##  License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/nischalbadal/leave-visualization-app/blob/main/LICENSE) file for details.
---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
