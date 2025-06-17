#!/usr/bin/env python3
"""
VulnForge Notification System
Handles alerts and notifications for findings
"""

import json
import logging
import smtplib
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import asyncio
import aiohttp

class Notifier:
    def __init__(self, config_manager: Any):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.notification_queue = asyncio.Queue()
        self.worker_task = None
        
    async def start(self):
        """Start notification worker"""
        self.worker_task = asyncio.create_task(self._notification_worker())
        
    async def stop(self):
        """Stop notification worker"""
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
                
    async def notify(self, message: str, severity: str = "info", 
                    data: Optional[Dict] = None, channels: Optional[List[str]] = None):
        """Queue a notification"""
        notification = {
            "message": message,
            "severity": severity,
            "data": data or {},
            "timestamp": datetime.now().isoformat(),
            "channels": channels or self._get_enabled_channels()
        }
        
        await self.notification_queue.put(notification)
        
    async def _notification_worker(self):
        """Process notification queue"""
        while True:
            try:
                notification = await self.notification_queue.get()
                await self._process_notification(notification)
                self.notification_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing notification: {e}")
                
    async def _process_notification(self, notification: Dict):
        """Process a single notification"""
        for channel in notification["channels"]:
            try:
                if channel == "email":
                    await self._send_email(notification)
                elif channel == "discord":
                    await self._send_discord(notification)
                elif channel == "webhook":
                    await self._send_webhook(notification)
            except Exception as e:
                self.logger.error(f"Error sending notification to {channel}: {e}")
                
    async def _send_email(self, notification: Dict):
        """Send email notification"""
        if not self.config.get("notifications.email.enabled"):
            return
            
        try:
            msg = MIMEMultipart()
            msg["Subject"] = f"VulnForge Alert: {notification['severity'].upper()}"
            msg["From"] = self.config.get("notifications.email.username")
            msg["To"] = self.config.get("notifications.email.username")
            
            # Build email body
            body = f"""
            VulnForge Alert
            --------------
            Severity: {notification['severity']}
            Time: {notification['timestamp']}
            
            Message:
            {notification['message']}
            
            Additional Data:
            {json.dumps(notification['data'], indent=2)}
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            # Send email
            with smtplib.SMTP(
                self.config.get("notifications.email.smtp_server"),
                self.config.get("notifications.email.smtp_port")
            ) as server:
                server.starttls()
                server.login(
                    self.config.get("notifications.email.username"),
                    self.config.get("notifications.email.password")
                )
                server.send_message(msg)
                
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            
    async def _send_discord(self, notification: Dict):
        """Send Discord notification"""
        if not self.config.get("notifications.discord.enabled"):
            return
            
        webhook_url = self.config.get("notifications.discord.webhook_url")
        if not webhook_url:
            return
            
        try:
            # Create Discord embed
            embed = {
                "title": f"VulnForge Alert: {notification['severity'].upper()}",
                "description": notification["message"],
                "color": self._get_severity_color(notification["severity"]),
                "timestamp": notification["timestamp"],
                "fields": [
                    {
                        "name": "Severity",
                        "value": notification["severity"],
                        "inline": True
                    }
                ]
            }
            
            # Add data fields
            for key, value in notification["data"].items():
                embed["fields"].append({
                    "name": key,
                    "value": str(value),
                    "inline": False
                })
                
            # Send to Discord
            async with aiohttp.ClientSession() as session:
                await session.post(webhook_url, json={"embeds": [embed]})
                
        except Exception as e:
            self.logger.error(f"Error sending Discord notification: {e}")
            
    async def _send_webhook(self, notification: Dict):
        """Send generic webhook notification"""
        webhook_url = self.config.get("notifications.webhook_url")
        if not webhook_url:
            return
            
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(webhook_url, json=notification)
        except Exception as e:
            self.logger.error(f"Error sending webhook notification: {e}")
            
    def _get_enabled_channels(self) -> List[str]:
        """Get list of enabled notification channels"""
        channels = []
        
        if self.config.get("notifications.email.enabled"):
            channels.append("email")
            
        if self.config.get("notifications.discord.enabled"):
            channels.append("discord")
            
        if self.config.get("notifications.webhook_url"):
            channels.append("webhook")
            
        return channels
        
    def _get_severity_color(self, severity: str) -> int:
        """Get Discord color for severity level"""
        colors = {
            "critical": 0xFF0000,  # Red
            "high": 0xFFA500,      # Orange
            "medium": 0xFFFF00,    # Yellow
            "low": 0x00FF00,       # Green
            "info": 0x0000FF       # Blue
        }
        return colors.get(severity.lower(), 0x808080)  # Default to gray 