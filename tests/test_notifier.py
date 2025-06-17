#!/usr/bin/env python3
"""
Tests for the VulnForge notification system
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from utils.notifier import Notifier

@pytest.fixture
def mock_config():
    config = Mock()
    config.get.side_effect = lambda key: {
        "notifications.email.enabled": True,
        "notifications.email.username": "test@example.com",
        "notifications.email.password": "password123",
        "notifications.email.smtp_server": "smtp.example.com",
        "notifications.email.smtp_port": 587,
        "notifications.discord.enabled": True,
        "notifications.discord.webhook_url": "https://discord.com/api/webhooks/test",
        "notifications.webhook_url": "https://example.com/webhook"
    }.get(key)
    return config

@pytest.fixture
async def notifier(mock_config):
    notifier = Notifier(mock_config)
    await notifier.start()
    yield notifier
    await notifier.stop()

@pytest.mark.asyncio
async def test_notify_basic(notifier):
    """Test basic notification"""
    with patch("utils.notifier.Notifier._process_notification") as mock_process:
        await notifier.notify("Test message", "info")
        await asyncio.sleep(0.1)  # Allow time for queue processing
        mock_process.assert_called_once()

@pytest.mark.asyncio
async def test_notify_with_data(notifier):
    """Test notification with additional data"""
    test_data = {
        "vulnerability": "SQL Injection",
        "severity": "high",
        "affected_url": "https://example.com/login"
    }
    
    with patch("utils.notifier.Notifier._process_notification") as mock_process:
        await notifier.notify("Vulnerability found", "high", data=test_data)
        await asyncio.sleep(0.1)
        
        # Verify notification data
        call_args = mock_process.call_args[0][0]
        assert call_args["message"] == "Vulnerability found"
        assert call_args["severity"] == "high"
        assert call_args["data"] == test_data

@pytest.mark.asyncio
async def test_notify_specific_channels(notifier):
    """Test notification to specific channels"""
    with patch("utils.notifier.Notifier._process_notification") as mock_process:
        await notifier.notify(
            "Test message",
            "info",
            channels=["email", "discord"]
        )
        await asyncio.sleep(0.1)
        
        # Verify channels
        call_args = mock_process.call_args[0][0]
        assert set(call_args["channels"]) == {"email", "discord"}

@pytest.mark.asyncio
async def test_email_notification(notifier):
    """Test email notification sending"""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.return_value.__enter__.return_value = mock_smtp.return_value
        
        await notifier.notify(
            "Test email",
            "critical",
            channels=["email"]
        )
        await asyncio.sleep(0.1)
        
        # Verify SMTP was called
        mock_smtp.assert_called_once_with(
            "smtp.example.com",
            587
        )

@pytest.mark.asyncio
async def test_discord_notification(notifier):
    """Test Discord notification sending"""
    with patch("aiohttp.ClientSession.post") as mock_post:
        await notifier.notify(
            "Test Discord",
            "high",
            data={"finding": "XSS vulnerability"},
            channels=["discord"]
        )
        await asyncio.sleep(0.1)
        
        # Verify Discord webhook was called
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]["json"]
        assert "embeds" in call_args
        assert len(call_args["embeds"]) == 1
        assert call_args["embeds"][0]["title"] == "VulnForge Alert: HIGH"

@pytest.mark.asyncio
async def test_webhook_notification(notifier):
    """Test generic webhook notification"""
    with patch("aiohttp.ClientSession.post") as mock_post:
        test_data = {
            "scan_id": "123",
            "target": "example.com",
            "findings": ["vuln1", "vuln2"]
        }
        
        await notifier.notify(
            "Test webhook",
            "medium",
            data=test_data,
            channels=["webhook"]
        )
        await asyncio.sleep(0.1)
        
        # Verify webhook was called
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]["json"]
        assert call_args["message"] == "Test webhook"
        assert call_args["severity"] == "medium"
        assert call_args["data"] == test_data

@pytest.mark.asyncio
async def test_severity_colors(notifier):
    """Test severity color mapping"""
    colors = {
        "critical": 0xFF0000,
        "high": 0xFFA500,
        "medium": 0xFFFF00,
        "low": 0x00FF00,
        "info": 0x0000FF
    }
    
    for severity, expected_color in colors.items():
        color = notifier._get_severity_color(severity)
        assert color == expected_color
        
    # Test unknown severity
    assert notifier._get_severity_color("unknown") == 0x808080 