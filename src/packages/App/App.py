from typing import Callable, Dict, Optional

class App:
    __routes: Dict[str, tuple[Callable[[list[str]], None], Optional[Callable[[list[str]], bool]]]] = {}

    @staticmethod
    def routes(
        name: str,
        func: Callable[[list[str]], None],
        middleware: Optional[Callable[[list[str]], bool]] = None
    ) -> None:
        App.__routes[name] = (func, middleware)

    @staticmethod
    def run(argv: list[str]) -> None:
        if not argv:
            print("Error: No command provided.")
            return

        route_name = argv[0]
        args = argv[1:]

        if route_name not in App.__routes:
            print(f"Error: Unknown command '{route_name}'.")
            return

        func, middleware = App.__routes[route_name]

        if middleware:
            allowed = middleware(args)
            if not allowed:
                print(f"Error: Middleware blocked route '{route_name}'.")
                return

        func(args)
