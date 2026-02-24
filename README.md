# AstrologyAPI
 Natal Chart & Compatibility Calculation Service


## Project Overview

AstrologyAPI is a web service for calculating astrological natal charts and relationship compatibility (synastry).

The application allows users to:

- Build a full natal chart based on birth date, time, and geographic location
- Calculate planetary positions and house cusps (Placidus system)
- Detect aspects within a natal chart
- Compare two charts and compute compatibility scores
- Retrieve structured results via REST API endpoints

The service uses the Swiss Ephemeris library for precise astronomical calculations.


## Installation

The project is deployed using Docker.

### Prerequisites

- Docker
- Docker Compose

### Setup Instructions

##### 1. Clone the repository

    git clone https://github.com/andreibaliyevich/AstrologyAPI.git

##### 2. Navigate to the project directory

    cd AstrologyAPI

##### 3. Add Swiss Ephemeris data files

Download the Swiss Ephemeris ephemeris files from:

[https://www.astro.com/ftp/swisseph/ephe/](https://www.astro.com/ftp/swisseph/ephe/)

After downloading, copy the entire ephe folder into the backend directory of the project so that the structure becomes:

    backend/
    ├── app/
    ├── ephe/

> **Note:**
> The ephe directory must be located inside the backend folder, next to the app directory.
> This folder contains astronomical data required for planetary position calculations.
> Without these files, natal chart computation will not work correctly.

##### 4. Build Docker images

    docker compose build

##### 5. Start the service

    docker compose up

The API will be available at:

    http://localhost:5000


## API Endpoints

### Natal Chart

    /charts/build

Builds a natal chart based on provided birth data.

### Compatibility

    /charts/compare

Compares two natal charts and returns compatibility analysis.


## License

This project is licensed under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)
