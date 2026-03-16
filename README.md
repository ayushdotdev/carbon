| ![](assets/bnnr.jpg) |
| -------------------- |

# Carbon [WIP]

> **Handle your discord server. Effortlessly.**

Carbon is a modern, high-performance Discord management bot designed to streamline moderation and enhance server management. Built with `discord.py`, `SQLAlchemy`, and `Redis`, it offers a robust and scalable solution for communities of all sizes.

## ✨ Features

- **Automated Moderation:** Streamline ban and warn processes.
- **Appeal System:** Integrated ban and warn appeal logs and settings.
- **Internationalization (i18n):** Multi-language support out of the box.
- **Reason Aliases:** Save time with shortcuts for common moderation reasons.
- **Clean Defaults:** Sensible default configurations for a hassle-free setup.
- **Developer-Friendly:** Clean service-oriented architecture for easy extensibility.

## 🚀 Getting Started

### Prerequisites

- **Python:** 3.12 or higher
- **Poetry:** For dependency management
- **PostgreSQL:** For persistent data storage
- **Redis:** For caching and performance
- **Discord Bot:** From the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/sudoscrawl/carbon.git
    cd carbon
    ```

2.  **Install Dependencies:**

    ```bash
    poetry install
    ```

3.  **Configure Environment Variables:**
    Copy the `.env.example` file and fill in your details:

    ```bash
    cp .env.example .env
    ```

    Edit `.env` and provide your `BOT_TOKEN`, `DB_URL`, and Redis credentials.

4.  **Run Migrations (if applicable):**

    ```bash
    poetry run alembic upgrade head
    ```

5.  **Start the Bot:**
    ```bash
    poetry run python main.py
    ```

### Running with Docker

You can also run Carbon using Docker Compose:

```bash
docker-compose up -d
```

## 🛠️ Tech Stack

- **Language:** [Python 3.12](https://www.python.org/)
- **Library:** [discord.py](https://github.com/Rapptz/discord.py)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Caching:** [Redis](https://redis.io/)
- **Logging:** [structlog](https://www.structlog.org/)
- **i18n:** [Babel](https://babel.pocoo.org/)

## 📜 License

This project is licensed under the [GPL-3.0 License](LICENSE).
