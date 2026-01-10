from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class EnrichmentSettings:
    hibp_api_key: Optional[str] = os.getenv("HIBP_API_KEY")
    shodan_api_key: Optional[str] = os.getenv("SHODAN_API_KEY")
    censys_id: Optional[str] = os.getenv("CENSYS_API_ID")
    censys_secret: Optional[str] = os.getenv("CENSYS_API_SECRET")
    passive_dns_endpoint: Optional[str] = os.getenv("PASSIVE_DNS_ENDPOINT")
    passive_dns_token: Optional[str] = os.getenv("PASSIVE_DNS_TOKEN")


async def call_with_retries(func, *args, **kwargs):
    retries = 3
    delay = 1
    for attempt in range(1, retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:
            if attempt == retries:
                logger.warning("enrich.retry_exhausted", extra={"error": str(exc)})
                return {"error": str(exc)}
            await asyncio.sleep(delay)
            delay *= 2


async def hibp_lookup(
    client: httpx.AsyncClient, email: str, settings: EnrichmentSettings
):
    if not settings.hibp_api_key or "@" not in email:
        return {"enabled": False}
    headers = {"hibp-api-key": settings.hibp_api_key}
    resp = await client.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
        headers=headers,
        timeout=10,
    )
    if resp.status_code == 404:
        return {"found": False}
    resp.raise_for_status()
    return {"found": True, "breaches": resp.json()}


async def shodan_lookup(
    client: httpx.AsyncClient, target: str, settings: EnrichmentSettings
):
    if not settings.shodan_api_key:
        return {"enabled": False}
    resp = await client.get(
        "https://api.shodan.io/shodan/host/search",
        params={"query": target, "key": settings.shodan_api_key},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return {"matches": data.get("matches", [])[:5]}


async def censys_lookup(
    client: httpx.AsyncClient, target: str, settings: EnrichmentSettings
):
    if not settings.censys_id or not settings.censys_secret:
        return {"enabled": False}
    resp = await client.get(
        "https://search.censys.io/api/v2/hosts/search",
        params={"q": target},
        auth=(settings.censys_id, settings.censys_secret),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


async def passive_dns_lookup(
    client: httpx.AsyncClient, target: str, settings: EnrichmentSettings
):
    if not settings.passive_dns_endpoint:
        return {"enabled": False}
    headers = {}
    if settings.passive_dns_token:
        headers["Authorization"] = f"Bearer {settings.passive_dns_token}"
    resp = await client.get(
        settings.passive_dns_endpoint,
        params={"q": target},
        headers=headers,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


async def enrich(
    structured_fields: Dict[str, Any], target_value: str
) -> Dict[str, Any]:
    settings = EnrichmentSettings()
    async with httpx.AsyncClient() as client:
        tasks = []
        email = structured_fields.get("email")
        tasks.append(call_with_retries(hibp_lookup, client, email or "", settings))
        tasks.append(call_with_retries(shodan_lookup, client, target_value, settings))
        tasks.append(call_with_retries(censys_lookup, client, target_value, settings))
        tasks.append(
            call_with_retries(passive_dns_lookup, client, target_value, settings)
        )
        results = await asyncio.gather(*tasks)

    return {
        "hibp": results[0],
        "shodan": results[1],
        "censys": results[2],
        "passive_dns": results[3],
    }
