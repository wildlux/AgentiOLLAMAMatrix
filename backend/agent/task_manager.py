import threading
import time
import uuid
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import queue

class Task:
    """Rappresenta un task da eseguire"""
    
    def __init__(self, task_id: str, function: Callable, args: tuple = (), kwargs: dict = None):
        self.task_id = task_id
        self.function = function
        self.args = args
        self.kwargs = kwargs or {}
        self.status = "pending"  # pending, running, completed, failed
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    def execute(self) -> None:
        """Esegue il task"""
        self.status = "running"
        self.started_at = datetime.now()
        
        try:
            self.result = self.function(*self.args, **self.kwargs)
            self.status = "completed"
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
        finally:
            self.completed_at = datetime.now()

class TaskManager:
    """Gestione avanzata dei task per l'agente MCP"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.max_concurrent = config['tasks']['max_concurrent']
        self.task_timeout = config['tasks']['timeout']
        
        self.task_queue = queue.Queue()
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        self.workers: List[threading.Thread] = []
        
        self.lock = threading.Lock()
        self.running = False
    
    def start(self) -> None:
        """Avvia il task manager"""
        if not self.running:
            self.running = True
            for i in range(self.max_concurrent):
                worker = threading.Thread(target=self._worker_loop, daemon=True)
                worker.start()
                self.workers.append(worker)
    
    def stop(self) -> None:
        """Ferma il task manager"""
        self.running = False
        for worker in self.workers:
            worker.join()
    
    def _worker_loop(self) -> None:
        """Loop principale del worker"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task:
                    self._execute_task(task)
            except queue.Empty:
                continue
    
    def _execute_task(self, task: Task) -> None:
        """Esegue un task con gestione del timeout"""
        with self.lock:
            self.active_tasks[task.task_id] = task
        
        # Crea un thread separato per il task con timeout
        task_thread = threading.Thread(target=task.execute)
        task_thread.start()
        task_thread.join(timeout=self.task_timeout)
        
        if task_thread.is_alive():
            # Task in timeout
            task.status = "failed"
            task.error = f"Task timeout after {self.task_timeout} seconds"
        
        with self.lock:
            self.completed_tasks.append(task)
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    def add_task(self, function: Callable, args: tuple = (), kwargs: dict = None) -> str:
        """Aggiunge un nuovo task alla coda"""
        task_id = str(uuid.uuid4())
        task = Task(task_id, function, args, kwargs)
        self.task_queue.put(task)
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Restituisce lo stato di un task"""
        with self.lock:
            # Cerca nei task attivi
            if task_id in self.active_tasks:
                task = self.active_tasks[task_id]
                return self._task_to_dict(task)
            
            # Cerca nei task completati
            for task in reversed(self.completed_tasks):
                if task.task_id == task_id:
                    return self._task_to_dict(task)
        
        return None
    
    def _task_to_dict(self, task: Task) -> Dict:
        """Converte un task in dizionario"""
        return {
            'task_id': task.task_id,
            'status': task.status,
            'result': task.result,
            'error': task.error,
            'created_at': task.created_at.isoformat(),
            'started_at': task.started_at.isoformat() if task.started_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'duration': self._calculate_duration(task)
        }
    
    def _calculate_duration(self, task: Task) -> Optional[float]:
        """Calcola la durata del task in secondi"""
        if task.completed_at and task.started_at:
            return (task.completed_at - task.started_at).total_seconds()
        return None
    
    def get_active_tasks(self) -> List[Dict]:
        """Restituisce tutti i task attivi"""
        with self.lock:
            return [self._task_to_dict(task) for task in self.active_tasks.values()]
    
    def get_completed_tasks(self, limit: int = 10) -> List[Dict]:
        """Restituisce i task completati"""
        with self.lock:
            return [self._task_to_dict(task) for task in self.completed_tasks[-limit:]]
    
    def clear_completed_tasks(self) -> None:
        """Pulisce i task completati"""
        with self.lock:
            self.completed_tasks = []
    
    def get_stats(self) -> Dict:
        """Restituisce statistiche sui task"""
        with self.lock:
            return {
                'active_tasks': len(self.active_tasks),
                'completed_tasks': len(self.completed_tasks),
                'queue_size': self.task_queue.qsize(),
                'max_concurrent': self.max_concurrent
            }