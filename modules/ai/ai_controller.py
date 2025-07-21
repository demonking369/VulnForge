import os

class AIController:
    def run_ai_task(self, task, context=None, debug=False):
        try:
            result = self.llm.run_task(task, context=context, debug=debug)
            if not result or not str(result).strip():
                result = f"[AI Fallback] No result for task: {task}"
            self._log_ai_task(task, result, debug)
            return result
        except Exception as e:
            self._log_ai_task(task, f"[AI ERROR] {e}", debug)
            return f"[AI ERROR] {e}"

    def _log_ai_task(self, task, result, debug):
        log_path = os.path.expanduser("~/.vulnforge/sessions/logs/ai_controller.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(f"[TASK] {task}\n[RESULT] {result}\n[DEBUG] {debug}\n\n") 