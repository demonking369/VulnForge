use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use std::collections::{HashMap, VecDeque};
use uuid::Uuid;

/// Operational mode for NeuroRift
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "UPPERCASE")]
pub enum OperationalMode {
    Offensive,
    Defensive,
}

/// Session status states
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum SessionStatus {
    Active,
    Paused,
    Completed,
    Failed,
}

/// Agent types in NeuroRift
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum AgentType {
    Planner,
    Operator,
    Navigator,
    Analyst,
    Scribe,
}

/// Agent status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentStatus {
    pub agent: AgentType,
    pub state: AgentState,
    pub current_task: Option<String>,
    pub last_update: DateTime<Utc>,
}

/// Agent state
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum AgentState {
    Idle,
    Planning,
    Executing,
    Analyzing,
    Writing,
    WaitingApproval,
    Error,
}

/// Task in the execution queue
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub tool_name: String,
    pub target: String,
    pub args: HashMap<String, serde_json::Value>,
    pub status: TaskStatus,
    pub created_at: DateTime<Utc>,
    pub started_at: Option<DateTime<Utc>>,
    pub completed_at: Option<DateTime<Utc>>,
}

/// Task status
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum TaskStatus {
    Queued,
    Running,
    Completed,
    Failed,
    Cancelled,
}

/// Approval request for human-in-the-loop
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApprovalRequest {
    pub id: String,
    pub action: Action,
    pub reason: String,
    pub created_at: DateTime<Utc>,
    pub status: ApprovalStatus,
}

/// Action requiring approval
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Action {
    pub action_type: ActionType,
    pub description: String,
    pub risk_level: RiskLevel,
    pub details: serde_json::Value,
}

/// Action type
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ActionType {
    ToolExecution,
    BrowserNavigation,
    FormSubmission,
    FileWrite,
    RootCommand,
}

/// Risk level
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "UPPERCASE")]
pub enum RiskLevel {
    Low,
    Medium,
    High,
    Critical,
}

/// Approval status
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum ApprovalStatus {
    Pending,
    Approved,
    Denied,
}

/// Security finding
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Finding {
    pub id: String,
    pub title: String,
    pub severity: Severity,
    pub description: String,
    pub tool_source: String,
    pub discovered_at: DateTime<Utc>,
    pub details: serde_json::Value,
}

/// Severity level
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "UPPERCASE")]
pub enum Severity {
    Info,
    Low,
    Medium,
    High,
    Critical,
}

/// Artifact generated during session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Artifact {
    pub id: String,
    pub artifact_type: ArtifactType,
    pub name: String,
    pub path: String,
    pub created_at: DateTime<Utc>,
    pub metadata: HashMap<String, String>,
}

/// Artifact type
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ArtifactType {
    Report,
    Screenshot,
    Log,
    Data,
    Other,
}

/// Complete session state
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionState {
    pub id: String,
    pub name: String,
    pub status: SessionStatus,
    pub mode: OperationalMode,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub task_queue: VecDeque<Task>,
    pub approval_queue: VecDeque<ApprovalRequest>,
    pub agent_states: HashMap<AgentType, AgentStatus>,
    pub findings: Vec<Finding>,
    pub artifacts: Vec<Artifact>,
    pub metadata: HashMap<String, String>,
}

impl SessionState {
    /// Create a new session
    pub fn new(name: String, mode: OperationalMode) -> Self {
        let now = Utc::now();
        let id = format!("session_{}", Uuid::new_v4().to_string().replace("-", "")[..12].to_string());
        
        let mut agent_states = HashMap::new();
        for agent in [AgentType::Planner, AgentType::Operator, AgentType::Navigator, AgentType::Analyst, AgentType::Scribe] {
            agent_states.insert(agent, AgentStatus {
                agent,
                state: AgentState::Idle,
                current_task: None,
                last_update: now,
            });
        }
        
        Self {
            id,
            name,
            status: SessionStatus::Active,
            mode,
            created_at: now,
            updated_at: now,
            task_queue: VecDeque::new(),
            approval_queue: VecDeque::new(),
            agent_states,
            findings: Vec::new(),
            artifacts: Vec::new(),
            metadata: HashMap::new(),
        }
    }
    
    /// Update the session timestamp
    pub fn touch(&mut self) {
        self.updated_at = Utc::now();
    }
    
    /// Add a task to the queue
    pub fn queue_task(&mut self, tool_name: String, target: String, args: HashMap<String, serde_json::Value>) {
        let task = Task {
            id: format!("task_{}", Uuid::new_v4().to_string().replace("-", "")[..8].to_string()),
            tool_name,
            target,
            args,
            status: TaskStatus::Queued,
            created_at: Utc::now(),
            started_at: None,
            completed_at: None,
        };
        
        self.task_queue.push_back(task);
        self.touch();
    }
    
    /// Add an approval request
    pub fn request_approval(&mut self, action: Action, reason: String) -> String {
        let approval = ApprovalRequest {
            id: format!("approval_{}", Uuid::new_v4().to_string().replace("-", "")[..8].to_string()),
            action,
            reason,
            created_at: Utc::now(),
            status: ApprovalStatus::Pending,
        };
        
        let id = approval.id.clone();
        self.approval_queue.push_back(approval);
        self.touch();
        id
    }
    
    /// Add a finding
    pub fn add_finding(&mut self, title: String, severity: Severity, description: String, tool_source: String, details: serde_json::Value) {
        let finding = Finding {
            id: format!("finding_{}", Uuid::new_v4().to_string().replace("-", "")[..8].to_string()),
            title,
            severity,
            description,
            tool_source,
            discovered_at: Utc::now(),
            details,
        };
        
        self.findings.push(finding);
        self.touch();
    }
}
