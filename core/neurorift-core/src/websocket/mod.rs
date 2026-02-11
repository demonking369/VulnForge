pub mod events;

use anyhow::Result;
use futures_util::{SinkExt, StreamExt};
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::broadcast;
use tokio_tungstenite::{accept_async, tungstenite::Message};
use crate::websocket::events::WSEvent;

/// WebSocket server for real-time communication
pub struct WebSocketServer {
    addr: SocketAddr,
    event_tx: broadcast::Sender<WSEvent>,
}

impl WebSocketServer {
    /// Create a new WebSocket server
    pub fn new(addr: SocketAddr) -> Self {
        let (event_tx, _) = broadcast::channel(1000);
        
        Self {
            addr,
            event_tx,
        }
    }
    
    /// Get a sender for broadcasting events
    pub fn get_sender(&self) -> broadcast::Sender<WSEvent> {
        self.event_tx.clone()
    }
    
    /// Start the WebSocket server
    pub async fn run(self: Arc<Self>) -> Result<()> {
        let listener = TcpListener::bind(self.addr).await?;
        tracing::info!("WebSocket server listening on {}", self.addr);
        
        loop {
            match listener.accept().await {
                Ok((stream, peer_addr)) => {
                    tracing::info!("New connection from {}", peer_addr);
                    let server = self.clone();
                    tokio::spawn(async move {
                        if let Err(e) = server.handle_connection(stream).await {
                            tracing::error!("Connection error: {}", e);
                        }
                    });
                }
                Err(e) => {
                    tracing::error!("Accept error: {}", e);
                }
            }
        }
    }
    
    /// Handle a single WebSocket connection
    async fn handle_connection(&self, stream: TcpStream) -> Result<()> {
        let ws_stream = accept_async(stream).await?;
        let (mut ws_sender, mut ws_receiver) = ws_stream.split();
        
        // Subscribe to broadcast events
        let mut event_rx = self.event_tx.subscribe();
        
        // Spawn task to forward broadcast events to this client
        let mut send_task = tokio::spawn(async move {
            while let Ok(event) = event_rx.recv().await {
                let json = serde_json::to_string(&event).unwrap();
                if ws_sender.send(Message::Text(json)).await.is_err() {
                    break;
                }
            }
        });
        
        // Handle incoming messages from client
        let event_tx = self.event_tx.clone();
        let mut recv_task = tokio::spawn(async move {
            while let Some(msg) = ws_receiver.next().await {
                match msg {
                    Ok(Message::Text(text)) => {
                        // Parse client command
                        if let Ok(event) = serde_json::from_str::<WSEvent>(&text) {
                            // Broadcast to all clients (including sender)
                            let _ = event_tx.send(event);
                        }
                    }
                    Ok(Message::Close(_)) => {
                        tracing::info!("Client closed connection");
                        break;
                    }
                    Err(e) => {
                        tracing::error!("WebSocket error: {}", e);
                        break;
                    }
                    _ => {}
                }
            }
        });
        
        // Wait for either task to complete
        tokio::select! {
            _ = (&mut send_task) => {
                recv_task.abort();
            }
            _ = (&mut recv_task) => {
                send_task.abort();
            }
        }
        
        Ok(())
    }
    
    /// Broadcast an event to all connected clients
    pub fn broadcast(&self, event: WSEvent) {
        let _ = self.event_tx.send(event);
    }
}
