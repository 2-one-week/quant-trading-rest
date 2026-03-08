from dataclasses import dataclass
from pathlib import Path
import tomllib

from core.infra.util import find_project_root


@dataclass(frozen=True)
class TradingProfile:
    broker: str
    name: str
    key_file: Path
    order_file: Path | None
    mock: bool


def load_trading_profile(
    broker: str, profile_name: str, start: Path | None = None
) -> TradingProfile:
    project_root = find_project_root(start)
    config_path = project_root / "trading_profiles.toml"

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Trading profile config not found: {config_path}") from exc

    broker_config = config.get(broker)
    if not isinstance(broker_config, dict):
        raise RuntimeError(
            f"Broker profile section '{broker}' not found in {config_path}"
        )

    profile = broker_config.get(profile_name)
    if not isinstance(profile, dict):
        available = ", ".join(sorted(broker_config.keys())) or "(none)"
        raise RuntimeError(
            f"Trading profile '{broker}.{profile_name}' not found in {config_path}. "
            f"Available profiles: {available}"
        )

    key_value = profile.get("key_file")
    if not key_value:
        raise RuntimeError(
            f"Trading profile '{broker}.{profile_name}' is missing 'key_file'"
        )

    order_value = profile.get("order_file")
    return TradingProfile(
        broker=broker,
        name=profile_name,
        key_file=project_root / key_value,
        order_file=(project_root / order_value) if order_value else None,
        mock=bool(profile.get("mock", False)),
    )
