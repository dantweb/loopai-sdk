# Real-Time Monitoring - Live Cycle Tracking

**Date:** November 19, 2025
**Component:** Monitoring System
**Status:** Design Proposal

---

## Overview

This document details the real-time monitoring system for tracking cycle executions, agent statuses, and system health with live updates via Socket.IO.

---

## Monitoring Components

```
Frontend (AgentLifeMonitor.vue)
├── CycleProgressView - Overall cycle progress
├── AgentStatusDashboard - Per-agent status
├── ExecutionLogsViewer - Real-time logs
└── PerformanceMetrics - System health

Backend (StatusAggregator Service)
├── Cycle execution tracking
├── Agent status collection
├── Log aggregation
└── Socket.IO event broadcasting

Database (CycleExecutionLog)
└── Persistent log storage
```

---

## Socket.IO Event Architecture

### Event Flow

```
Agent Execution → ActionOrchestrator → StatusAggregator → Socket.IO → Frontend
                                              ↓
                                        Database (logs)
```

### Client Events (Frontend → Backend)

```javascript
// Subscribe to cycle updates
socket.emit('subscribe_cycle_updates', {
  execution_id: 'abc123',
  user_id: 1
});

// Unsubscribe from cycle updates
socket.emit('unsubscribe_cycle_updates', {
  execution_id: 'abc123'
});

// Subscribe to agent statuses
socket.emit('subscribe_agent_statuses', {
  agent_ids: ['FRBG/agent1', 'FRBG/agent2'],
  user_id: 1
});
```

### Server Events (Backend → Frontend)

```javascript
// Cycle status changed
socket.on('cycle_status_update', (data) => {
  // data: { execution_id, status, timestamp }
});

// Agent action started
socket.on('agent_action_started', (data) => {
  // data: { agent_id, action_name, execution_id, timestamp }
});

// Agent action completed
socket.on('agent_action_completed', (data) => {
  // data: { agent_id, action_name, success, duration_seconds, timestamp }
});

// Agent action failed
socket.on('agent_action_failed', (data) => {
  // data: { agent_id, action_name, error, timestamp }
});

// Cycle progress update
socket.on('cycle_progress_update', (data) => {
  // data: { execution_id, current_day, current_action, progress: {...} }
});

// Execution log entry
socket.on('execution_log_entry', (data) => {
  // data: { execution_id, level, message, timestamp, details }
});
```

---

## Frontend: AgentLifeMonitor.vue

```vue
<template>
  <div class="agent-life-monitor">
    <n-space vertical size="large">
      <!-- Execution Selector -->
      <n-select
        v-model:value="selectedExecutionId"
        :options="executionOptions"
        placeholder="Select running cycle to monitor"
        filterable
        @update:value="handleExecutionChange"
      />

      <!-- No selection state -->
      <n-empty
        v-if="!selectedExecutionId"
        description="Select a running cycle to monitor"
        style="margin-top: 100px"
      />

      <!-- Monitoring Dashboard -->
      <div v-else class="monitor-dashboard">
        <!-- Cycle Progress -->
        <cycle-progress-view
          :execution="currentExecution"
          :progress="progressData"
        />

        <!-- Agent Status Dashboard -->
        <agent-status-dashboard
          :agent-statuses="agentStatuses"
          :loading="loading"
        />

        <!-- Execution Logs -->
        <execution-logs-viewer
          :execution-id="selectedExecutionId"
          :logs="logs"
          :live="true"
        />

        <!-- Performance Metrics -->
        <performance-metrics
          :execution="currentExecution"
        />
      </div>
    </n-space>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, inject } from 'vue';
import { NSpace, NSelect, NEmpty, useMessage } from 'naive-ui';
import ApiService from '../api/ApiService';
import { useCycleMonitoring } from '../composables/useCycleMonitoring';

import CycleProgressView from './CycleProgressView.vue';
import AgentStatusDashboard from './AgentStatusDashboard.vue';
import ExecutionLogsViewer from './ExecutionLogsViewer.vue';
import PerformanceMetrics from './PerformanceMetrics.vue';

export default {
  name: 'AgentLifeMonitor',
  components: {
    NSpace,
    NSelect,
    NEmpty,
    CycleProgressView,
    AgentStatusDashboard,
    ExecutionLogsViewer,
    PerformanceMetrics
  },
  setup() {
    const message = useMessage();
    const socket = inject('socket');

    const selectedExecutionId = ref(null);
    const currentExecution = ref(null);
    const runningExecutions = ref([]);
    const agentStatuses = ref({});
    const progressData = ref(null);
    const logs = ref([]);
    const loading = ref(false);

    // Set up Socket.IO monitoring
    useCycleMonitoring(socket, {
      onCycleStatusUpdate: (data) => {
        if (data.execution_id === selectedExecutionId.value) {
          updateExecutionStatus(data);
        }
      },
      onAgentActionStarted: (data) => {
        updateAgentStatus(data.agent_id, {
          status: 'running',
          current_action: data.action_name,
          last_update: data.timestamp
        });
      },
      onAgentActionCompleted: (data) => {
        updateAgentStatus(data.agent_id, {
          status: 'completed',
          last_completed_action: data.action_name,
          last_update: data.timestamp
        });
      },
      onAgentActionFailed: (data) => {
        updateAgentStatus(data.agent_id, {
          status: 'failed',
          error: data.error,
          last_update: data.timestamp
        });
        message.error(`Agent ${data.agent_id} action failed: ${data.error}`);
      },
      onCycleProgressUpdate: (data) => {
        if (data.execution_id === selectedExecutionId.value) {
          progressData.value = data.progress;
        }
      },
      onExecutionLogEntry: (data) => {
        if (data.execution_id === selectedExecutionId.value) {
          logs.value.unshift(data);  // Add to top
          if (logs.value.length > 100) {
            logs.value.pop();  // Keep last 100 logs
          }
        }
      }
    });

    // Fetch running executions
    const fetchRunningExecutions = async () => {
      try {
        const response = await ApiService.getRunningExecutions();
        runningExecutions.value = response.executions || [];
      } catch (error) {
        message.error('Failed to load running executions');
      }
    };

    // Fetch execution details
    const fetchExecutionDetails = async (executionId) => {
      loading.value = true;
      try {
        const response = await ApiService.getCycleExecutionStatus(executionId);
        currentExecution.value = response.execution;
        progressData.value = response.execution.progress;

        // Initialize agent statuses
        const agents = response.execution.agents || [];
        agentStatuses.value = agents.reduce((acc, agent) => {
          acc[agent.agent_id] = agent;
          return acc;
        }, {});
      } catch (error) {
        message.error('Failed to load execution details');
      } finally {
        loading.value = false;
      }
    };

    // Fetch logs
    const fetchLogs = async (executionId) => {
      try {
        const response = await ApiService.getCycleExecutionLogs(executionId, {
          limit: 100,
          order: 'desc'
        });
        logs.value = response.logs || [];
      } catch (error) {
        message.error('Failed to load logs');
      }
    };

    // Update functions
    const updateExecutionStatus = (data) => {
      if (currentExecution.value) {
        Object.assign(currentExecution.value, data);
      }
    };

    const updateAgentStatus = (agentId, statusUpdate) => {
      if (!agentStatuses.value[agentId]) {
        agentStatuses.value[agentId] = { agent_id: agentId };
      }
      Object.assign(agentStatuses.value[agentId], statusUpdate);
    };

    // Handle execution change
    const handleExecutionChange = (executionId) => {
      if (!executionId) return;

      // Unsubscribe from previous execution
      if (selectedExecutionId.value && socket.value) {
        socket.value.emit('unsubscribe_cycle_updates', {
          execution_id: selectedExecutionId.value
        });
      }

      // Subscribe to new execution
      if (socket.value) {
        socket.value.emit('subscribe_cycle_updates', {
          execution_id: executionId
        });
      }

      // Fetch details
      fetchExecutionDetails(executionId);
      fetchLogs(executionId);
    };

    // Computed execution options
    const executionOptions = computed(() => {
      return runningExecutions.value.map(exec => ({
        label: `${exec.configuration_name} (Day ${exec.current_day}/${exec.total_days})`,
        value: exec.id
      }));
    });

    onMounted(() => {
      fetchRunningExecutions();
    });

    return {
      selectedExecutionId,
      currentExecution,
      executionOptions,
      agentStatuses,
      progressData,
      logs,
      loading,
      handleExecutionChange
    };
  }
};
</script>

<style scoped>
.monitor-dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.monitor-dashboard > * {
  grid-column: span 2;
}

@media (min-width: 1200px) {
  .monitor-dashboard > .cycle-progress-view {
    grid-column: span 1;
  }
  .monitor-dashboard > .agent-status-dashboard {
    grid-column: span 1;
  }
}
</style>
```

---

## Component: CycleProgressView.vue

```vue
<template>
  <n-card title="Cycle Progress" class="cycle-progress-view">
    <n-space vertical>
      <!-- Overall Progress Bar -->
      <div>
        <n-space justify="space-between">
          <span>Overall Progress</span>
          <span>{{ progress?.percentage.toFixed(1) }}%</span>
        </n-space>
        <n-progress
          type="line"
          :percentage="progress?.percentage || 0"
          :status="getProgressStatus()"
          :height="20"
          style="margin-top: 10px"
        />
      </div>

      <!-- Day Progress -->
      <n-grid :cols="2" :x-gap="12">
        <n-grid-item>
          <n-statistic label="Current Day">
            <template #default>
              {{ execution?.current_day }} / {{ execution?.total_days }}
            </template>
          </n-statistic>
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="Current Action">
            <template #default>
              <n-tag :type="getActionTagType()">
                {{ execution?.current_action || 'Waiting' }}
              </n-tag>
            </template>
          </n-statistic>
        </n-grid-item>
      </n-grid>

      <!-- Action Statistics -->
      <n-grid :cols="4" :x-gap="12">
        <n-grid-item>
          <n-statistic label="Total Actions" :value="progress?.total_actions || 0" />
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="Completed" :value="progress?.completed_actions || 0">
            <template #suffix>
              <n-icon color="green"><CheckCircleIcon /></n-icon>
            </template>
          </n-statistic>
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="Failed" :value="progress?.failed_actions || 0">
            <template #suffix>
              <n-icon color="red"><CloseCircleIcon /></n-icon>
            </template>
          </n-statistic>
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="Success Rate">
            <template #default>
              {{ progress?.success_rate.toFixed(1) }}%
            </template>
          </n-statistic>
        </n-grid-item>
      </n-grid>

      <!-- Timing Information -->
      <n-descriptions :column="2" bordered>
        <n-descriptions-item label="Started At">
          {{ formatTimestamp(execution?.timing?.started_at) }}
        </n-descriptions-item>
        <n-descriptions-item label="Elapsed Time">
          {{ formatDuration(execution?.timing?.elapsed_seconds) }}
        </n-descriptions-item>
        <n-descriptions-item label="Estimated Remaining">
          {{ formatDuration(execution?.timing?.estimated_remaining_seconds) }}
        </n-descriptions-item>
        <n-descriptions-item label="Est. Completion">
          {{ formatTimestamp(execution?.timing?.estimated_completion) }}
        </n-descriptions-item>
      </n-descriptions>
    </n-space>
  </n-card>
</template>

<script>
import { computed } from 'vue';
import { NCard, NSpace, NProgress, NGrid, NGridItem, NStatistic, NTag, NIcon, NDescriptions, NDescriptionsItem } from 'naive-ui';
import { CheckmarkCircle as CheckCircleIcon, CloseCircle as CloseCircleIcon } from '@vicons/ionicons5';

export default {
  name: 'CycleProgressView',
  components: {
    NCard, NSpace, NProgress, NGrid, NGridItem, NStatistic,
    NTag, NIcon, NDescriptions, NDescriptionsItem,
    CheckCircleIcon, CloseCircleIcon
  },
  props: {
    execution: {
      type: Object,
      required: true
    },
    progress: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const getProgressStatus = () => {
      if (props.execution?.status === 'failed') return 'error';
      if (props.execution?.status === 'completed') return 'success';
      if (props.progress?.success_rate < 80) return 'warning';
      return 'info';
    };

    const getActionTagType = () => {
      if (!props.execution?.current_action) return 'default';
      return 'info';
    };

    const formatTimestamp = (timestamp) => {
      if (!timestamp) return 'N/A';
      return new Date(timestamp).toLocaleString();
    };

    const formatDuration = (seconds) => {
      if (!seconds) return 'N/A';
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${hours}h ${minutes}m ${secs}s`;
    };

    return {
      getProgressStatus,
      getActionTagType,
      formatTimestamp,
      formatDuration
    };
  }
};
</script>
```

---

## Component: AgentStatusDashboard.vue

```vue
<template>
  <n-card title="Agent Status" class="agent-status-dashboard">
    <n-space vertical>
      <n-grid :cols="2" :x-gap="12" :y-gap="12">
        <n-grid-item v-for="(status, agentId) in agentStatuses" :key="agentId">
          <n-card size="small" :title="agentId">
            <template #header-extra>
              <n-tag :type="getStatusTagType(status.status)">
                {{ status.status || 'unknown' }}
              </n-tag>
            </template>

            <n-space vertical size="small">
              <!-- Current Action -->
              <div v-if="status.current_action">
                <strong>Current Action:</strong> {{ status.current_action }}
              </div>

              <!-- Last Completed Action -->
              <div v-if="status.last_completed_action">
                <strong>Last Completed:</strong> {{ status.last_completed_action }}
              </div>

              <!-- Statistics -->
              <n-grid :cols="2" :x-gap="8">
                <n-grid-item>
                  <n-statistic label="Completed" :value="status.actions_completed || 0" />
                </n-grid-item>
                <n-grid-item>
                  <n-statistic label="Failed" :value="status.actions_failed || 0" />
                </n-grid-item>
              </n-grid>

              <!-- Error Message -->
              <n-alert v-if="status.error" type="error" size="small">
                {{ status.error }}
              </n-alert>

              <!-- Last Update -->
              <div style="font-size: 12px; color: #999;">
                Last update: {{ formatTimestamp(status.last_update) }}
              </div>
            </n-space>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- Empty State -->
      <n-empty
        v-if="Object.keys(agentStatuses).length === 0"
        description="No agent data available"
      />
    </n-space>
  </n-card>
</template>

<script>
import { NCard, NSpace, NGrid, NGridItem, NTag, NStatistic, NAlert, NEmpty } from 'naive-ui';

export default {
  name: 'AgentStatusDashboard',
  components: {
    NCard, NSpace, NGrid, NGridItem, NTag, NStatistic, NAlert, NEmpty
  },
  props: {
    agentStatuses: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const getStatusTagType = (status) => {
      const statusMap = {
        'running': 'info',
        'completed': 'success',
        'failed': 'error',
        'waiting': 'default'
      };
      return statusMap[status] || 'default';
    };

    const formatTimestamp = (timestamp) => {
      if (!timestamp) return 'N/A';
      return new Date(timestamp).toLocaleString();
    };

    return {
      getStatusTagType,
      formatTimestamp
    };
  }
};
</script>
```

---

## Component: ExecutionLogsViewer.vue

```vue
<template>
  <n-card title="Execution Logs" class="execution-logs-viewer">
    <template #header-extra>
      <n-space>
        <!-- Level Filter -->
        <n-select
          v-model:value="levelFilter"
          :options="levelOptions"
          placeholder="Filter by level"
          clearable
          style="width: 150px"
        />

        <!-- Auto-scroll Toggle -->
        <n-switch v-model:value="autoScroll">
          <template #checked>Auto-scroll</template>
          <template #unchecked>Manual</template>
        </n-switch>

        <!-- Clear Button -->
        <n-button @click="clearLogs" size="small">
          Clear
        </n-button>
      </n-space>
    </template>

    <div ref="logContainer" class="log-container" @scroll="handleScroll">
      <div
        v-for="(log, index) in filteredLogs"
        :key="index"
        :class="['log-entry', `log-${log.level}`]"
      >
        <span class="log-timestamp">{{ formatTimestamp(log.timestamp) }}</span>
        <span class="log-level">{{ log.level }}</span>
        <span v-if="log.agent_id" class="log-agent">{{ log.agent_id }}</span>
        <span v-if="log.action_name" class="log-action">{{ log.action_name }}</span>
        <span class="log-message">{{ log.message }}</span>
        <pre v-if="log.details" class="log-details">{{ JSON.stringify(log.details, null, 2) }}</pre>
      </div>

      <!-- Empty State -->
      <n-empty v-if="filteredLogs.length === 0" description="No logs yet" />
    </div>
  </n-card>
</template>

<script>
import { ref, computed, watch, nextTick } from 'vue';
import { NCard, NSpace, NSelect, NSwitch, NButton, NEmpty } from 'naive-ui';

export default {
  name: 'ExecutionLogsViewer',
  components: {
    NCard, NSpace, NSelect, NSwitch, NButton, NEmpty
  },
  props: {
    executionId: {
      type: String,
      required: true
    },
    logs: {
      type: Array,
      required: true
    },
    live: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const logContainer = ref(null);
    const levelFilter = ref(null);
    const autoScroll = ref(true);
    const isUserScrolling = ref(false);

    const levelOptions = [
      { label: 'Debug', value: 'debug' },
      { label: 'Info', value: 'info' },
      { label: 'Warning', value: 'warning' },
      { label: 'Error', value: 'error' },
      { label: 'Critical', value: 'critical' }
    ];

    // Filtered logs
    const filteredLogs = computed(() => {
      let filtered = props.logs;

      if (levelFilter.value) {
        filtered = filtered.filter(log => log.level === levelFilter.value);
      }

      return filtered;
    });

    // Auto-scroll to bottom
    const scrollToBottom = () => {
      if (autoScroll.value && !isUserScrolling.value && logContainer.value) {
        nextTick(() => {
          logContainer.value.scrollTop = logContainer.value.scrollHeight;
        });
      }
    };

    // Handle manual scrolling
    const handleScroll = () => {
      if (!logContainer.value) return;

      const { scrollTop, scrollHeight, clientHeight } = logContainer.value;
      const isAtBottom = scrollHeight - scrollTop - clientHeight < 10;

      isUserScrolling.value = !isAtBottom;

      // Re-enable auto-scroll if user scrolls to bottom
      if (isAtBottom && !autoScroll.value) {
        autoScroll.value = true;
      }
    };

    // Clear logs
    const clearLogs = () => {
      props.logs.splice(0, props.logs.length);
    };

    // Format timestamp
    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString();
    };

    // Watch logs for changes and auto-scroll
    watch(() => props.logs.length, () => {
      scrollToBottom();
    });

    return {
      logContainer,
      levelFilter,
      autoScroll,
      levelOptions,
      filteredLogs,
      handleScroll,
      clearLogs,
      formatTimestamp
    };
  }
};
</script>

<style scoped>
.log-container {
  max-height: 500px;
  overflow-y: auto;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 10px;
  border-radius: 4px;
}

.log-entry {
  padding: 4px 0;
  border-bottom: 1px solid #333;
}

.log-timestamp {
  color: #858585;
  margin-right: 8px;
}

.log-level {
  padding: 2px 6px;
  border-radius: 3px;
  margin-right: 8px;
  font-weight: bold;
}

.log-debug { color: #858585; }
.log-info .log-level { background-color: #0e639c; color: white; }
.log-warning .log-level { background-color: #cd9731; color: white; }
.log-error .log-level { background-color: #f14c4c; color: white; }
.log-critical .log-level { background-color: #c80000; color: white; }

.log-agent {
  color: #4ec9b0;
  margin-right: 8px;
}

.log-action {
  color: #dcdcaa;
  margin-right: 8px;
}

.log-message {
  color: #d4d4d4;
}

.log-details {
  margin-top: 4px;
  padding: 8px;
  background-color: #262626;
  border-left: 3px solid #007acc;
  color: #ce9178;
  font-size: 11px;
  overflow-x: auto;
}
</style>
```

---

## Backend: StatusAggregator Service

```python
# loopai_src/web/services/status_aggregator.py

import logging
from datetime import datetime
from web.database import db
from web.admin_models.cycle_execution import CycleExecution
from web.admin_models.cycle_execution_log import CycleExecutionLog

logger = logging.getLogger(__name__)

class StatusAggregator:
    """Service for collecting and broadcasting execution status."""

    def __init__(self, socket_io):
        self.socket_io = socket_io

    def broadcast_cycle_status(self, execution_id, status_data):
        """Broadcast cycle status update."""
        self.socket_io.emit('cycle_status_update', {
            'execution_id': str(execution_id),
            'timestamp': datetime.utcnow().isoformat(),
            **status_data
        }, room=f'cycle_{execution_id}')

        logger.debug(f"Broadcasted cycle status for {execution_id}: {status_data}")

    def broadcast_agent_action_started(self, execution_id, agent_id, action_name):
        """Broadcast agent action started."""
        data = {
            'execution_id': str(execution_id),
            'agent_id': agent_id,
            'action_name': action_name,
            'timestamp': datetime.utcnow().isoformat()
        }

        self.socket_io.emit('agent_action_started', data, room=f'cycle_{execution_id}')
        self._log_execution(execution_id, 'info', agent_id, action_name, f"Action {action_name} started")

    def broadcast_agent_action_completed(self, execution_id, agent_id, action_name, duration_seconds):
        """Broadcast agent action completed."""
        data = {
            'execution_id': str(execution_id),
            'agent_id': agent_id,
            'action_name': action_name,
            'success': True,
            'duration_seconds': duration_seconds,
            'timestamp': datetime.utcnow().isoformat()
        }

        self.socket_io.emit('agent_action_completed', data, room=f'cycle_{execution_id}')
        self._log_execution(execution_id, 'info', agent_id, action_name, f"Action {action_name} completed in {duration_seconds}s")

    def broadcast_agent_action_failed(self, execution_id, agent_id, action_name, error):
        """Broadcast agent action failed."""
        data = {
            'execution_id': str(execution_id),
            'agent_id': agent_id,
            'action_name': action_name,
            'error': str(error),
            'timestamp': datetime.utcnow().isoformat()
        }

        self.socket_io.emit('agent_action_failed', data, room=f'cycle_{execution_id}')
        self._log_execution(execution_id, 'error', agent_id, action_name, f"Action {action_name} failed: {error}")

    def broadcast_progress_update(self, execution_id):
        """Broadcast cycle progress update."""
        execution = CycleExecution.query.get(execution_id)
        if not execution:
            return

        data = {
            'execution_id': str(execution_id),
            'current_day': execution.current_day,
            'current_action': execution.current_action_name,
            'progress': {
                'percentage': (execution.completed_actions / execution.total_actions * 100) if execution.total_actions > 0 else 0,
                'total_actions': execution.total_actions,
                'completed_actions': execution.completed_actions,
                'failed_actions': execution.failed_actions,
                'success_rate': ((execution.completed_actions / (execution.completed_actions + execution.failed_actions)) * 100) if (execution.completed_actions + execution.failed_actions) > 0 else 100
            },
            'timestamp': datetime.utcnow().isoformat()
        }

        self.socket_io.emit('cycle_progress_update', data, room=f'cycle_{execution_id}')

    def _log_execution(self, execution_id, level, agent_id, action_name, message, details=None):
        """Create execution log entry."""
        log = CycleExecutionLog(
            execution_id=execution_id,
            level=level,
            agent_id=agent_id,
            action_name=action_name,
            message=message,
            details=details
        )

        db.session.add(log)
        db.session.commit()

        # Broadcast log entry
        self.socket_io.emit('execution_log_entry', log.to_dict(), room=f'cycle_{execution_id}')
```

---

## Performance Considerations

### 1. Event Throttling
```python
from functools import wraps
import time

def throttle_event(seconds=1):
    """Throttle event emissions."""
    last_call = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = f"{func.__name__}_{args[0]}"  # First arg is usually execution_id

            if key not in last_call or now - last_call[key] >= seconds:
                last_call[key] = now
                return func(*args, **kwargs)

        return wrapper
    return decorator

# Usage
@throttle_event(seconds=1)
def broadcast_progress_update(self, execution_id):
    # Only emits once per second per execution
    ...
```

### 2. Database Optimizations
- Index on `execution_id` for log queries
- Limit log retention (delete old logs)
- Use database connection pooling
- Batch log inserts

### 3. Socket.IO Rooms
- Use rooms for targeted broadcasts
- Unsubscribe on disconnect
- Limit room size (max subscribers)

---

## Next Steps

1. Implement StatusAggregator service
2. Create monitoring frontend components
3. Add Socket.IO event handlers
4. Implement log storage and retrieval
5. Performance testing and optimization
6. Real-time dashboard testing

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related:** [00_OVERVIEW.md](./00_OVERVIEW.md), [03_FRONTEND_INTEGRATION.md](./03_FRONTEND_INTEGRATION.md)
