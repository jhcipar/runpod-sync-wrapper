import inspect
import os
from typing import Any, Callable, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn


Handler = Callable[[Any], Any]
InitHook = Optional[Callable[[], Any]]


class RunpodSyncWrapper:
    def __init__(self, handler: Handler, init: InitHook = None, route: str = "/__runpod/invoke"):
        self.handler = handler
        self.init = init
        self.route = route
        self.ready = False
        self.app = FastAPI()
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.on_event("startup")
        async def startup() -> None:
            if self.init is not None:
                if inspect.iscoroutinefunction(self.init):
                    await self.init()
                else:
                    self.init()
            self.ready = True

        @self.app.get("/ping")
        async def ping() -> JSONResponse:
            if not self.ready:
                return JSONResponse(status_code=204, content={"status": "initializing"})
            return JSONResponse(status_code=200, content={"status": "healthy"})

        @self.app.post(self.route)
        async def invoke(request: Request) -> JSONResponse:
            if not self.ready:
                raise HTTPException(status_code=503, detail="worker is still starting")

            try:
                body = await request.json()
            except Exception as exc:
                raise HTTPException(status_code=400, detail="invalid json body") from exc

            try:
                if inspect.iscoroutinefunction(self.handler):
                    result = await self.handler(body)
                else:
                    result = self.handler(body)
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

            return JSONResponse(status_code=200, content={"output": result})


def create_app(handler: Handler, init: InitHook = None, route: str = "/__runpod/invoke") -> FastAPI:
    return RunpodSyncWrapper(handler=handler, init=init, route=route).app


def run(handler: Handler, init: InitHook = None, route: str = "/__runpod/invoke") -> None:
    app = create_app(handler=handler, init=init, route=route)
    port = int(os.getenv("PORT", "8888"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    def example_handler(event: Any) -> Any:
        prompt = event.get("prompt", "") if isinstance(event, dict) else ""
        return {"generated_text": f"Response to: {prompt}"}

    run(example_handler)
