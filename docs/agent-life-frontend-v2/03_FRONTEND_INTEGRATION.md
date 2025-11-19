# Frontend Integration - Vue.js Implementation

**Date:** November 19, 2025
**Component:** Vue.js Frontend
**Status:** Design Proposal

---

## Overview

This document details the frontend implementation for the Agent Life v2 interface, including component structure, state management, real-time updates, and user experience patterns.

---

## Component Architecture

### Current Structure
```
AgentLife.vue (Single component)
└── Chat functionality only
```

### Proposed Structure
```
AgentLife.vue (Main container)
├── AgentLifeChat.vue (Refactored chat)
├── AgentLifeCycles.vue (Cycle management)
│   ├── CycleConfigForm.vue
│   ├── CycleList.vue
│   └── CycleControlPanel.vue
├── AgentLifeMonitor.vue (Real-time monitoring)
│   ├── CycleProgressView.vue
│   ├── AgentStatusDashboard.vue
│   └── ExecutionLogsViewer.vue
├── AgentLifeConstellations.vue (Action configuration)
│   ├── ConstellationDesigner.vue
│   ├── ConstellationList.vue
│   └── ConstellationPreview.vue
└── AgentLifeAnalytics.vue (Performance analytics)
    ├── CycleHistoryBrowser.vue
    ├── PerformanceCharts.vue
    └── CollaborationInsights.vue
```

---

## Main Container: AgentLife.vue

### Refactored Implementation

```vue
<template>
  <div class="agent-life">
    <n-page-header title="Agent Life" />

    <n-tabs v-model:value="activeTab" type="line" animated>
      <!-- Chat Tab -->
      <n-tab-pane name="chat" tab="Chat">
        <agent-life-chat
          :agents="agents"
          :current-user-id="currentUserId"
          :socket="socket"
        />
      </n-tab-pane>

      <!-- Cycles Tab -->
      <n-tab-pane name="cycles" tab="Cycles">
        <agent-life-cycles
          :agents="agents"
          :current-user-id="currentUserId"
        />
      </n-tab-pane>

      <!-- Monitor Tab -->
      <n-tab-pane name="monitor" tab="Monitor">
        <agent-life-monitor
          :socket="socket"
        />
      </n-tab-pane>

      <!-- Constellations Tab -->
      <n-tab-pane name="constellations" tab="Constellations">
        <agent-life-constellations
          :current-user-id="currentUserId"
        />
      </n-tab-pane>

      <!-- Analytics Tab -->
      <n-tab-pane name="analytics" tab="Analytics">
        <agent-life-analytics
          :current-user-id="currentUserId"
        />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, provide } from 'vue';
import { useRouter } from 'vue-router';
import { io } from 'socket.io-client';
import { NPageHeader, NTabs, NTabPane } from 'naive-ui';
import ApiService from '../api/ApiService';
import AgentModel from '../models/AgentModel';

// Child components
import AgentLifeChat from './AgentLifeChat.vue';
import AgentLifeCycles from './AgentLifeCycles.vue';
import AgentLifeMonitor from './AgentLifeMonitor.vue';
import AgentLifeConstellations from './AgentLifeConstellations.vue';
import AgentLifeAnalytics from './AgentLifeAnalytics.vue';

export default {
  name: 'AgentLife',
  components: {
    NPageHeader,
    NTabs,
    NTabPane,
    AgentLifeChat,
    AgentLifeCycles,
    AgentLifeMonitor,
    AgentLifeConstellations,
    AgentLifeAnalytics
  },
  setup() {
    const router = useRouter();
    const activeTab = ref('chat');
    const agents = ref([]);
    const socket = ref(null);
    const currentUserId = ref(localStorage.getItem('current-user-id'));

    // Fetch agents on mount
    const fetchAgents = async () => {
      try {
        const res = await AgentModel.loadAll();
        agents.value = res.filter(a => a.user_id == currentUserId.value);
      } catch (err) {
        console.error('Error fetching agents:', err);
      }
    };

    // Initialize Socket.IO
    const initSocket = () => {
      const token = localStorage.getItem('user-token');
      const API_BASE_HOST = process.env.VUE_APP_API_BASE_HOST || 'http://localhost:5000/api';

      socket.value = io(API_BASE_HOST, {
        auth: { token },
        transports: ['polling'],
        withCredentials: true
      });

      socket.value.on('connect', () => {
        console.log('Socket connected');
        // Subscribe to user-specific events
        socket.value.emit('subscribe_agentlife', { user_id: currentUserId.value });
      });

      socket.value.on('disconnect', () => {
        console.log('Socket disconnected');
      });
    };

    // Provide shared state to children
    provide('agents', agents);
    provide('socket', socket);
    provide('currentUserId', currentUserId);

    onMounted(async () => {
      if (!currentUserId.value) {
        router.push('/');
        return;
      }

      await fetchAgents();
      initSocket();
    });

    onBeforeUnmount(() => {
      if (socket.value) {
        socket.value.disconnect();
      }
    });

    return {
      activeTab,
      agents,
      socket,
      currentUserId
    };
  }
};
</script>

<style scoped>
.agent-life {
  padding: 20px;
}
</style>
```

---

## Cycle Management: AgentLifeCycles.vue

```vue
<template>
  <div class="agent-life-cycles">
    <n-space vertical size="large">
      <!-- Header with Create button -->
      <n-space justify="space-between">
        <h2>Cycle Management</h2>
        <n-button type="primary" @click="showCreateForm = true">
          <template #icon><n-icon><AddIcon /></n-icon></template>
          Create Cycle
        </n-button>
      </n-space>

      <!-- Filters -->
      <n-space>
        <n-select
          v-model:value="statusFilter"
          :options="statusOptions"
          placeholder="Filter by status"
          clearable
          style="width: 200px"
        />
        <n-input
          v-model:value="searchQuery"
          placeholder="Search cycles..."
          clearable
          style="width: 300px"
        >
          <template #prefix><n-icon><SearchIcon /></n-icon></template>
        </n-input>
      </n-space>

      <!-- Cycle List -->
      <cycle-list
        :cycles="filteredCycles"
        :loading="loading"
        @select="selectCycle"
        @start="startCycle"
        @edit="editCycle"
        @delete="deleteCycle"
      />

      <!-- Create/Edit Form Modal -->
      <n-modal
        v-model:show="showCreateForm"
        preset="card"
        title="Create Cycle Configuration"
        style="width: 800px"
      >
        <cycle-config-form
          :cycle="selectedCycle"
          :agents="agents"
          @submit="handleSubmit"
          @cancel="showCreateForm = false"
        />
      </n-modal>

      <!-- Control Panel (when cycle selected) -->
      <cycle-control-panel
        v-if="selectedCycle"
        :cycle="selectedCycle"
        @start="startCycle"
        @pause="pauseCycle"
        @resume="resumeCycle"
        @stop="stopCycle"
        @close="selectedCycle = null"
      />
    </n-space>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject } from 'vue';
import { NSpace, NButton, NSelect, NInput, NModal, NIcon, useMessage } from 'naive-ui';
import { Add as AddIcon, Search as SearchIcon } from '@vicons/ionicons5';
import ApiService from '../api/ApiService';

import CycleList from './CycleList.vue';
import CycleConfigForm from './CycleConfigForm.vue';
import CycleControlPanel from './CycleControlPanel.vue';

export default {
  name: 'AgentLifeCycles',
  components: {
    NSpace,
    NButton,
    NSelect,
    NInput,
    NModal,
    NIcon,
    CycleList,
    CycleConfigForm,
    CycleControlPanel,
    AddIcon,
    SearchIcon
  },
  setup() {
    const message = useMessage();
    const agents = inject('agents');
    const currentUserId = inject('currentUserId');

    const cycles = ref([]);
    const loading = ref(false);
    const showCreateForm = ref(false);
    const selectedCycle = ref(null);
    const statusFilter = ref(null);
    const searchQuery = ref('');

    const statusOptions = [
      { label: 'Draft', value: 'draft' },
      { label: 'Scheduled', value: 'scheduled' },
      { label: 'Running', value: 'active' },
      { label: 'Archived', value: 'archived' }
    ];

    // Computed filtered cycles
    const filteredCycles = computed(() => {
      let filtered = cycles.value;

      if (statusFilter.value) {
        filtered = filtered.filter(c => c.status === statusFilter.value);
      }

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(c =>
          c.name.toLowerCase().includes(query) ||
          (c.description && c.description.toLowerCase().includes(query))
        );
      }

      return filtered;
    });

    // Fetch cycles
    const fetchCycles = async () => {
      loading.value = true;
      try {
        const response = await ApiService.getCycles(currentUserId.value);
        cycles.value = response.cycles || [];
      } catch (error) {
        message.error('Failed to load cycles');
        console.error(error);
      } finally {
        loading.value = false;
      }
    };

    // Start cycle
    const startCycle = async (cycleId) => {
      try {
        const response = await ApiService.startCycle(cycleId);
        message.success(`Cycle started: ${response.execution.id}`);
        await fetchCycles();
      } catch (error) {
        message.error('Failed to start cycle');
        console.error(error);
      }
    };

    // Pause cycle
    const pauseCycle = async (executionId) => {
      try {
        await ApiService.pauseCycleExecution(executionId);
        message.success('Cycle paused');
        await fetchCycles();
      } catch (error) {
        message.error('Failed to pause cycle');
        console.error(error);
      }
    };

    // Resume cycle
    const resumeCycle = async (executionId) => {
      try {
        await ApiService.resumeCycleExecution(executionId);
        message.success('Cycle resumed');
        await fetchCycles();
      } catch (error) {
        message.error('Failed to resume cycle');
        console.error(error);
      }
    };

    // Stop cycle
    const stopCycle = async (executionId) => {
      try {
        await ApiService.stopCycleExecution(executionId);
        message.success('Cycle stopped');
        await fetchCycles();
      } catch (error) {
        message.error('Failed to stop cycle');
        console.error(error);
      }
    };

    // Handle form submit
    const handleSubmit = async (cycleData) => {
      try {
        if (selectedCycle.value) {
          await ApiService.updateCycle(selectedCycle.value.id, cycleData);
          message.success('Cycle updated');
        } else {
          await ApiService.createCycle(cycleData);
          message.success('Cycle created');
        }
        showCreateForm.value = false;
        selectedCycle.value = null;
        await fetchCycles();
      } catch (error) {
        message.error('Failed to save cycle');
        console.error(error);
      }
    };

    // Select cycle for viewing/editing
    const selectCycle = (cycle) => {
      selectedCycle.value = cycle;
    };

    // Edit cycle
    const editCycle = (cycle) => {
      selectedCycle.value = cycle;
      showCreateForm.value = true;
    };

    // Delete cycle
    const deleteCycle = async (cycleId) => {
      try {
        await ApiService.deleteCycle(cycleId);
        message.success('Cycle deleted');
        await fetchCycles();
      } catch (error) {
        message.error('Failed to delete cycle');
        console.error(error);
      }
    };

    onMounted(() => {
      fetchCycles();
    });

    return {
      cycles,
      filteredCycles,
      loading,
      showCreateForm,
      selectedCycle,
      statusFilter,
      searchQuery,
      statusOptions,
      agents,
      startCycle,
      pauseCycle,
      resumeCycle,
      stopCycle,
      handleSubmit,
      selectCycle,
      editCycle,
      deleteCycle
    };
  }
};
</script>
```

---

## API Service Extensions

```javascript
// src/api/ApiService.js (extensions)

class ApiService {
  // ... existing methods ...

  // Cycle Management
  async getCycles(userId, params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.get(`/api/agentlife/cycles/?${query}`);
  }

  async getCycle(cycleId) {
    return this.get(`/api/agentlife/cycles/${cycleId}/`);
  }

  async createCycle(cycleData) {
    return this.post('/api/agentlife/cycles/', cycleData);
  }

  async updateCycle(cycleId, cycleData) {
    return this.put(`/api/agentlife/cycles/${cycleId}/`, cycleData);
  }

  async deleteCycle(cycleId) {
    return this.delete(`/api/agentlife/cycles/${cycleId}/`);
  }

  async cloneCycle(cycleId, overrides = {}) {
    return this.post(`/api/agentlife/cycles/${cycleId}/clone/`, overrides);
  }

  // Cycle Execution Control
  async startCycle(cycleId, options = {}) {
    return this.post(`/api/agentlife/cycles/${cycleId}/start/`, options);
  }

  async pauseCycleExecution(executionId) {
    return this.post(`/api/agentlife/cycles/executions/${executionId}/pause/`);
  }

  async resumeCycleExecution(executionId) {
    return this.post(`/api/agentlife/cycles/executions/${executionId}/resume/`);
  }

  async stopCycleExecution(executionId, options = {}) {
    return this.post(`/api/agentlife/cycles/executions/${executionId}/stop/`, options);
  }

  async getCycleExecutionStatus(executionId) {
    return this.get(`/api/agentlife/cycles/executions/${executionId}/status/`);
  }

  async getCycleExecutionLogs(executionId, params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.get(`/api/agentlife/cycles/executions/${executionId}/logs/?${query}`);
  }

  // Action Constellations
  async getConstellations(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.get(`/api/agentlife/constellations/?${query}`);
  }

  async getConstellation(constellationId) {
    return this.get(`/api/agentlife/constellations/${constellationId}/`);
  }

  async createConstellation(constellationData) {
    return this.post('/api/agentlife/constellations/', constellationData);
  }

  async updateConstellation(constellationId, constellationData) {
    return this.put(`/api/agentlife/constellations/${constellationId}/`, constellationData);
  }

  async deleteConstellation(constellationId) {
    return this.delete(`/api/agentlife/constellations/${constellationId}/`);
  }

  async validateConstellation(sequence) {
    return this.post('/api/agentlife/constellations/validate/', { sequence });
  }

  // Monitoring & Analytics
  async getAgentStatuses() {
    return this.get('/api/agentlife/agents/status/');
  }

  async getDashboardSummary(userId) {
    return this.get(`/api/agentlife/dashboard/?user_id=${userId}`);
  }

  async getCycleAnalytics(cycleId) {
    return this.get(`/api/agentlife/cycles/${cycleId}/analytics/`);
  }
}

export default new ApiService();
```

---

## State Management with Pinia

```javascript
// src/stores/agentLifeStore.js

import { defineStore } from 'pinia';
import ApiService from '../api/ApiService';

export const useAgentLifeStore = defineStore('agentLife', {
  state: () => ({
    cycles: [],
    runningExecutions: new Map(),
    constellations: [],
    agentStatuses: new Map(),
    loading: false,
    error: null
  }),

  getters: {
    activeCycles: (state) => state.cycles.filter(c => c.status === 'active'),
    draftCycles: (state) => state.cycles.filter(c => c.status === 'draft'),
    presetConstellations: (state) => state.constellations.filter(c => c.is_preset),

    getCycleById: (state) => (id) => state.cycles.find(c => c.id === id),
    getConstellationById: (state) => (id) => state.constellations.find(c => c.id === id),
    getExecutionStatus: (state) => (id) => state.runningExecutions.get(id),
    getAgentStatus: (state) => (agentId) => state.agentStatuses.get(agentId)
  },

  actions: {
    async fetchCycles(userId) {
      this.loading = true;
      try {
        const response = await ApiService.getCycles(userId);
        this.cycles = response.cycles || [];
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchConstellations() {
      this.loading = true;
      try {
        const response = await ApiService.getConstellations();
        this.constellations = response.constellations || [];
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async startCycle(cycleId) {
      const response = await ApiService.startCycle(cycleId);
      this.runningExecutions.set(response.execution.id, response.execution);
      return response.execution;
    },

    updateExecutionStatus(executionId, status) {
      const execution = this.runningExecutions.get(executionId);
      if (execution) {
        Object.assign(execution, status);
      }
    },

    updateAgentStatus(agentId, status) {
      this.agentStatuses.set(agentId, status);
    }
  }
});
```

---

## Socket.IO Event Handlers

```javascript
// src/composables/useCycleMonitoring.js

import { onMounted, onBeforeUnmount } from 'vue';
import { useAgentLifeStore } from '../stores/agentLifeStore';

export function useCycleMonitoring(socket) {
  const store = useAgentLifeStore();

  const setupListeners = () => {
    if (!socket.value) return;

    // Cycle status updates
    socket.value.on('cycle_status_update', (data) => {
      console.log('Cycle status update:', data);
      store.updateExecutionStatus(data.execution_id, {
        status: data.status,
        ...data
      });
    });

    // Agent action started
    socket.value.on('agent_action_started', (data) => {
      console.log('Agent action started:', data);
      store.updateAgentStatus(data.agent_id, {
        current_action: data.action_name,
        status: 'running',
        last_update: data.timestamp
      });
    });

    // Agent action completed
    socket.value.on('agent_action_completed', (data) => {
      console.log('Agent action completed:', data);
      store.updateAgentStatus(data.agent_id, {
        current_action: null,
        status: 'waiting',
        last_update: data.timestamp,
        last_completed_action: data.action_name
      });
    });

    // Agent action failed
    socket.value.on('agent_action_failed', (data) => {
      console.error('Agent action failed:', data);
      store.updateAgentStatus(data.agent_id, {
        current_action: null,
        status: 'failed',
        last_update: data.timestamp,
        error: data.error
      });
    });

    // Cycle progress update
    socket.value.on('cycle_progress_update', (data) => {
      store.updateExecutionStatus(data.execution_id, {
        current_day: data.current_day,
        current_action: data.current_action,
        progress: data.progress
      });
    });

    // Execution log entry
    socket.value.on('execution_log_entry', (data) => {
      // Handle in log viewer component
      console.log('Log entry:', data);
    });
  };

  const cleanupListeners = () => {
    if (!socket.value) return;

    socket.value.off('cycle_status_update');
    socket.value.off('agent_action_started');
    socket.value.off('agent_action_completed');
    socket.value.off('agent_action_failed');
    socket.value.off('cycle_progress_update');
    socket.value.off('execution_log_entry');
  };

  onMounted(() => {
    setupListeners();
  });

  onBeforeUnmount(() => {
    cleanupListeners();
  });

  return {
    setupListeners,
    cleanupListeners
  };
}
```

---

## Responsive Design

### Mobile Layout
- Collapsible filters
- Stacked cards instead of table
- Bottom sheet for control panels
- Simplified action constellation designer
- Touch-friendly controls

### Tablet Layout
- Side-by-side panels
- Responsive grid layout
- Modal overlays for forms
- Optimized touch targets

### Desktop Layout
- Full featured interface
- Multi-column layouts
- Advanced visual editors
- Keyboard shortcuts

---

## Performance Optimization

### 1. Lazy Loading
```javascript
// Lazy load heavy components
const AgentLifeConstellations = defineAsyncComponent(() =>
  import('./AgentLifeConstellations.vue')
);
```

### 2. Virtual Scrolling
```vue
<!-- For large lists -->
<n-virtual-list
  :items="cycles"
  :item-size="80"
  style="max-height: 600px"
>
  <template #default="{ item }">
    <cycle-card :cycle="item" />
  </template>
</n-virtual-list>
```

### 3. Debouncing
```javascript
import { useDebounceFn } from '@vueuse/core';

const debouncedSearch = useDebounceFn((query) => {
  searchQuery.value = query;
}, 300);
```

### 4. Memoization
```javascript
const expensiveComputation = computed(() => {
  // Cache expensive calculations
  return cycles.value.map(c => calculateMetrics(c));
});
```

---

## Accessibility

### ARIA Labels
```vue
<n-button
  aria-label="Start cycle"
  @click="startCycle"
>
  Start
</n-button>
```

### Keyboard Navigation
```vue
<div
  tabindex="0"
  @keydown.enter="selectCycle"
  @keydown.space="selectCycle"
>
  {{ cycle.name }}
</div>
```

### Screen Reader Support
```vue
<div role="status" aria-live="polite">
  {{ statusMessage }}
</div>
```

---

## Testing Strategy

### Unit Tests (Vitest)
```javascript
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import AgentLifeCycles from './AgentLifeCycles.vue';

describe('AgentLifeCycles', () => {
  it('renders cycle list', () => {
    const wrapper = mount(AgentLifeCycles, {
      props: { agents: [] }
    });
    expect(wrapper.find('.agent-life-cycles').exists()).toBe(true);
  });

  it('filters cycles by status', async () => {
    const wrapper = mount(AgentLifeCycles);
    await wrapper.vm.statusFilter = 'draft';
    expect(wrapper.vm.filteredCycles.length).toBeGreaterThan(0);
  });
});
```

### Integration Tests (Cypress)
```javascript
describe('Cycle Management', () => {
  it('creates a new cycle', () => {
    cy.visit('/agent-life');
    cy.get('[data-cy=create-cycle-btn]').click();
    cy.get('[data-cy=cycle-name-input]').type('Test Cycle');
    cy.get('[data-cy=submit-btn]').click();
    cy.contains('Cycle created').should('be.visible');
  });
});
```

---

## Next Steps

1. Set up Pinia store
2. Create base components (CycleList, CycleCard, etc.)
3. Implement API service methods
4. Build main container with tabs
5. Develop cycle management components
6. Add Socket.IO event handlers
7. Implement monitoring components
8. Build analytics components
9. Testing and refinement

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related:** [00_OVERVIEW.md](./00_OVERVIEW.md), [04_BACKEND_INTEGRATION.md](./04_BACKEND_INTEGRATION.md)
