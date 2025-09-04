from mcp.server.fastmcp import FastMCP, Context  
import json  
  
# FastMCPサーバーの作成  
mcp = FastMCP("Token Echo Server")  
  
@mcp.tool()  
async def echo_headers(ctx: Context) -> str:  
    """ヘッダーからトークン情報を取得して返すツール"""  
    # リクエストコンテキストからヘッダー情報を取得  
    request = ctx.request_context.request  
    headers = dict(request.headers)  
      
    # 認証関連のヘッダーを抽出  
    auth_headers = {  
        key.lower(): value   
        for key, value in headers.items()   
        if key.lower() in ['authorization', 'x-custom-header', 'x-trace-id']  
    }  
      
    return json.dumps(auth_headers, indent=2)  
  
if __name__ == "__main__":  
    mcp.run(transport="streamable-http")
