# Task Tracker



A simple task management REST API built to learn Kubernetes, GitOps, and service mesh concepts.



## Tech Stack



\- \*\*Python 3.12\*\* + \*\*FastAPI\*\* — REST API

\- \*\*Pydantic\*\* — data validation

\- \*\*Prometheus client\*\* — metrics exposure

\- \*\*Docker\*\* — containerization

\- \*\*Kubernetes (EKS)\*\* — orchestration

\- \*\*ArgoCD\*\* — GitOps continuous deployment

\- \*\*Istio Ambient\*\* — service mesh + canary deployments

\- \*\*Prometheus + Grafana\*\* — monitoring



## Endpoints



| Method | Path           | Description              |

|--------|----------------|--------------------------|

| GET    | `/`            | Welcome message          |

| GET    | `/health`      | Kubernetes health probe  |

| GET    | `/tasks`       | List all tasks           |

| POST   | `/tasks`       | Create a new task        |

| DELETE | `/tasks/{id}`  | Delete a task            |

| GET    | `/metrics`     | Prometheus metrics       |



## Running Locally



```bash

pip install -r requirements.txt

uvicorn main:app --reload

```



Then open `http://localhost:8000/docs` for the interactive API.



## Running with Docker



```bash

docker build -t task-tracker:v1 .

docker run -d -p 8000:8000 task-tracker:v1

```



## Project Status



Built as part of my SDAIA co-op program — an end-to-end demonstration of modern cloud-native deployment practices.

