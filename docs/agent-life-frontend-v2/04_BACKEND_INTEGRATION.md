# Backend Integration - Flask API Implementation

**Date:** November 19, 2025
**Component:** Flask Backend
**Status:** Design Proposal

---

## Overview

This document details the backend implementation for Agent Life v2, including Flask routes, service layer architecture, database models, Socket.IO events, and background task orchestration.

---

## Current Backend Structure

### agentlife.py (Current Implementation)
```python
# 3 basic endpoints:
/api/agentlife/fetch_new_messages/<user_id>/  # GET messages
/api/agentlife/send_message/                  # POST message
/api/agentlife/assign_task/                   # POST task assignment
```

**Limitations:**
- No cycle management
- No action configuration
- No monitoring or analytics
- No real-time status updates

---

## Proposed Backend Architecture

```
loopai_src/web/routes/agentlife.py (Enhanced routes)
├── Cycle Management Endpoints
├── Action Constellation Endpoints
├── Monitoring & Status Endpoints
└── Analytics Endpoints

loopai_src/web/services/
├── cycle_manager.py (New)
├── action_orchestrator.py (New)
├── status_aggregator.py (New)
└── constellation_manager.py (New)

loopai_src/web/admin_models/
├── cycle_configuration.py (New)
├── cycle_execution.py (New)
├── cycle_execution_log.py (New)
└── action_constellation.py (New)
```

---

## Database Models

### 1. CycleConfiguration Model

```python
# loopai_src/web/admin_models/cycle_configuration.py

from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import JSON, UUID, ENUM
from web.database import db

class CycleConfiguration(db.Model):
    """Configuration for agent cycles."""
    __tablename__ = 'cycle_configurations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Cycle parameters
    days = db.Column(db.Integer, nullable=False, default=1)
    agents = db.Column(JSON, nullable=False)  # List of agent addresses

    # Action constellation reference
    constellation_id = db.Column(UUID(as_uuid=True), db.ForeignKey('action_constellations.id'), nullable=False)

    # Timing configuration
    action_wait_seconds = db.Column(db.Integer, default=15)
    day_wait_seconds = db.Column(db.Integer, default=20)
    reflection_frequency_days = db.Column(db.Integer, default=5)

    # Scheduling
    scheduled_start = db.Column(db.DateTime, nullable=True)
    auto_repeat = db.Column(db.Boolean, default=False)
    repeat_interval_days = db.Column(db.Integer, nullable=True)

    # Metadata
    status = db.Column(ENUM('draft', 'scheduled', 'active', 'archived', name='cycle_status'), default='draft', index=True)
    is_preset = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    tags = db.Column(JSON, default=[])

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    executions = db.relationship('CycleExecution', back_populates='configuration', cascade='all, delete-orphan')
    constellation = db.relationship('ActionConstellation', back_populates='cycles')
    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self, include_executions=False):
        """Serialize to dictionary."""
        data = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'days': self.days,
            'agents': self.agents,
            'constellation_id': str(self.constellation_id),
            'timing': {
                'action_wait_seconds': self.action_wait_seconds,
                'day_wait_seconds': self.day_wait_seconds,
                'reflection_frequency_days': self.reflection_frequency_days
            },
            'scheduling': {
                'scheduled_start': self.scheduled_start.isoformat() if self.scheduled_start else None,
                'auto_repeat': self.auto_repeat,
                'repeat_interval_days': self.repeat_interval_days
            },
            'status': self.status,
            'is_preset': self.is_preset,
            'is_public': self.is_public,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_executions:
            data['executions'] = [e.to_dict() for e in self.executions]

        return data
```

### 2. CycleExecution Model

```python
# loopai_src/web/admin_models/cycle_execution.py

from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import JSON, UUID, ENUM
from web.database import db

class CycleExecution(db.Model):
    """Runtime execution state of a cycle."""
    __tablename__ = 'cycle_executions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    configuration_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cycle_configurations.id'), nullable=False, index=True)

    # Execution state
    status = db.Column(ENUM('queued', 'running', 'paused', 'completed', 'failed', 'stopped', name='execution_status'), default='queued', index=True)
    current_day = db.Column(db.Integer, default=1)
    total_days = db.Column(db.Integer, nullable=False)
    current_action_index = db.Column(db.Integer, default=0)
    current_action_name = db.Column(db.String(100), nullable=True)

    # Timestamps
    queued_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    started_at = db.Column(db.DateTime, nullable=True)
    paused_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    failed_at = db.Column(db.DateTime, nullable=True)

    # Progress metrics
    total_actions = db.Column(db.Integer, default=0)
    completed_actions = db.Column(db.Integer, default=0)
    failed_actions = db.Column(db.Integer, default=0)
    skipped_actions = db.Column(db.Integer, default=0)

    # Execution details
    agent_states = db.Column(JSON, default={})
    error_message = db.Column(db.Text, nullable=True)
    execution_metadata = db.Column(JSON, default={})

    # Relationships
    configuration = db.relationship('CycleConfiguration', back_populates='executions')
    logs = db.relationship('CycleExecutionLog', back_populates='execution', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self, include_logs=False):
        """Serialize to dictionary."""
        data = {
            'id': str(self.id),
            'configuration_id': str(self.configuration_id),
            'status': self.status,
            'current_day': self.current_day,
            'total_days': self.total_days,
            'current_action': self.current_action_name,
            'progress': {
                'percentage': (self.completed_actions / self.total_actions * 100) if self.total_actions > 0 else 0,
                'total_actions': self.total_actions,
                'completed_actions': self.completed_actions,
                'failed_actions': self.failed_actions,
                'skipped_actions': self.skipped_actions,
                'success_rate': ((self.completed_actions / (self.completed_actions + self.failed_actions)) * 100) if (self.completed_actions + self.failed_actions) > 0 else 100
            },
            'timing': {
                'queued_at': self.queued_at.isoformat() if self.queued_at else None,
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'paused_at': self.paused_at.isoformat() if self.paused_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
                'failed_at': self.failed_at.isoformat() if self.failed_at else None
            },
            'agent_states': self.agent_states,
            'error_message': self.error_message
        }

        if include_logs:
            data['logs'] = [log.to_dict() for log in self.logs.limit(100).all()]

        return data
```

### 3. ActionConstellation Model

```python
# loopai_src/web/admin_models/action_constellation.py

from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import JSON, UUID
from web.database import db

class ActionConstellation(db.Model):
    """Action sequence configurations."""
    __tablename__ = 'action_constellations'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL = system preset

    # Action sequence definition
    sequence = db.Column(JSON, nullable=False)

    # Metadata
    is_preset = db.Column(db.Boolean, default=False, index=True)
    is_public = db.Column(db.Boolean, default=False)
    tags = db.Column(JSON, default=[])
    version = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cycles = db.relationship('CycleConfiguration', back_populates='constellation')
    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self, include_usage=False):
        """Serialize to dictionary."""
        data = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'sequence': self.sequence,
            'is_preset': self.is_preset,
            'is_public': self.is_public,
            'tags': self.tags,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_usage:
            data['usage'] = {
                'cycles_using': len(self.cycles),
                'last_used': max((c.updated_at for c in self.cycles), default=None)
            }

        return data
```

---

## Service Layer

### 1. CycleManager Service

```python
# loopai_src/web/services/cycle_manager.py

import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from web.database import db
from web.admin_models.cycle_configuration import CycleConfiguration
from web.admin_models.cycle_execution import CycleExecution
from web.services.constellation_manager import ConstellationManager
from web.services.action_orchestrator import ActionOrchestrator

logger = logging.getLogger(__name__)

class CycleManager:
    """Service for managing cycle lifecycles."""

    def __init__(self, socket_io=None):
        self.socket_io = socket_io
        self.constellation_manager = ConstellationManager()
        self.orchestrator = ActionOrchestrator(socket_io)

    def create_cycle(self, user_id, cycle_data):
        """Create a new cycle configuration."""
        try:
            # Validate constellation exists
            constellation = self.constellation_manager.get_constellation(cycle_data['constellation_id'])
            if not constellation:
                raise ValueError("Invalid constellation_id")

            # Validate agents
            if not cycle_data.get('agents') or len(cycle_data['agents']) == 0:
                raise ValueError("At least one agent required")

            # Validate days
            days = cycle_data.get('days', 1)
            if not (1 <= days <= 30):
                raise ValueError("Days must be between 1 and 30")

            # Create cycle configuration
            cycle = CycleConfiguration(
                created_by=user_id,
                **cycle_data
            )

            db.session.add(cycle)
            db.session.commit()

            logger.info(f"Created cycle {cycle.id} for user {user_id}")
            return cycle

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database error creating cycle: {e}")
            raise ValueError("Database error creating cycle")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating cycle: {e}")
            raise

    def get_cycles(self, user_id, filters=None):
        """Get cycles for a user with optional filters."""
        query = CycleConfiguration.query.filter_by(created_by=user_id)

        if filters:
            if 'status' in filters:
                query = query.filter_by(status=filters['status'])
            if 'tags' in filters:
                query = query.filter(CycleConfiguration.tags.contains(filters['tags']))

        return query.order_by(CycleConfiguration.created_at.desc()).all()

    def get_cycle(self, cycle_id, user_id):
        """Get a specific cycle configuration."""
        cycle = CycleConfiguration.query.get_or_404(cycle_id)

        # Check permissions
        if cycle.created_by != user_id and not cycle.is_public:
            raise PermissionError("Not authorized to view this cycle")

        return cycle

    def update_cycle(self, cycle_id, user_id, cycle_data):
        """Update a cycle configuration."""
        cycle = CycleConfiguration.query.get_or_404(cycle_id)

        # Check permissions
        if cycle.created_by != user_id:
            raise PermissionError("Not authorized to modify this cycle")

        # Check if cycle is running
        active_execution = CycleExecution.query.filter_by(
            configuration_id=cycle_id,
            status='running'
        ).first()

        if active_execution:
            raise ValueError("Cannot modify a running cycle")

        # Update fields
        for key, value in cycle_data.items():
            if hasattr(cycle, key):
                setattr(cycle, key, value)

        cycle.updated_at = datetime.utcnow()
        db.session.commit()

        logger.info(f"Updated cycle {cycle_id}")
        return cycle

    def delete_cycle(self, cycle_id, user_id):
        """Delete a cycle configuration."""
        cycle = CycleConfiguration.query.get_or_404(cycle_id)

        # Check permissions
        if cycle.created_by != user_id:
            raise PermissionError("Not authorized to delete this cycle")

        # Check for running executions
        active_execution = CycleExecution.query.filter_by(
            configuration_id=cycle_id,
            status='running'
        ).first()

        if active_execution:
            raise ValueError("Cannot delete a cycle with running execution")

        db.session.delete(cycle)
        db.session.commit()

        logger.info(f"Deleted cycle {cycle_id}")

    def start_cycle(self, cycle_id, user_id, options=None):
        """Start a cycle execution."""
        cycle = self.get_cycle(cycle_id, user_id)

        # Create execution record
        execution = CycleExecution(
            configuration_id=cycle_id,
            total_days=cycle.days,
            status='queued'
        )

        # Calculate total actions
        constellation = cycle.constellation
        total_actions = self._calculate_total_actions(constellation.sequence, cycle.days)
        execution.total_actions = total_actions

        db.session.add(execution)
        db.session.commit()

        logger.info(f"Created execution {execution.id} for cycle {cycle_id}")

        # Queue for background execution
        self.orchestrator.queue_execution(execution.id)

        return execution

    def pause_execution(self, execution_id, user_id):
        """Pause a running cycle execution."""
        execution = CycleExecution.query.get_or_404(execution_id)

        # Check permissions
        if execution.configuration.created_by != user_id:
            raise PermissionError("Not authorized")

        # Check if pauseable
        if execution.status != 'running':
            raise ValueError(f"Cannot pause execution in status: {execution.status}")

        # Update status
        execution.status = 'paused'
        execution.paused_at = datetime.utcnow()
        db.session.commit()

        # Signal orchestrator
        self.orchestrator.pause_execution(execution_id)

        # Broadcast status update
        if self.socket_io:
            self.socket_io.emit('cycle_status_update', {
                'execution_id': str(execution_id),
                'status': 'paused'
            }, room=f'cycle_{execution_id}')

        logger.info(f"Paused execution {execution_id}")
        return execution

    def resume_execution(self, execution_id, user_id):
        """Resume a paused cycle execution."""
        execution = CycleExecution.query.get_or_404(execution_id)

        # Check permissions
        if execution.configuration.created_by != user_id:
            raise PermissionError("Not authorized")

        # Check if resumable
        if execution.status != 'paused':
            raise ValueError(f"Cannot resume execution in status: {execution.status}")

        # Update status
        execution.status = 'running'
        db.session.commit()

        # Signal orchestrator
        self.orchestrator.resume_execution(execution_id)

        # Broadcast status update
        if self.socket_io:
            self.socket_io.emit('cycle_status_update', {
                'execution_id': str(execution_id),
                'status': 'running'
            }, room=f'cycle_{execution_id}')

        logger.info(f"Resumed execution {execution_id}")
        return execution

    def stop_execution(self, execution_id, user_id, reason=None):
        """Stop a running or paused cycle execution."""
        execution = CycleExecution.query.get_or_404(execution_id)

        # Check permissions
        if execution.configuration.created_by != user_id:
            raise PermissionError("Not authorized")

        # Update status
        execution.status = 'stopped'
        if reason:
            execution.error_message = f"Stopped by user: {reason}"
        db.session.commit()

        # Signal orchestrator
        self.orchestrator.stop_execution(execution_id)

        # Broadcast status update
        if self.socket_io:
            self.socket_io.emit('cycle_status_update', {
                'execution_id': str(execution_id),
                'status': 'stopped'
            }, room=f'cycle_{execution_id}')

        logger.info(f"Stopped execution {execution_id}")
        return execution

    def _calculate_total_actions(self, sequence, days):
        """Calculate total number of actions in sequence."""
        total = 0
        for action_def in sequence.get('actions', []):
            if action_def['type'] == 'action':
                total += 1
            elif action_def['type'] == 'loop':
                loop_actions = len(action_def.get('actions', []))
                iterations = action_def.get('iterations', 1)
                total += loop_actions * iterations
        return total * days  # Multiply by number of days
```

---

## Enhanced API Routes

```python
# loopai_src/web/routes/agentlife.py (Enhanced)

import logging
from flask import jsonify, request, current_app
from flask.blueprints import Blueprint
from web.routes.middleware import token_required
from web.services.cycle_manager import CycleManager
from web.services.constellation_manager import ConstellationManager
from core.services.session_manager import session_manager

logger = logging.getLogger(__name__)
agentlife_bp = Blueprint('agentlife', __name__)

# Initialize services (with Socket.IO from app)
def get_cycle_manager():
    from web.web_interface import socketio
    return CycleManager(socket_io=socketio)

def get_constellation_manager():
    return ConstellationManager()

# ============================================================================
# CYCLE MANAGEMENT ENDPOINTS
# ============================================================================

@agentlife_bp.route('/api/agentlife/cycles/', methods=['POST'])
@token_required
def create_cycle(current_user):
    """Create a new cycle configuration."""
    try:
        cycle_data = request.get_json()
        manager = get_cycle_manager()
        cycle = manager.create_cycle(current_user.id, cycle_data)
        return jsonify({
            'success': True,
            'cycle': cycle.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating cycle: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/', methods=['GET'])
@token_required
def list_cycles(current_user):
    """List cycle configurations for current user."""
    try:
        filters = {
            'status': request.args.get('status'),
            'tags': request.args.getlist('tags')
        }
        filters = {k: v for k, v in filters.items() if v}

        manager = get_cycle_manager()
        cycles = manager.get_cycles(current_user.id, filters)

        return jsonify({
            'success': True,
            'cycles': [c.to_dict() for c in cycles],
            'total': len(cycles)
        }), 200
    except Exception as e:
        logger.error(f"Error listing cycles: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/<cycle_id>/', methods=['GET'])
@token_required
def get_cycle(current_user, cycle_id):
    """Get a specific cycle configuration."""
    try:
        manager = get_cycle_manager()
        cycle = manager.get_cycle(cycle_id, current_user.id)
        return jsonify({
            'success': True,
            'cycle': cycle.to_dict(include_executions=True)
        }), 200
    except PermissionError:
        return jsonify({'success': False, 'error': 'Not authorized'}), 403
    except Exception as e:
        logger.error(f"Error getting cycle: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/<cycle_id>/', methods=['PUT'])
@token_required
def update_cycle(current_user, cycle_id):
    """Update a cycle configuration."""
    try:
        cycle_data = request.get_json()
        manager = get_cycle_manager()
        cycle = manager.update_cycle(cycle_id, current_user.id, cycle_data)
        return jsonify({
            'success': True,
            'cycle': cycle.to_dict()
        }), 200
    except (ValueError, PermissionError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating cycle: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/<cycle_id>/', methods=['DELETE'])
@token_required
def delete_cycle(current_user, cycle_id):
    """Delete a cycle configuration."""
    try:
        manager = get_cycle_manager()
        manager.delete_cycle(cycle_id, current_user.id)
        return jsonify({
            'success': True,
            'message': 'Cycle deleted successfully'
        }), 200
    except (ValueError, PermissionError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error deleting cycle: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/<cycle_id>/start/', methods=['POST'])
@token_required
def start_cycle(current_user, cycle_id):
    """Start a cycle execution."""
    try:
        options = request.get_json() or {}
        manager = get_cycle_manager()
        execution = manager.start_cycle(cycle_id, current_user.id, options)
        return jsonify({
            'success': True,
            'execution': execution.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error starting cycle: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@agentlife_bp.route('/api/agentlife/cycles/executions/<execution_id>/pause/', methods=['POST'])
@token_required
def pause_execution(current_user, execution_id):
    """Pause a running execution."""
    try:
        manager = get_cycle_manager()
        execution = manager.pause_execution(execution_id, current_user.id)
        return jsonify({
            'success': True,
            'execution': execution.to_dict()
        }), 200
    except (ValueError, PermissionError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error pausing execution: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/executions/<execution_id>/resume/', methods=['POST'])
@token_required
def resume_execution(current_user, execution_id):
    """Resume a paused execution."""
    try:
        manager = get_cycle_manager()
        execution = manager.resume_execution(execution_id, current_user.id)
        return jsonify({
            'success': True,
            'execution': execution.to_dict()
        }), 200
    except (ValueError, PermissionError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error resuming execution: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@agentlife_bp.route('/api/agentlife/cycles/executions/<execution_id>/stop/', methods=['POST'])
@token_required
def stop_execution(current_user, execution_id):
    """Stop a running or paused execution."""
    try:
        data = request.get_json() or {}
        reason = data.get('reason')
        manager = get_cycle_manager()
        execution = manager.stop_execution(execution_id, current_user.id, reason)
        return jsonify({
            'success': True,
            'execution': execution.to_dict()
        }), 200
    except (ValueError, PermissionError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error stopping execution: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# CONSTELLATION ENDPOINTS
# (Similar pattern, see 02_ACTION_CONSTELLATION_DESIGN.md)
# ============================================================================

# ============================================================================
# MONITORING & ANALYTICS ENDPOINTS
# (See 05_REALTIME_MONITORING.md)
# ============================================================================
```

---

## Database Migrations

```bash
# Create migration
flask db migrate -d web/migrations -m "Add cycle management tables"

# Apply migration
flask db upgrade -d web/migrations
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_cycle_manager.py

import pytest
from web.services.cycle_manager import CycleManager
from web.admin_models.cycle_configuration import CycleConfiguration

class TestCycleManager:
    def test_create_cycle(self, db_session, test_user):
        manager = CycleManager()
        cycle_data = {
            'name': 'Test Cycle',
            'days': 3,
            'agents': ['FRBG/agent1'],
            'constellation_id': 'standard-daily-workflow'
        }

        cycle = manager.create_cycle(test_user.id, cycle_data)
        assert cycle.name == 'Test Cycle'
        assert cycle.days == 3

    def test_start_cycle(self, db_session, test_cycle):
        manager = CycleManager()
        execution = manager.start_cycle(test_cycle.id, test_cycle.created_by)
        assert execution.status == 'queued'
        assert execution.total_days == test_cycle.days
```

---

## Next Steps

1. Create database models
2. Write migrations
3. Implement service layer
4. Create API endpoints
5. Write unit tests
6. Integration testing
7. Performance optimization
8. Documentation

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related:** [00_OVERVIEW.md](./00_OVERVIEW.md), [03_FRONTEND_INTEGRATION.md](./03_FRONTEND_INTEGRATION.md)
