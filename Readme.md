# Analytics API

An analytics API microservice built to track and analyze web application traffic using time-series data. This project demonstrates building a complete data pipeline from scratch, handling event ingestion, storage, and aggregation for real-time analytics.

## Overview

This API allows you to collect and analyze web application events such as page views, user sessions, and interaction metrics. It's designed to handle high-volume time-series data efficiently using TimescaleDB, a PostgreSQL extension optimized for time-series workloads.

The service provides REST endpoints for:
- Ingesting analytics events (page views, user interactions)
- Querying aggregated analytics data with time-bucketing
- Filtering by pages, time ranges, and user attributes
- Operating system detection from user agent strings

## Demo

A demo showing how to interact with the API is available in the [demo notebook](notebooks/demo-interacting-with-api.ipynb). The demo covers creating events, querying analytics data, and working with the time-series aggregations. Click the link to view the notebook directly in GitHub's notebook viewer.



## Tech Stack

- **Python 3.12+** - Core language
- **FastAPI** - Modern async web framework
- **SQLModel + SQLAlchemy** - ORM and database toolkit
- **TimescaleDB** - PostgreSQL extension for time-series data
- **Docker** - Containerization and deployment
- **Poetry** - Dependency management

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

### Running with Docker Compose


```bash
docker compose up
```

This will start both the API service and TimescaleDB database. The API will be available at `http://localhost:8002`.

To stop the services:

```bash
docker compose down
```

To remove volumes (clears database data):

```bash
docker compose down -v
```


## API Endpoints

- `POST /api/events/` - Create a new analytics event
- `GET /api/events/` - Get aggregated analytics data
- `GET /api/events/{event_id}` - Get a specific event by ID
- `GET /healthz` - Health check endpoint

