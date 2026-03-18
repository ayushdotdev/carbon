import os


def pytest_sessionstart(session):
    """
    Sets up the environment variables before any tests or app code are imported.
    """
    os.environ["BOT_TOKEN"] = "mock_token"
    os.environ["DB_URL"] = "postgresql+asyncpg://user:pass@localhost:5432/db"
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["REDIS_PASSWORD"] = "mock_pass"
