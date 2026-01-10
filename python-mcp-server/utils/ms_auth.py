import msal, asyncio, sys
from pathlib import Path
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


class MSAuth:
    """Handles Microsoft authentication"""

    def __init__(self, client_id, tenant_id, token_cache_file):
        self.app = msal.PublicClientApplication(
            client_id, # this is what associates the server with the app reg.
            authority=f"https://login.microsoftonline.com/{tenant_id}",
            token_cache=self._load_cache(token_cache_file)
        )
        self.executor = ThreadPoolExecutor(max_workers=1)

    def _load_cache(self, token_cache_file: Path):
        """Load token cache from file"""
        cache = msal.SerializableTokenCache()
        if token_cache_file.exists():
            cache.deserialize(token_cache_file.read_text())
        return cache
    
    def _save_cache(self, token_cache_file: Path):
        """Write token cache to file"""
        if self.app.token_cache.has_state_changed:
            token_cache_file.write_text(self.app.token_cache.serialize())

    async def get_token(self, token_cache_file: Path, scopes):
        """Get access token with device code flow"""
        try:
            # Try token from cache
            accounts = self.app.get_accounts()
            print(f"[AUTH] get_accounts() found {len(accounts)} cached accounts", file=sys.stderr, flush=True)

            if accounts:
                # acquire access token without user interaction
                result = self.app.acquire_token_silent(scopes, account=accounts[0])
                if result and "access_token" in result: 
                    print("[AUTH] Using cached token", file=sys.stderr, flush=True)
                    return result["access_token"]
        
            # Try authenticating with NEW device code
            print("[AUTH] No cached token, initiating device flow...", file=sys.stderr, flush=True)
            flow = self.app.initiate_device_flow(scopes=scopes)

            if "user_code" not in flow:
                raise Exception("Failed to create device flow")
        
            # Show user the device code for authentication
            print("\n", file=sys.stderr, flush=True)
            print("=" * 60, file=sys.stderr, flush=True)
            print(flow["message"], file=sys.stderr, flush=True)
            print("=" * 60, file=sys.stderr, flush=True)
            print("\n", file=sys.stderr, flush=True)
            print("[AUTH] Pending user authentication...", file=sys.stderr, flush=True)

            # await user authentication
            loop = asyncio.get_event_loop()
            # result = self.app.acquire_token_by_device_flow(flow) 
            result = await loop.run_in_executor( # blocking
                self.executor,
                self.app.acquire_token_by_device_flow,
                flow
            )

            if "access_token" in result:
                self._save_cache(token_cache_file)
                return result["access_token"]
            else:
                raise Exception(f"Authentication failed: {result.get('error_description')}")
        except Exception as e:
            print("[AUTH] Exception in MSAuth.get_token", file=sys.stderr, flush=True)
            raise 

