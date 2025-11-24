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

    @classmethod
    def load(cls) -> "EnvConfig":
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path, override=False)

        required_keys = {
            "TEST_API_KEY": os.getenv("TEST_API_KEY"),
            "TEST_SECRET_KEY": os.getenv("TEST_SECRET_KEY"),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT"),
            "MASTER_KEY": os.getenv("MASTER_KEY")
        }

        # Detect missing or empty values
        missing = [k for k, v in required_keys.items() if not v]
        if missing:
            raise EnvironmentError(
                f"❌ Missing environment variables: {', '.join(missing)} in {env_path}"
            )

        # Basic sanity check for format
        if len(required_keys["TEST_API_KEY"]) < 10 or len(required_keys["TEST_SECRET_KEY"]) < 10:
            raise ValueError("❌ API keys appear too short or invalid. Please verify your .env file.")

        print("✅ Environment variables successfully loaded.")
        return cls(
            TEST_API_KEY=required_keys["TEST_API_KEY"],
            TEST_SECRET_KEY=required_keys["TEST_SECRET_KEY"],
            JWT_SECRET=required_keys["JWT_SECRET"],
            ENVIRONMENT=required_keys["ENVIRONMENT"],
            MASTER_KEY=required_keys["MASTER_KEY"]
        )

configLoaded = EnvConfig.load()