from typing import Any, Dict

class MemoryEngine:
    def __init__(self) -> None:
        self.active = False

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def status(self) -> str:
        return 'active' if self.active else 'stopped'

    def summarize(self, records: Any) -> Dict[str, Any]:
        if not records:
            return {'summary': 'Sem dados para resumir', 'record_count': 0}

        snippet = ' '.join(str(records[0]).split()[:20])
        return {
            'summary': f'Resumo de memória: {snippet}...',
            'record_count': len(records) if hasattr(records, '__len__') else 1,
        }
