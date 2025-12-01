import os
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class EnvConfig:
    """Immutable configuration object for environment keys."""
    TEST_API_KEY: str
    TEST_SECRET_KEY: str
    JWT_SECRET: str
    ENVIRONMENT: str
    MASTER_KEY: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    SESSION_SECRET_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CALLBACK_URL: str

    @classmethod
    def load(cls) -> "EnvConfig":
        # Load .env file
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path, override=False)

        # Read all required keys
        required_keys = {
            "TEST_API_KEY": os.getenv("TEST_API_KEY"),
            "TEST_SECRET_KEY": os.getenv("TEST_SECRET_KEY"),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            "MASTER_KEY": os.getenv("MASTER_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT"),
            "SESSION_SECRET_KEY": os.getenv("SESSION_SECRET_KEY"),
            "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
            "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
            "GOOGLE_CALLBACK_URL": os.getenv("GOOGLE_CALLBACK_URL"),
        }

        # Detect missing or empty variables
        missing = [k for k, v in required_keys.items() if not v]
        if missing:
            raise EnvironmentError(
                f"❌ Missing env variables: {', '.join(missing)} in {env_path}"
            )

        # Sanity checks
        if len(required_keys["TEST_API_KEY"]) < 10:
            raise ValueError("❌ TEST_API_KEY is too short.")
        if len(required_keys["TEST_SECRET_KEY"]) < 10:
            raise ValueError("❌ TEST_SECRET_KEY is too short.")

        print("✅ Environment variables successfully loaded.")

        # Return full immutable config
        return cls(
            TEST_API_KEY=required_keys["TEST_API_KEY"],
            TEST_SECRET_KEY=required_keys["TEST_SECRET_KEY"],
            JWT_SECRET=required_keys["JWT_SECRET"],
            ENVIRONMENT=required_keys["ENVIRONMENT"],
            MASTER_KEY=required_keys["MASTER_KEY"],
            DB_NAME=required_keys["DB_NAME"],
            DB_USER=required_keys["DB_USER"],
            DB_PASSWORD=required_keys["DB_PASSWORD"],
            DB_HOST=required_keys["DB_HOST"],
            DB_PORT=required_keys["DB_PORT"],
            GOOGLE_CLIENT_ID=required_keys["GOOGLE_CLIENT_ID"],
            GOOGLE_CLIENT_SECRET=required_keys["GOOGLE_CLIENT_SECRET"],
            GOOGLE_CALLBACK_URL=required_keys["GOOGLE_CALLBACK_URL"],
            SESSION_SECRET_KEY=required_keys["SESSION_SECRET_KEY"]
        )

# Global config object
configLoaded = EnvConfig.load()
