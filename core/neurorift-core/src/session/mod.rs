use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::fs;
use chrono::{DateTime, Utc};
use crate::state::SessionState;

/// .nrs file format version
const NRS_VERSION: &str = "1.0";

/// .nrs file structure
#[derive(Debug, Serialize, Deserialize)]
pub struct NrsFile {
    pub version: String,
    pub session: SessionState,
    pub saved_at: DateTime<Utc>,
}

/// Session persistence manager
pub struct SessionManager {
    sessions_dir: PathBuf,
}

impl SessionManager {
    /// Create a new session manager
    pub fn new(base_dir: impl AsRef<Path>) -> Result<Self> {
        let sessions_dir = base_dir.as_ref().join("sessions");
        fs::create_dir_all(&sessions_dir)
            .context("Failed to create sessions directory")?;
        
        Ok(Self { sessions_dir })
    }
    
    /// Save session to .nrs file
    pub fn save_session(&self, session: &SessionState) -> Result<PathBuf> {
        let nrs_file = NrsFile {
            version: NRS_VERSION.to_string(),
            session: session.clone(),
            saved_at: Utc::now(),
        };
        
        let filename = format!("{}.nrs", session.id);
        let path = self.sessions_dir.join(&filename);
        
        let json = serde_json::to_string_pretty(&nrs_file)
            .context("Failed to serialize session")?;
        
        fs::write(&path, json)
            .context("Failed to write session file")?;
        
        tracing::info!("Session saved: {}", path.display());
        Ok(path)
    }
    
    /// Load session from .nrs file
    pub fn load_session(&self, session_id: &str) -> Result<SessionState> {
        let filename = format!("{}.nrs", session_id);
        let path = self.sessions_dir.join(&filename);
        
        let json = fs::read_to_string(&path)
            .context("Failed to read session file")?;
        
        let nrs_file: NrsFile = serde_json::from_str(&json)
            .context("Failed to deserialize session")?;
        
        // Version check
        if nrs_file.version != NRS_VERSION {
            tracing::warn!("Session file version mismatch: {} != {}", nrs_file.version, NRS_VERSION);
        }
        
        tracing::info!("Session loaded: {}", session_id);
        Ok(nrs_file.session)
    }
    
    /// List all sessions
    pub fn list_sessions(&self) -> Result<Vec<SessionMetadata>> {
        let mut sessions = Vec::new();
        
        for entry in fs::read_dir(&self.sessions_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("nrs") {
                if let Ok(metadata) = self.get_session_metadata(&path) {
                    sessions.push(metadata);
                }
            }
        }
        
        // Sort by updated_at descending
        sessions.sort_by(|a, b| b.updated_at.cmp(&a.updated_at));
        
        Ok(sessions)
    }
    
    /// Get session metadata without loading full state
    fn get_session_metadata(&self, path: &Path) -> Result<SessionMetadata> {
        let json = fs::read_to_string(path)?;
        let nrs_file: NrsFile = serde_json::from_str(&json)?;
        
        Ok(SessionMetadata {
            id: nrs_file.session.id,
            name: nrs_file.session.name,
            status: nrs_file.session.status,
            mode: nrs_file.session.mode,
            created_at: nrs_file.session.created_at,
            updated_at: nrs_file.session.updated_at,
            task_count: nrs_file.session.task_queue.len(),
            finding_count: nrs_file.session.findings.len(),
        })
    }
    
    /// Delete a session
    pub fn delete_session(&self, session_id: &str) -> Result<()> {
        let filename = format!("{}.nrs", session_id);
        let path = self.sessions_dir.join(&filename);
        
        fs::remove_file(&path)
            .context("Failed to delete session file")?;
        
        tracing::info!("Session deleted: {}", session_id);
        Ok(())
    }
    
    /// Export session to a specific path
    pub fn export_session(&self, session_id: &str, dest_path: impl AsRef<Path>) -> Result<()> {
        let filename = format!("{}.nrs", session_id);
        let src_path = self.sessions_dir.join(&filename);
        
        fs::copy(&src_path, dest_path.as_ref())
            .context("Failed to export session")?;
        
        tracing::info!("Session exported: {} -> {}", session_id, dest_path.as_ref().display());
        Ok(())
    }

    /// Export session to default exports directory
    pub fn export_session_auto(&self, session_id: &str) -> Result<PathBuf> {
        let exports_dir = self.sessions_dir.parent()
            .unwrap_or_else(|| Path::new("."))
            .join("exports");
            
        fs::create_dir_all(&exports_dir).context("Failed to create exports directory")?;
        
        let filename = format!("{}_{}.nrs", session_id, Utc::now().format("%Y%m%d_%H%M%S"));
        let dest_path = exports_dir.join(&filename);
        
        self.export_session(session_id, &dest_path)?;
        
        Ok(dest_path)
    }
}

/// Session metadata for listing
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionMetadata {
    pub id: String,
    pub name: String,
    pub status: crate::state::SessionStatus,
    pub mode: crate::state::OperationalMode,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub task_count: usize,
    pub finding_count: usize,
}
